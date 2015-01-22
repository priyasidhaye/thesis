import simplejson as json
import sys

def incremental_tag_urls(input_file, output_file) :
	tag_dict = {'n' : 'nontraditional', 't' : 'traditional', 'e' : 'evaluative', 'd' : 'descriptive', 'm' : 'mixed' }
	with open(input_file, 'r') as input_obj :
		data = json.load(input_obj)
	ncases = len(data)
	ntodo = len([case for case in data if 'tags' not in data[case]])
    
	print '%d of %d to be tagged' % (ntodo, ncases)
	raw_input('Press any key to begin.') 
    
	try:	
		for url_id in data:
			tagged = 'tags' in data[url_id]
			while not tagged:
				try:
					print data[url_id]['url']
					print data[url_id]['text_newspaper'].encode('ascii', 'ignore'), '\n'
					tag_letters = raw_input("Enter tags : ")
					if 'q' in tag_letters: raise ValueError()
					for t in list(tag_letters):
						assert t in tag_dict
					assert len(tag_letters) > 0
					comment = raw_input("Enter comment(default none): ")
					if comment == 'q': raise ValueError()
					consider = raw_input("Consider url? (y/n)")
					if consider in 'q': raise ValueError()
					assert consider in 'yn' and len(consider) > 0
					data[url_id]['tags'] = [tag_dict[t] for t in list(tag_letters)]
					print data[url_id]['tags']
					if comment != "" :
						data[url_id]['comment'] = comment
						print data[url_id]['comment']
					data[url_id]['consider'] = consider
					print data[url_id]['consider']
					tagged = True
				except AssertionError:
					continue
	except ValueError:
		pass
	with open(output_file, 'w') as op_obj :
		op_obj.write(json.dumps(data))


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print '''Usage: python ./tag.py <input_json_file> (<output_json_file>)
        
If not specified, output_file will be the input_file and overwrite it.
'''
		exit()
	input_file = sys.argv[1]
	if len(sys.argv) > 2:
		output_file = sys.argv[2]
	else:
		output_file = input_file
	incremental_tag_urls(input_file, output_file)
