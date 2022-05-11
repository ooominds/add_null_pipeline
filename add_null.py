#import sys
from numpy import array, savetxt, transpose
from nltk import RegexpParser, tree
from os import system
from os.path import exists
from sys import argv
import logging
from subprocess import check_output
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("add_null")
logger.setLevel(level=logging.INFO)


# Creates a parse tree (nltk.Tree) from a given tagged sentence
def apply_grammar(grammar, line):
    cp = RegexpParser(grammar)
    return cp.parse(line)


def add_null(infile="200_extra_sentences.txt", outfile="nulled_sentences",  nphrase_file='rndm'):
    # Grammar rules were arrived at from the noun-phrase finding,
    # Strictly speaking: not all of them are necessary for the naive null-tagger
    grammar = r"""
            GEN: {<POS|DPS|DT0><NN.*|VVB-NN.*>+}
            NPR1: {<AT0.*|DT0><|AJ.*>*<AJ0.*><NN.*><PRP.*><AT0.*><NN.*>}
            NullNPR1: {<AJ0.*><NN.*><PRP.*><AT0.*><NN.*>+}
            NPR2: {<AT.*|DT0><ORD><CRD>*<NN.*|VVB-NN.*>+}
            NullNPR2: {<ORD><CRD>*<NN.*|VVB-NN.*>+}
            NPR3: {<AT.*|DT0><ORD>*<CRD><NN.*|VVB-NN.*>+}
            NullNPR3: {<ORD>*<CRD><NN.*|VVB-NN.*>+}
            NPR4: {<AT.*|DT0><AJ.*|PP\$|DP.*|AV.*|>*<NN.*|VVB-NN.*|NP0-NN.*>+}
            NullNPR4: {<AJ.*>*<NN.*|VVB-NN.*|NP0-NN.*>+}
            """
    data_read = (line for line in open("{}.txt".format(infile), 'r', encoding="utf-8"))
    with open("{}.txt".format(outfile), 'w', encoding="utf-8") as f:
        nf = open("{}.txt".format(nphrase_file), 'w', encoding="utf-8")
        for line in data_read:
            #the line is a string in the form of tuples that represent a word and tag pair
            if '\\' in line:
                line = line.replace('\\', '#')
            line = "[{}]".format(line)
            eval_line = eval(line)
            #print(eval_line)
            #to store a sentence
            sen, tagged_words = [], []
            noun_chunk = apply_grammar(grammar, eval_line)
            #noun_chunk is a nltk Tree
            for n in noun_chunk:
                n_phrase = str(n)
                sen.append(n_phrase)

                #tags that had a rule applied have to be treated slightly differently
                if isinstance(n, tree.Tree):
                    if n_phrase.find("NullNPR") > 0:
                        #add a null tag to the beginning of the noun-phrase
                        tagged_words += [('ø', 'AT0')] + [w for w in n.leaves()]
                    else:
                        tagged_words += [w for w in n.leaves()]
                else:
                    tagged_words.append(n)
            for pair in tagged_words:
                f.write("{}\t{}\n".format(pair[0], pair[1]))
            nf.writelines(' '.join(sen))

        #output_arr = transpose(array([array([w for w,t in tagged_words]), array([t for w,t in tagged_words])]))
        #savetxt("%s.txt"%(outfile), output_arr, delimiter = "\t", encoding="utf-8", fmt='%s')
        #f.writelines(' '.join([tw[0] for tw in tagged_words]) + "\n")
        nf.close()

def extract_all_sentences(cur_file, new_file):
    f = open("{}.txt".format(new_file), 'w')
    f.close()

    data_gen = (line for line in open("{}.txt".format(cur_file), 'r', encoding="utf-8"))
    sen_count, sentence = 0, ""
    sen_list = []
    for line in data_gen:
        #split the line into tags and tokens
        #marks a complete sentence
        token, tag  = line.strip('\n').split('\t')
        token = token.replace("'", "")
        token = token.replace("\"", "#")
        if token.strip() in ['.','?','!']:
            sen_count += 1
            sentence += '("{}", "{}")'.format(token, tag)
            sen_list.append(sentence)
            sentence = ""
        else:
            sentence += '("{}", "{}"),'.format(token, tag)
        if sen_count == 200:
            with open("{}.txt".format(new_file), 'a') as nf:
                for sentence in sen_list:
                    nf.write("{}\n".format(sentence))
                sen_count = 0
                sen_list = []
                sentence = ""
    with open("{}.txt".format(new_file), 'a') as nf:
        for sentence in sen_list:
            nf.write("{}".format(sentence))

