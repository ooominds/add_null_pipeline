#import sys
from numpy import array, savetxt, transpose
from nltk import RegexpParser, tree
from os import system
from sys import argv
import logging
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
                    nf.write("[{}] \n".format(sentence))
                sen_count = 0
                sen_list = []
                sentence = ""
    with open("{}.txt".format(new_file), 'a') as nf:
        for sentence in sen_list:
            nf.write("{} \n".format(sentence))

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
    
    parser.add_argument('-sa', type=bool, default=True, help='A random sample from the in_file a specific number of sentences')
    parser.add_argument('-se', type=int, default=500, help='a random seed')
    parser.add_argument('-n', type=int, default=500, help='number of sentences to sample (requires sample flag to be set)')

    args = parser.parse_args()

    logger.info("Location of original POS-tagged file: {}".format(args.og_file))
    logger.info("Location of POS-tagged file as nltk-compatible sentences (per line): {}".format(args.in_file))
    logger.info("POS-tagged file with null-articles: {}".format(args.out_file))
    
    extract_all_sentences(args.og_file, args.in_file)
    # Next use the following command in the Linux terminal: shuf -n 500 [infile].txt > [infile]_[n].txt
    if args.sa:
        logger.info("Number of smapled sentences: {}".format(args.n))
        system("shuf -n {} {}.txt > {}_{}.txt".format(args.n, args.in_file, args.in_file, args.n))
        args.in_file = "{}_{}".format(args.in_file, args.n)
    add_null(args.in_file, args.out_file)

if __name__ == "__main__":
    #infile, outfile = sys.argv[1:3]
    #main(infile, outfile)
    main()



