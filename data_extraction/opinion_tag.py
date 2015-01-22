import simplejson as json
import matplotlib.pyplot as plt

def calc_tags(opinion_set, input_file) :
	with open(opinion_set, 'r') as opinion_obj :
		opinion_words = []
		weights = []
		for line in opinion_obj :
			parts = line.split()
			opinion_words.append(parts[2].split('=')[1])
			if parts[0].split('=')[1] == 'weaksubj' :
				weights.append(0.5)
			else :
				weights.append(1)
	with open(input_file, 'r') as to_tag :
		data = json.load(to_tag)
		
		op_word_counts = []
		weighted_op_word_counts = []
		c_subj = []
		for url_id in data :
			if data[url_id]['consider'] == 'y' :
				#Putting together color array for evaluative/subjective
				if 'evaluative' in data[url_id]['tags'] or 'mixed' in data[url_id]['tags']:
					c_subj.append('b')
				elif 'descriptive' in data[url_id]['tags']:
					c_subj.append('r')
				
				#Regular count
				try : 	
					opinion_word_count = float(len(set([word for word in opinion_words if word in data[url_id]['text_newspaper']]))) / float(len(data[url_id]['text_newspaper'].split())) * 10.0
				except ZeroDivisionError :
					print 'Divide by zero!'
				op_word_counts.append(opinion_word_count)
				
				
				#Weighted opinion word counts - counting strong 1 and weak 0.5

				weighted_opinion_count = 0
				for word in opinion_words :
					if word in data[url_id]['text_newspaper'] :
					#Count according to strong weak subj / only strong. Comment appropriate.
					#General weights will be added if necessary
						#weighted_opinion_count += weights[opinion_words.index(word)]
						if weights[opinion_words.index(word)] == 1 :
							weighted_opinion_count += 1
				
				try :
					weighted_op_word_counts.append(float(weighted_opinion_count) / float(len(data[url_id]['text_newspaper']))* 10 )
				except ZeroDivisionError :
					print 'Divide by zero!'

	wc = sorted(zip(op_word_counts, c_subj))
	w = [x for x,y in wc]
	c = [y for x,y in wc]
	plt.scatter([i for i in range(0, len(op_word_counts))],w,c = c)
	plt.xlabel('Samples')
	plt.ylabel('Number of opinion words')
	plt.title('Direct count')
	plt.show()

	wc = sorted(zip(weighted_op_word_counts, c_subj))
	w = [x for x,y in wc]
	c = [y for x,y in wc]
	plt.scatter([i for i in range(0, len(weighted_op_word_counts))],w,c = c)
	plt.xlabel('Samples')
	plt.ylabel('Number of opinion words')
	plt.title('Weighted count')
	plt.show()

def formality_tags(formal, informal,  input_file) :
	
	with open(formal,'r') as formal_obj : 
		formal_words = [line.strip() for line in formal_obj]

	with open(informal, 'r') as informal_obj :
		informal_words = [line.strip() for line in informal_obj]
			
	with open(input_file, 'r') as to_tag :
		data = json.load(to_tag)
	
	compare_against = []
	compare_to = []
	formal_count = []
	informal_count = []
	c = []
	for url_id in data : 
		if data[url_id]['consider'] == 'y' :
			text = data[url_id]['text_newspaper'].split()
			formal_occurrence = [word for word in formal_words if word in text]
			informal_occurrence =  [word for word in informal_words if word in text]

			formal_count.append(float(len(set(formal_occurrence))) / float(len(data[url_id]['text_newspaper'])) * 10) 
			informal_count.append(float(len(set(informal_occurrence))) / float(len(data[url_id]['text_newspaper'])) * 10) 

			print formal_occurrence
			print data[url_id]['url']
			#print informal_occurrence
			#print len(informal_occurrence)
			if 'traditional' in data[url_id]['tags'] : 
				c.append('r')
				compare_against.append(0)
			elif 'nontraditional' in data[url_id]['tags']:
				c.append('b')
				compare_against.append(1)
			if len(formal_occurrence) == 0 :
				compare_to.append(1)
			else :
				compare_to.append(0)
	
	
	matches = len([1 for i in compare_to if i == compare_against[compare_to.index(i)]])
	print (matches) , '/' , len(compare_to)
	

	wc = sorted(zip(formal_count, c))
	w = [x for x,y in wc]
	co = [y for x,y in wc]
	plt.scatter([i for i in range(0, len(formal_count))],w,c = co)
	plt.xlabel('Samples')
	plt.ylabel('Number of formal word matches (per 10 words)')
	plt.title('Compare to formal count')
	plt.show()

	wc = sorted(zip(informal_count, c))
	w = [x for x,y in wc]
	co = [y for x,y in wc]
	plt.scatter([i for i in range(0, len(informal_count))],w,c = co)
	plt.xlabel('Samples')
	plt.ylabel('Number of informal word matches (per 10 words)')
	plt.title('Compare to informal count')
	plt.show()
