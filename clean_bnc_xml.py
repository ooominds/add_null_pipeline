# -*- coding: utf-8 -*-

# P Milin; 06/05/2022


# # This runs for an interactive BlueBEAR session:
# ssh milinp@bluebear.bham.ac.uk
# module load slurm-interactive
# fisbatch_tmux --nodes 1 --ntasks 1 --time 02:00:00 --mem=60GB --qos=divjakd
# 
# cd /rds/projects/d/divjakd-ooo-minds/corpora/BNC_OLD/scripts/
# conda activate petar
# python


import re
from shlex import quote
import argparse
from nltk.corpus.reader.bnc import BNCCorpusReader

# Instantiate the reader like this
def clean_bnc(outfyes_path = "../processed_data/written_sentence_per_line_with_punctuationst", outfno_path = "../processed_data/written_sentence_per_line_without_punctuations", outf_path="../processed_data/written_sentence_tagged",
              bnc_root = "../BNC_XML_2007/download/Texts"):
    bnc = BNCCorpusReader(root=bnc_root, fileids=r'[A-K]/\w*/\w*\.xml')

    spoken = []
    written = []
    for fileid in bnc.fileids():
        if '<stext' in bnc.raw(fileid):
            spoken.append(fileid)
        else:
            written.append(fileid)

    outfyes = open(quote(f"{outfyes_path}.txt"), 'w')
    outfno = open(quote(f"{outfno_path}.txt"), 'w')
    for fileid in written:
        item_id = fileid.split('.')[0].split('/')[2]
        for sentence in bnc.sents(fileid):
            sentence = ' '.join(sentence)
            sentence = re.sub(r'\s+([;:,.?!\'"\)\(\]\[])', r'\1', sentence)
            outfyes.write('%s\t%s\n' % (item_id, sentence))
            sentence = re.sub(r'[^A-Za-z0-9\'\ ]+', '', sentence)
            outfno.write('%s\t%s\n' % (item_id, sentence))
    outfyes.close()
    outfno.close()

    outf = open(quote(f"{outf_path}.txt"), 'w')
    outf.write('SOURCE_ID\tWORD\tTAG\n')
    for fileid in written:
        item_id = fileid.split('.')[0].split('/')[2]
        for sentence in bnc.tagged_sents(fileid, c5=False):
            for word, tag in sentence:
                outf.write('%s\t%s\t%s\n' % (item_id, word, tag))
    outf.close()

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("outfyes", type=str, help="INPUT: path for creating written sentences per line file from BNC with punctuation")
    parser.add_argument("outfno", type=str, help="INPUT: path for creating written sentences per line file from BNC without punctuation")
    parser.add_argument("outf", type=str,help="INPUT: path for creating tagged written sentences")
    parser.add_argument("bnc_root", type=str, help="INPUT: path to the directory with the BNC text files")
    
    args = parser.parse_args()
    clean_bnc(args.outfyes, args.outfno, args.outf, args.bnc_root)


if __name__ == "__main__":
    run()

