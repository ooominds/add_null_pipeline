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

from nltk.corpus.reader.bnc import BNCCorpusReader

# Instantiate the reader like this
bnc = BNCCorpusReader(root='../BNC_XML_2007/download/Texts', fileids=r'[A-K]/\w*/\w*\.xml')

spoken = []
written = []
for fileid in bnc.fileids():
    if '<stext' in bnc.raw(fileid):
        spoken.append(fileid)
    else:
        written.append(fileid)

outfyes = open('../processed_data/written_sentence_per_line_with_punctuations.txt', 'w')
outfno = open('../processed_data/written_sentence_per_line_without_punctuations.txt', 'w')
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

outf = open('../processed_data/written_sentence_tagged.txt', 'w')
outf.write('SOURCE_ID\tWORD\tTAG\n')
for fileid in written:
    item_id = fileid.split('.')[0].split('/')[2]
    for sentence in bnc.tagged_sents(fileid, c5=False):
        for word, tag in sentence:
            outf.write('%s\t%s\t%s\n' % (item_id, word, tag))
outf.close()

