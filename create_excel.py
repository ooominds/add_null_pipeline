from add_null import extract_all_sentences
from pickle import load
from pandas import DataFrame

def create_excel(input_file, output_file, target_file, sen_markers = ['.','?','!']):
    data_read = (line for line in open("{}.txt".format(input_file), 'r', encoding="utf-8"))
    data_dic = {}
    targets, sourceIDs, sentences = [], [], []
    sen = ""
    cur_code = 2
    for line in data_read:
        #targets_read = (line for line in open("{}.txt".format(target_file), 'r', encoding="utf-8"))
        #for target in targets_read:
        #    reduced_line = line.strip("\n")
        #    reduced_line = reduced_line.replace('("ø", "AT0"),', '')
            #print(reduced_line)
        #    if eval(f'[{reduced_line}]') == eval(f'[{target}]'):
        #        target_code = 1

        line = f"[{line}]"
        eval_line = eval(line)
        if eval_line[0][0] == "CONTEXTA":
            target_code = 1
        elif eval_line[0][0] == "CONTEXTB":
            target_code = -1
        else:
            target_code = 0
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
    data_df.to_excel("output_file.xlsx", index=False)

def main():
    og_file = "may_16_test_null"
    output_file = "sampled_sens"
    input_file = "temp_sens"
    target_file = "source_sen"
    #input_file = "dummy_source"
    #target_file = "dummy_target"

    with open("sources_list.pickle", "rb") as sl:
        sources = load(sl)
    extract_all_sentences(og_file, input_file, sources)
    create_excel(input_file, output_file, target_file)

if __name__ == "__main__":
    main()