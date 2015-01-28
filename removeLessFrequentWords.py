import re
from collections import OrderedDict

word_dict = {}
with open("nyt_corpus_without_stopwords.txt") as infile:
    for line in infile:
    	line = line.strip()
    	line_tokenize = line.split()
    	for word in line_tokenize:
    		if word in word_dict:
    			word_dict[word] += 1
    		else:
    			word_dict[word] = 1

print len(word_dict.keys())

word_dict = OrderedDict(sorted(word_dict.items(), key=lambda t: t[1], reverse=True))
words_less_frequent = []

out_handle_filtered_count = open("nyt_corpus_without_stopwords_count.txt", 'wb')

for item in word_dict.items():
	if item[1] > 5:
		out_handle_filtered_count.write(item[0] + ' : ' + str(item[1]) + '\n')
	else:
		words_less_frequent.append(item[0])

out_handle_filtered_count.close()

print len(words_less_frequent)

# pattern = re.compile(r'\b(' + r'|'.join(words_less_frequent) + r')\b\s*')

# def remove_less_frequent_words (line):
# 	line = line.strip()
# 	new_line = pattern.sub('', line)
# 	new_line = re.sub(r'\s\s+', ' ', new_line)
# 	return new_line.strip()

# out_handle = open("nyt_corpus_cleaned_for_lda.txt", 'wb')
# line_count = 0
# with open("nyt_corpus_without_stopwords.txt") as infile:
#     for line in infile:
#     	out = remove_less_frequent_words(line)
#         out_handle.write(out + "\n")
#         line_count += 1
#         if line_count % 100000 == 0:
#         	print line_count
#         else:
#         	if line_count % 10000 == 0:
#         		print "."

# out_handle.close()