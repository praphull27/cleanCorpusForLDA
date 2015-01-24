from bs4 import BeautifulSoup
from nltk.stem.snowball import SnowballStemmer
import re
import os
import json
import gc
from collections import OrderedDict

stemmer = SnowballStemmer("english")

stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards', 'again', 
'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 
'always', 'am', 'among', 'amongst', 'amoungst', 'amount', 'an', 'and', 
'another', 'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 
'around', 'as', 'at', 'back', 'be', 'became', 'because', 'become', 'becomes', 
'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'below', 
'beside', 'besides', 'between', 'beyond', 'bill', 'both', 'bottom', 'but', 'by', 
'call', 'can', 'cannot', 'cant', 'co', 'computer', 'con', 'could', 'couldnt', 
'cry', 'did', 'de', 'describe', 'detail', 'do', 'does', 'doing', 'done', 'down', 
'due', 'during', 'each', 'eg', 'eight', 'either', 'eleven', 'else', 'elsewhere', 
'empty', 'enough', 'etc', 'even', 'ever', 'every', 'everyone', 'everything', 
'everywhere', 'except', 'few', 'fifteen', 'fify', 'fill', 'find', 'fire', 
'first', 'five', 'for', 'former', 'formerly', 'forty', 'found', 'four', 'from', 
'front', 'full', 'further', 'get', 'give', 'go', 'had', 'has', 'hasnt', 'have', 
'having', 'he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 
'hereupon', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'however', 
'hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed', 'interest', 'into', 'is', 
'it', 'its', 'itself', 'just', 'keep', 'last', 'latter', 'latterly', 'least', 
'less', 'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 
'mine', 'more', 'moreover', 'most', 'mostly', 'move', 'much', 'must', 'my', 
'myself', 'name', 'namely', 'neither', 'never', 'nevertheless', 'next', 'nine', 
'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 
'of', 'off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or', 'other', 
'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'part', 
'per', 'perhaps', 'please', 'put', 'rather', 're', 'same', 'see', 'seem', 
'seemed', 'seeming', 'seems', 'serious', 'several', 'she', 'should', 'show', 
'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some', 'somehow', 'someone', 
'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system', 
'take', 'ten', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 
'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 
'thereupon', 'these', 'they', 'thick', 'thin', 'third', 'this', 'those', 
'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 
'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 'un', 'under', 
'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well', 'were', 'what', 
'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 
'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 
'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with', 
'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself', 
'yourselves', 'the']

stopwords_single = [stemmer.stem(word) for word in stopwords]
stopwords.extend(stopwords_single)
stopwords = sorted(list(set(stopwords)))

dict_freq_filtered = {}
dict_freq_cleaned = {}

def read_clean_print (file_name):
	xml_file_handle = open(file_name, 'rb')
	xml_file_contents = xml_file_handle.read()
	xml_file_handle.close()

	xml_file_text = ''
	full_text_all = BeautifulSoup(xml_file_contents).find_all(class_="full_text")
	for full_text in full_text_all:
		xml_file_text += full_text.get_text(" ")
	xml_file_text = re.sub(r'[^a-zA-Z]', ' ', xml_file_text)
	xml_file_text = (xml_file_text.strip()).lower()
	xml_file_text_tokenized = xml_file_text.split()

	xml_file_filtered_words = [word for word in xml_file_text_tokenized if not stemmer.stem(word) in stopwords]
	xml_file_filtered_words = [word for word in xml_file_filtered_words if not word in stopwords]

	for word in xml_file_text_tokenized:
		if word in dict_freq_cleaned:
			dict_freq_cleaned[word] += 1
		else:
			dict_freq_cleaned[word] = 1

	for word in xml_file_filtered_words:
		if word in dict_freq_filtered:
			dict_freq_filtered[word] += 1
		else:
			dict_freq_filtered[word] = 1

	return (" ".join(xml_file_filtered_words), " ".join(xml_file_text_tokenized))

#read_clean_print('/Users/praphull/Desktop/msProject/nyt_corpus/1987/01/01/0000000.xml')

out_handle_filtered = open("nyt_courpus_without_stopwords.txt", 'wb')
out_handle_cleaned = open("nyt_courpus_with_stopwords.txt", 'wb')

file_count = 0

for root, dirs, files in os.walk("/Users/praphull/Desktop/msProject/nyt_corpus/", topdown=True):
	for name in files:
		if re.search(r'\.xml$', name):
			file_count += 1
			(filered, cleaned) = read_clean_print(os.path.join(root, name))
			out_handle_filtered.write(filered + "\n")
			out_handle_cleaned.write(cleaned + "\n")
			if file_count % 1000 == 0:
				print file_count
			else:
				if file_count % 100 == 0:
					print '.'
			gc.collect()

out_handle_filtered.close()
out_handle_cleaned.close()

out_handle_filtered = open("nyt_courpus_without_stopwords_count.txt", 'wb')
out_handle_cleaned = open("nyt_courpus_with_stopwords_txt.txt", 'wb')

d = OrderedDict(sorted(dict_freq_filtered.items(), key=lambda t: t[1], reverse=True))

for item in d.items():
	out_handle_filtered.write(item[0] + ' : ' + str(item[1]) + '\n')

d = OrderedDict(sorted(dict_freq_cleaned.items(), key=lambda t: t[1], reverse=True))

for item in d.items():
	out_handle_cleaned.write(item[0] + ' : ' + str(item[1]) + '\n')

out_handle_filtered.close()
out_handle_cleaned.close()
