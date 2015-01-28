from bs4 import BeautifulSoup
import re
import os
import multiprocessing

def read_and_tokenize (file_name):
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

	xml_file_filtered_words = [word for word in xml_file_text_tokenized if len(word) >=3]
	xml_file_filtered_text = " ".join(xml_file_filtered_words)
	return xml_file_filtered_text

root_path = "/Users/praphull/Desktop/msProject/nyt_corpus/"
paths = [os.path.join(root, name) for root, dirs, files in os.walk(root_path) for name in files]
paths_list = []
num = 10000
no_of_parts = len(paths) / num
if len(paths) % num != 0:
	no_of_parts += 1
paths_list = [paths[a*num:(a+1)*num] for a in range(no_of_parts)]

out_handle = open("nyt_corpus_original.txt", 'wb')
file_count = 0
for paths in paths_list:
	p = multiprocessing.Pool(processes=(multiprocessing.cpu_count() - 1))
	results = p.map(read_and_tokenize, paths)
	p.close()
	p.join()

	out_handle.write("\n".join(results) + "\n")
	file_count += 1
	if file_count % 10 == 0:
		print file_count*num
	else:
		print '.'

out_handle.close()
#1855658