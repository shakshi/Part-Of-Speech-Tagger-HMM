import sys
import json
import string

def hmm(words, tag_count, possible_tags, emission, transition, open_tags):

	#apply viterbi algorithm 
	n= len(words)
	#print("\n\nn", n)

	states=[["start"]]
	prob= { (0, 'start') : 1}
	backpointer = {}

	all_tags= list(tag_count.keys())
	t=1
	while t<=n:
		
		word= words[t-1]
		new_states=[]
		#print("\nword: ", word)
		#print("prev states: ", states[t-1])
		

		pt=[]
		if word in possible_tags:
			pt= list(possible_tags[word].keys())
			#print("possible tags: ", pt)
			for tag in pt:
			
				max_prob= 0 
				max_state= 0 

				for prev_state in states[t-1]:

					'''
					prob to go from prev state to this state 
					transition prob and prob to emit this tag at this state 
					calculate for each transition and then find the max 
					'''
					emit = 0 
					trans =0 

					if tag in emission:
						if word in emission[tag]:
							emit= emission[tag][word]

					if prev_state in transition:
						if tag in transition[prev_state]:
							trans= transition[prev_state][tag]

					pr= prob[(t-1, prev_state)]* trans * emit
					
					if pr >= max_prob:
						max_prob= pr
						max_state= prev_state

				if max_prob > 0:
					backpointer[(t, tag)] = max_state
					prob[(t, tag)]= max_prob

					new_states.append(tag)
			
		else:
			# word unknown 
			# also assume emission equal to 1 this is important 
					
			'''
			if the word is unknown then ignore emission prbabilities and assume 
			all tags and just use transition prob 
			'''

			pt= open_tags
			#print("possible tags: ", pt)
			for tag in pt:
			
				max_prob= 0 
				max_state= 0 

				for prev_state in states[t-1]:

					'''
					prob to go from prev state to this state 
					transition prob and prob to emit this tag at this state 
					calculate for each transition and then find the max 
					'''
					trans =0 

					if prev_state in transition:
						if tag in transition[prev_state]:
							trans= transition[prev_state][tag]

					pr= prob[(t-1, prev_state)]* trans 
					
					if pr >= max_prob:
						max_prob= pr
						max_state= prev_state

				if max_prob > 0:
					backpointer[(t, tag)] = max_state
					prob[(t, tag)]= max_prob

					new_states.append(tag)

	

		#print("new states", new_states)
		if len(new_states)==0:
			##print("breaking in middle")
			break;

		states.append(new_states)
		t += 1

	#for last state 
	#end state 
	
	if t==(n+1):
		'''
		reached last state
		'''
		#print("reached last state")
		t= n+1
		max_prob= 0 
		max_state= 0 

		#print("\nprev states: ", states[t-1])

		for prev_state in states[t-1]:

			trans=0 
			if prev_state in transition:
				if "end" in transition[prev_state]:
					trans= transition[prev_state]["end"]

			pr= prob[(t-1, prev_state)]* trans
			
			if pr >= max_prob:
				max_prob= pr
				max_state= prev_state

		if max_prob > 0:
			backpointer[(t, "end")] = max_state
			prob[(t, "end")]= max_prob
		'''
		else:
			print("no path to end state")
		'''

	# now track all back pointers from the end state 
	element= (n+1, "end")

	tags=[]
	if element in backpointer:

		#print("else no sequence possible")
		s= backpointer[(n+1, "end")]
		x= n;
		
		while x>=1:

			tags.append(s)
			s= backpointer[(x, s)]
			x = x-1

		tags.reverse()
	
	return tags


model_file= open("hmmmodel.txt", 'r', encoding="utf-8")
content = model_file.read()
ans= json.loads(content)

open_tags= ans["open_tags"]
tag_count= ans["tag_count"]
emission= ans["emission"]
transition= ans["transition"]
possible_tags= ans["possible_tags"]


test_file= sys.argv[1]
test_fp= open(test_file, 'r', encoding="utf-8")
lines= test_fp.read().split('\n')

punct = str.maketrans(string.punctuation, ' '*len(string.punctuation))
out= open("hmmoutput.txt", 'w', encoding="utf-8")

for line in lines:
	
	#print("\nline: ", line)
	#line = line.translate(punct)
	words= line.split(' ')
	
	if len(words) > 0:
		tags= hmm(words, tag_count, possible_tags, emission, transition, open_tags)
		n= len(tags)
		
		#print("tags:", end=" ")
		for i in range(n):
			#print(words[i] + '/' + tags[i].upper(), end=" ")
			out.write(words[i] + '/' + tags[i].upper() + " ")

		#print(" ")
	out.write("\n")

out.close()

