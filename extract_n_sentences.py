import os
import sys

'''

    Parameters
    ----------
    data_gen: generator | should be of BNC
         a generator object - this is each line read from the input file

    n: int
        number of sentences to process
    Returns
    ----------

    sentences: list of (list of str) | size(length) = n
         each str is a pair consisting of a token and its tag, e.g. "('the', 'DT')"
         each list of str is a sentence
'''
def extract_n_sentences(data_gen, n):
    sen_count = 0
    sentences, sen_so_far = [], []
    while sen_count < n:
        line = next(data_gen)
        #split the line into tags and tokens
        token, tag  = line.strip('\n').split('\t')
        sen_so_far.append('("%s", "%s"),'%(token, tag))
        #marks a complete sentence
        if token.strip() in ['.','?','!']:
            sen_count += 1
            sentences.append(sen_so_far)
            sen_so_far = []
    return sentences

def extract_all_sentences(data_gen, n):
    sen_count = 0
    sentences, sen_so_far = [], []
    for line in data_gen:
        #split the line into tags and tokens
        token, tag  = line.strip('\n').split('\t')
        sen_so_far.append('("%s", "%s"),'%(token, tag))
        #marks a complete sentence
        if token.strip() in ['.','?','!']:
            sen_count += 1
            sentences.append(sen_so_far)
            sen_so_far = []
    return sentences


def main(length=200, input_file='bnc.tagged.withNullArticles.txt', output_file="200_sentences.txt"):
    data_read = (line for line in open(input_file, 'r'))
    first_n = extract_n_sentences(data_read, length)
    #first_n = extract_all_sentences(data_read, length)

    #My python version did not support the "encoding" parameter for the open() function
    #with open("500_tagged_sentences.txt", 'w', encoding= 'utf-8) as f:
    with open(output_file, 'w') as f:
        for line in first_n:
            f.writelines(" ".join(line) + "\n")

#Extract n length sentences from a tagged dataset
if __name__ == "__main__":
    #input_file, output_file, length = sys.argv[1:4]
    #main(int(length), input_file, output_file)
    main()