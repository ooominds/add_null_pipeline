from nltk import RegexpParser, tree
from os import mkdir
from os.path import exists, join
from subprocess import run, check_output
from pickle import dump, load
from random import sample
from shlex import quote

import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("add_null")
logger.setLevel(level=logging.INFO)


# Creates a parse tree (nltk.Tree) from a given tagged sentence
def apply_grammar(grammar, line):
    cp = RegexpParser(grammar)
    return cp.parse(line)


def add_null(in_file="200_extra_sentences.txt", out_file="nulled_sentences"):
    """
        FUNCTION:
        ---------------
            Creates an "out_file" that is the result of adding null article tags and tokens to the file specified by the path "in_file"
        
        PARAMETERS
        ---------------
            in_file: the location of the input file from which sentences are extracted.
            out_file: the file path for the output

        OUTPUT(s)
        ---------------
            files:
                out_file: A file in the format of the og_file but with null article tags added
            return: None    
    """
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
    data_read = (line for line in open(f"{quote(in_file)}.txt", 'r', encoding="utf-8"))
    with open(f"{quote(out_file)}.txt", 'w', encoding="utf-8") as f:
        for line in data_read:
            #the line is a string in the form of tuples that represent a word and tag pair
            if '\\' in line:
                line = line.replace('\\', '#')
            if '--' in line:
                continue
            line = line[:-2]
            line = f"[{line}]"
            eval_line = eval(line)
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


def extract_all_sentences(cur_file, new_file, sen_markers = ['.','?','!'], keep_source=False):
    """
        FUNCTION:
        ---------------
            Extract sentences from "cur_file" and if "keep_source" = True, the tag for the source file is used to create
            additional files and a temporary folder called "temp_SOURCE_ID" located in the directory the command was run from.
            The additional source files are named after the tag associated with the sentences in the file. For example sentences with a source "XYZ"
            are stored in a file called XYZ.txt which can be found in the temp_SOURCE_ID folder.
        
        PARAMETERS
        ---------------
            cur_file: the location of the input file from which sentences are extracted.
            new_file: the location of a file of sentences extracted from cur_file (to be created).
            sen_markers: The symbols that demarcate the end of a sentence.
            keep_source: Whether to keep the sources (in individual files) and create the temp_SOURCE_ID directory

        OUTPUT(s)
        ---------------
            operations:
                if keep_source:
                    - sources files in a folder called "temp_SOURCE_ID".
                A file is created as referenced by the "new_file" variable.
            files:
                sources_list.pickle: a file that stores a list of all the sources.
                if keep_source:
                    - sources files in a folder called "temp_SOURCE_ID".
                A file is created as referenced by the "new_file" variable.
            return: None

    """
    f = open(f"{quote(new_file)}.txt", 'w')
    f.close()

    data_gen = (line for line in open(f"{quote(cur_file)}.txt", 'r', encoding="utf-8"))
    sen_complete, sentence = False, ""
    print("KEEP SOURCE: ", keep_source)
    sen_list = []
    sources = []
    
    for line in data_gen:
        #split the line into tags and tokens
        #marks a complete sentence
        if keep_source:
            source_id, token, tag  = line.strip('\n').split('\t')
        else:
            token, tag  = line.strip('\n').split('\t')
        token = token.replace("'", "APOST")
        token = token.replace('"', "SPCHMRK")
        if token.strip() in sen_markers:
            sen_complete = True
            sentence += f'("{token}", "{tag}")'
            sen_list.append(sentence)
            sentence = ""
        else:
            sentence += f'("{token}", "{tag}"),'
        if sen_complete:
            if keep_source:
                if not exists(f"temp_SOURCE_ID/{quote(source_id)}.txt"):
                    f = open(f"temp_SOURCE_ID/{quote(source_id)}.txt", 'w')
                    f.close()
                    sources.append(source_id)
                with open(f"temp_SOURCE_ID/{quote(source_id)}.txt", 'a') as nf:
                    for sentence in sen_list:
                        nf.write(f'{sentence},("{quote(source_id)}", "SOURCE") \n')                    
            with open(f"{quote(new_file)}.txt", 'a') as nf:
                if keep_source:
                    for sentence in sen_list:
                        nf.write(f'{sentence},("{quote(source_id)}", "SOURCE") \n')
                else:
                    for sentence in sen_list:
                        nf.write("{}\n".format(sentence))
                sen_complete = False
                sen_list = []
                sentence = ""

    with open(f"{quote(new_file)}.txt", 'a') as nf:
        for sentence in sen_list:
            nf.write(f"{sentence}")
    if keep_source:
        with open("sources_list.pickle", "wb") as sl:
            dump(sources, sl)

