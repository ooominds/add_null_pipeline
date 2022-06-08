from add_null import extract_all_sentences
from random import shuffle
from pickle import load
from pandas import DataFrame
import argparse

def add_article_tag(line):
    """
        FUNCTION:
        ---------------
            adds a marker to a random article in a line (sentence)
        
        PARAMETERS
        ---------------
            line: a sentence that will have one of its null articles marked

        OUTPUT(s)
        ---------------
            a line with a marked null article
    """
    articles = []
    for i, double in enumerate(line):
        if double[1] == "AT0":
            articles.append(i)
    shuffle(articles)
    chosen_article = articles[0]
    line[chosen_article] = (f"_{line[chosen_article][0]}_", line[chosen_article][1])
    return line

def create_excel(input_file, output_file, target_file="source_sen", sen_markers = ['.','?','!']):
    """
        FUNCTION:
        ---------------
            create an excel file with sampled sentences surrounded by their context sentences.
        
        PARAMETERS
        ---------------
            input_file:
                a .txt file created by the "extract_all_sentences" function
            output_file:
                path of the file the output should be written to
            target_file:
                path to the location of the file with the target sentences (default as source_sen.txt)
        OUTPUT(s)
        ---------------
    """
    data_read = (line for line in open("{}.txt".format(input_file), 'r', encoding="utf-8"))
    data_dic = {}
    targets, sourceIDs, sentences = [], [], []
    sen = ""
    cur_code = 2
    for line in data_read:
        line = f"[{line}]"
        eval_line = eval(line)
        if eval_line[0][0] == "CONTEXTA":
            target_code = 1
        elif eval_line[0][0] == "CONTEXTB":
            target_code = -1
        else:
            target_code = 0
            eval_line = add_article_tag(eval_line)
        if cur_code != target_code and cur_code != 2:
            targets.append(cur_code)
            sourceIDs.append(sourceID)
            sentences.append(sen)
            sen = ""

        sourceID = eval_line[-1][0]
        for sen_token in eval_line[1:-1]:
            word, tag = sen_token
            if "APOST" in word:
                word = word.replace("APOST", "'")
            if "SPCHMRK" in word:
                word = word.replace("SPCHMRK", '"')
            if tag in ["PUN", "POS"]:
                sen += "" + word
            else:
                sen += " " + word
        cur_code = target_code
        sen += "; "

    data_dic["TARGET"] = targets
    data_dic["ID"] = sourceIDs
    data_dic["Sentence"] = sentences
    data_df = DataFrame(data_dic)
    data_df.to_excel(f"{output_file}.xlsx", index=False)

def main():
    parser = argparse.ArgumentParser()

    # default is output.txt
    parser.add_argument('-inpt', type=str, help='INPUT: location of the POS-tagged .txt file with null tags added - stored as two coumns, one for teh tag and the other for the token')

    # new_output
    parser.add_argument('-otpt', type=str, help='CREATED: location of the output file. A .xlsx file with rows for each sentence, rows where the sentence is a context sentence will have multiple sentences in the "sentence" column')

    # source_sen
    parser.add_argument('-ta', type=str, help='INPUT: location of the POS-tagged corpus file, A .txt file with two columns, one for a word and the other for the POS-tag')
    
    # sources_list.pickle
    parser.add_argument('-sl', type=str, help='INPUT: location of the .pkl that stores the list of sources')

    args = parser.parse_args()
    output_file = "output"
    aux_file = "temp_sens"
    target_file = "source_sen"

    with open(f"{args.sl}.pickle", "rb") as sl:
        sources = load(sl)
    extract_all_sentences(args.inpt, aux_file, sources)
    create_excel(aux_file, args.otpt, args.ta)

if __name__ == "__main__":
    main()