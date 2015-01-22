import simplejson as json
import random
import matplotlib.pyplot as plt

def remove_urls(url_file, to_remove, use, delete) :
	with open(to_remove, 'r') as r_file : 
		remove_words = [x.strip() for x in r_file]
	to_write = {}
	bad = []
	with open(url_file, 'r') as u_file : 
		data = json.load(u_file)
		for url_id in data : 
			flag = 0
			for word in remove_words :
				if word in data[url_id]['title'] :
					if word in ['YouTube','Instagram'] :
						decision = 'y'
					else :
						print data[url_id]['title']
						print word
						decision = raw_input("Skip? y/n\n")
					if decision == 'y' :
						flag = 1
						bad.append(url_id)
						break
			if flag == 0 :
				to_write[url_id] = data[url_id]
	with open(use, 'w') as op_file :
		op_file.write(json.dumps(to_write))
	print len(to_write.keys())
	with open(delete, 'w') as bad_file : 
		for word in bad :
			bad_file.write(word + '\n')

#TODO : Change, turn into random, make new file for this to remove arabic titles		
def pick_random(n, input_file, sample) :
	count = 0
	samples = {}
	with open(input_file, 'r') as input_obj :
		data = json.load(input_obj)
	for url_id in data :
		print data[url_id]['title']
		dec = raw_input("Include? y/n")
		if dec == 'y' and count < 100 :
			samples[url_id] = data[url_id]
		count += 1
		if count == 100 :
			break
	with open(sample, 'w') as sample_obj :
		sample_obj.write(json.dumps(samples))

def tag_urls(input_file) :
	tag_dict = {'n' : 'news', 'b' : 'blog', 'a' : 'article', 'e' : 'evaluative', 'd' : 'descriptive' }
	with open(input_file, 'r') as input_obj :
		data = json.load(input_obj)
	for url_id in data : 
		print data[url_id]['url']
		print data[url_id]['text_boilerpipe'], '\n'
		tag_letters = raw_input("Enter tags : ")
		data[url_id]['tags'] = [tag_dict[t] for t in list(tag_letters)]
		print data[url_id]['tags']
		data[url_id]['consider'] = raw_input("Consider url?(y/n) ")
	with open(input_file, 'w') as op_obj :
		op_obj.write(json.dumps(data))


def pick_sample(size, input_file, op_file) :
	with open(input_file, 'r') as ip_obj :
		data = json.load(ip_obj)
	count = 0
	for urlid in data : 
		data[urlid]['temp_id'] = count 
		count += 1
	num = 0
	samples = {}
	selected = []
	while num < size :
		pick = random.randint(0, count)
		if pick not in selected :
			for urlid in data : 
				if 'temp_id' in data[urlid].keys() and data[urlid]['temp_id'] == pick :
					break
			print urlid
			samples[urlid] = data[urlid]
			selected.append(pick)
			del samples[urlid]['temp_id']
			num += 1
	with open(op_file, 'w') as op_obj :
		op_obj.write(json.dumps(samples))
	

def check_threshold_length(input_file) :
	with open(input_file, 'r') as input_obj :
		data = json.load(input_obj)
	
	word_count = []
	char_count = []
	consider = []
	for url_id in data :
		word_count.append(len(data[url_id]['text_newspaper'].split()))
		char_count.append(len(data[url_id]['text_newspaper']))
		if data[url_id]['consider'] == 'y' :
			consider.append('b')
		else : 
			consider.append('r')
	wc = sorted(zip(word_count, consider))
	xa = [i for i in range(0, len(wc)/2)]
	w = [x for x, y in wc]
	c = [y for x, y in wc]
	plt.scatter(xa, w[:len(w)/2], c = c[:len(c)/2])
	#plt.scatter(xa, w, c = c)
	plt.ylabel('Number of words')
	plt.show()