def run_bash_comms(n, in_file, new_f, args):
    """
        FUNCTION:
        ---------------
            Runs bash commands (shuf and grep) to obtain a sample of "n" sentences from the file referenced by "in_file"
            if args.con == True then the context of the "n" sampled sentences are also obtained.
            The results are stored in a new file "new_f"
        
        PARAMETERS
        ---------------
            n: number of sentences to sample
            in_file: location of the POS-tagged corpus .txt file stored as sentence per line, each line contains sequences of tuples that form a sentence, the tuples contain a word and POS-tag 
            new_f: location of sampled sentences (and optionally: the context with context tags for each sentence)
            args: parameter arguments that are passed into the function when the code is run from a terminal.

            Relevant parameters are:
                args.in_file: Location of the POS-tagged corpus .txt file stored as sentence per line, each line contains sequences of tuples that form a sentence, the tuples contain a word and POS-tag
                args.con: Whether to sample the context
                args.n: Number of sentences to sample from args.in_file

        OUTPUT(s)
        ---------------
            operations:
            files:
                source_sen.txt: a file that stores all the sampled sentences without their context.
                new_f: .txt file of sampled sentences (and optionally: the context with context tags for each sentence)
            return: None
    """
    if args.sa:
        logger.info(f"Number of sampled sentences: {args.n}")
        check_output(f"shuf -n {n} {quote(in_file)}.txt >> {quote(new_f)}.txt", shell=True)
    elif args.con:
        delim = "$\n"
        print(f"grep AT0 {quote(in_file)}.txt | shuf -n {n} >> source_sen.txt")
        check_output(f"grep AT0 {quote(in_file)}.txt | shuf -n {n} >> source_sen.txt", shell=True)
        if args.c == -1:
            b, a= args.b, args.a
        else:
            b, a = args.c, args.c
        
        sample_sentences = (line for line in open("source_sen.txt", 'r', encoding="utf-8"))
        for line in sample_sentences:
            bash_args = f"{line[:-1]}"
            source_file =f"temp_SOURCE_ID/{line[-17:-14]}.txt"
            with open(source_file, 'r') as f:
                lines_list = f.readlines()
                for i, line in enumerate(lines_list):
                    
                    # assigning context token
                    if bash_args.strip("\n") == line.strip("\n"):
                        target_line = '("TARGET", "TARGET"),' + line
                        if i-b > 0:
                            span_b = ['("CONTEXTB", "CONTEXTB"),' + line for line in lines_list[i-b:i]]
                        else:
                            span_b = ['("CONTEXTB", "CONTEXTB"),' + line for line in lines_list[0:i]]
                        if i+a < len(lines_list):
                            span_a = ['("CONTEXTA", "CONTEXTA"),' + line for line in lines_list[i+1:i+a+1]]
                        else:
                            span_a = ['("CONTEXTA", "CONTEXTA"),' + line for line in lines_list[i:len(lines_list)-1]]
                        span_b.append(target_line)
                        span = span_b + span_a
                        with open(f"{new_f}.txt", 'a') as nf:
                            for line in span:
                                nf.write(line)
                        break