# Maybe make a tagger later
def add_tags(infile):
    from nltk import tag, word_tokenize
    txt_file = (line for line in open("{}.txt".format(infile), 'r', encoding="utf-8"))
    for line in txt_file:
        sen_tokenized = word_tokenize(line)
        sen_tagged = tag.pos_tag(sen_tokenized, tagset="claws5")

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('og_file', type=str, help='location of the POS-tagged corpus file, A .txt file with two columns, one for a word and the other for the POS-tag')
    parser.add_argument('in_file', type=str, help='location of the POS-tagged corpus .txt file stored as sentence per line, each line contains sequences of tuples that form a sentence, the tuples contain a word and POS-tag')
    parser.add_argument('out_file', type=str, help='location of the output file. A .txt file with two columns, one for a word and the other for the POS-tag (with null article tags)')
    
    parser.add_argument('-sa', action='store_true', help='Sample random sentences from the in_file')
    parser.add_argument('-sr', action='store_true', help='Sample random sentences from the in_file as well as r sentence before and l sentences after')
    parser.add_argument('-se', type=int, default=500, help='a random seed')
    parser.add_argument('-n', type=int, default=500, help='number of sentences to sample (requires sample flag to be set)')
    parser.add_argument('-c', type=int, default=-1, help='number of sentences before and after the sampled sentence to include')
    parser.add_argument('-b', type=int, default=3, help='number of sentences before a sampled sentence to include')
    parser.add_argument('-a', type=int, default=3, help='number of sentences after a sampled sentence to include')

    args = parser.parse_args()

    logger.info("Location of original POS-tagged file: {}".format(args.og_file))
    logger.info("Location of POS-tagged file as nltk-compatible sentences (per line): {}".format(args.in_file))
    logger.info("POS-tagged file with null-articles: {}".format(args.out_file))
    
    if not exists("{}.txt".format(args.in_file)):
        extract_all_sentences(args.og_file, args.in_file)
    else:
        logger.info("{} already exists, skipping sentence file creation step".format(args.in_file))
    # Next use the following command in the Linux terminal: shuf -n 500 [infile].txt > [infile]_[n].txt
    if args.sa:
        logger.info("Number of smapled sentences: {}".format(args.n))
        system("shuf -n {} {}.txt > {}_sa_{}.txt".format(args.n, args.in_file, args.in_file, args.n))
        args.in_file = "{}_sa_{}".format(args.in_file, args.n)

    elif args.sr:
        if args.c == -1:
            logger.info("Number of smapled sentences: {} \n sentences before: {} \n sentence after: {}".format(args.n, args.b, args.a))
            system("shuf -n {} {}.txt | xargs -I % grep -F -B {} -A {} % {}.txt > {}_sr_{}.txt".format(args.n, args.in_file, args.b, args.a, args.in_file, args.in_file, args.n))
            args.in_file = "{}_sr_{}".format(args.in_file, args.n)
        else:
            logger.info("Number of smapled sentences: {} \n sentences before: {} \n sentence after: {}".format(args.n, args.c, args.c))
            #p = check_output("shuf -n {} {}.txt | xargs -I % grep -C {} % {}.txt".format(args.n, args.in_file, args.c, args.in_file), shell=True)
            #print(p)
            system("shuf -n {} {}.txt | xargs -I % grep -F -C {} % {}.txt > {}_sr_{}.txt".format(args.n, args.in_file, args.c, args.in_file, args.in_file, args.n))
            args.in_file = "{}_sr_{}".format(args.in_file, args.n)

    add_null(args.in_file, args.out_file)

if __name__ == "__main__":
    #shuf stagged_c5_500.txt -n 5 | grep -B 6 stagged_c5_500.txt
    #shuf stagged_c5_500.txt -n 2 | xargs -I % grep -B 1 -A 1 % stagged_c5_500.txt
    #infile, outfile = sys.argv[1:3]
    #main(infile, outfile)
    main()



