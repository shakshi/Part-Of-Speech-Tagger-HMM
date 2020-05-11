import sys
import json
import operator 

input_file= sys.argv[1]

all_tags= set()
open_tags= []

tag_count={}
emission={}
transition={}
possible_tags={}

f= open(input_file, 'r', encoding="utf-8")
content= f.read()
lines= content.split('\n')

for line in lines:

	wordlist= line.split()
	n= len(wordlist)

	words=[]
	tags=[]

	for i in range(n):
		a= wordlist[i].rsplit('/', 1)

		if len(a) == 2:
			word, tag= a[0], a[1]
			words.append(word)
			tags.append(tag)


	for i in range(len(words)):
		
		word= words[i]
		tag= tags[i]

		all_tags.add(tag)

		if tag in tag_count:
			tag_count[tag] += 1
		else:
			tag_count[tag]=1

		if tag in emission:
			if word in emission[tag]:
				emission[tag][word] += 1
			else:
				emission[tag][word]=1
		else:
			emission[tag]= { word : 1}

		if i==0:
			'''
			add transition from q0 to that tag/ or prob to start from that tag 
			'''

			if "start" not in transition:
				transition["start"]= {}

			if tag in transition["start"]:
				transition["start"][tag] +=1
			else:
				transition["start"][tag] = 1

		if i==(n-1):
			tag2= 'end'
		else:
			tag2= tags[i+1]
		
		
		if tag in transition:
			if tag2 in transition[tag]:
				transition[tag][tag2] += 1
			else:
				transition[tag][tag2]=1
		else:
			transition[tag]= {tag2: 1}

		if word in possible_tags:
			if tag in possible_tags[word]:
				possible_tags[word][tag] += 1
			else:
				possible_tags[word][tag] = 1
		else:
			possible_tags[word] = {tag : 1} 


def convert_to_prob(all_tags, tag_count, transition, emission):

	for tag in all_tags:

		if tag in transition:

			for tag2 in all_tags:
				
				if tag2 in transition[tag]:
					transition[tag][tag2] += 1
				else:
					transition[tag][tag2] = 1
		else:

			# no transition from this tag in training data 
			# so equal transition prob to all the rest tags 
			transition[tag]= {}

			for tag2 in all_tags:
				
				transition[tag][tag2] = 1
		
	for tag in transition:	
		total = sum(transition[tag].values())
		for tag2, count in transition[tag].items():
			transition[tag][tag2] = count/total

	for tag in emission:

		#total= sum(emission[tag].values())
		total= tag_count[tag]
		for word, count in emission[tag].items():
			emission[tag][word] = count/total

	return transition, emission

all_tags.add("end")
transition, emission= convert_to_prob(all_tags, tag_count, transition, emission)

tag_count= dict(sorted(tag_count.items(), key=operator.itemgetter(1),reverse=True))
n= 17
print(len(list(tag_count.keys())))
open_tags = list(tag_count.keys())[:n]

print("open tags: ", open_tags)
#print("transition: ", transition)
#print(emission)

#print(tag_count)

ans = {}
ans["open_tags"]=open_tags
ans["tag_count"]= tag_count
ans["emission"]= emission
ans["transition"]= transition
ans["possible_tags"]= possible_tags

fp= open("hmmmodel.txt", 'w')
json.dump(ans, fp)