def random_sample_range(args):
    """
        FUNCTION:
        ---------------
            From the sentences found in args.in_file, a random sample of size args.n sentences is taken from several source files, context is added to each depending on
            the range specified by either args.c or a combination of args.b and args.a.

        PARAMETERS
        ---------------
            args: parameter arguments that are passed into the function when the code is run from a terminal.

            Relevant parameters are:
                args.in_file: Location of the POS-tagged corpus .txt file stored as sentence per line, each line contains sequences of tuples that form a sentence, the tuples contain a word and POS-tag
                args.so: Whether the sources of each sentence is being stored or not
                args.n: Number of sentences to sample from args.in_file
        
        OUTPUT(s)
        ---------------
            operations: reassigns the value of args.in_file to a new file (new_f) that contains sampled sentences with context tags
            files:
            return: None
    """
    from math import ceil 
    if args.so:
        logger.info(f"Number of sampled sentences: {args.n} \n sentences before: {args.b} \n sentence after: {args.a}")
        new_f = f"{quote(args.in_file)}_sr_{args.n}"
        f = open(f"{quote(new_f)}.txt", "w")
        f.close()

        # Remove the file that stores the sampled sentences each run
        check_output("truncate -s 0 source_sen.txt", shell=True)
        # Remove the file that stores the sampled sentences and their context each run
        check_output(f"truncate -s 0 {quote(new_f)}.txt", shell=True)

        # Get the context of sampled sentences
        run_bash_comms(args.n, args.in_file, new_f, args)
    else:
        new_f = f"{quote(args.in_file)}_sa_{args.n}"
        f = open(f"{quote(new_f)}.txt", "w")
        f.close()
        run_bash_comms(args.n, args.in_file, new_f, args)
    args.in_file = new_f

# Maybe make a tagger later
def add_tags(in_file):
    raise NotImplementedError
    #from nltk import tag, word_tokenize
    #txt_file = (line for line in open(f"{quote(in_file)}.txt", 'r', encoding="utf-8"))
    #for line in txt_file:
    #    sen_tokenized = word_tokenize(line)
    #    sen_tagged = tag.pos_tag(sen_tokenized, tagset="claws5")

def main():

    # Various arguments that are passed into the code
    parser = argparse.ArgumentParser()
    parser.add_argument('og_file', type=str, help='INPUT: location of the POS-tagged corpus file, A .txt file with two columns, one for a word and the other for the POS-tag')
    parser.add_argument('in_file', type=str, help='CREATED: location of the POS-tagged corpus .txt file stored as sentence per line, each line contains sequences of tuples that form a sentence, the tuples contain a word and POS-tag')
    parser.add_argument('out_file', type=str, help='CREATED: location of the output file. A .txt file with two columns, one for a word and the other for the POS-tag (with null article tags)')
    
    parser.add_argument('-sa', action='store_true', help='Sample random sentences from the in_file')
    parser.add_argument('-con', action='store_true', help='Sample random sentences from the in_file as well as r sentence before and l sentences after')
    parser.add_argument('-so', action='store_true', help='Give the source ID of this sentence')

    parser.add_argument('-se', type=int, default=500, help='a random seed')
    parser.add_argument('-n', type=int, default=500, help='number of sentences to sample (requires sample flag to be set)')
    parser.add_argument('-c', type=int, default=-1, help='number of sentences before and after the sampled sentence to include')
    parser.add_argument('-b', type=int, default=3, help='number of sentences before a sampled sentence to include')
    parser.add_argument('-a', type=int, default=3, help='number of sentences after a sampled sentence to include')

    args = parser.parse_args()

    logger.info(f"Location of original POS-tagged file: {quote(args.og_file)}")
    logger.info(f"Location of POS-tagged file as nltk-compatible sentences (per line): {quote(args.in_file)}")
    logger.info(f"POS-tagged file with null-articles: {quote(args.out_file)}")
    if exists(f"{quote(args.in_file)}.txt"):
        logger.info(f"{quote(args.in_file)} already exists, skipping sentence file creation step")
    else:
        if args.so:
            if not exists("temp_SOURCE_ID"):
                mkdir("temp_SOURCE_ID")            
            extract_all_sentences(args.og_file, args.in_file, keep_source=True)
        else:
            extract_all_sentences(args.og_file, args.in_file)

    if args.sa or args.con:
        random_sample_range(args)

    add_null(args.in_file, args.out_file)

if __name__ == "__main__":
    main()



