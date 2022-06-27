from os import sep


PY_VERSION =  "3" # python version being used 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     PARAMETERS FOR clean_bnc_xml.py
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

outfyes= f"BNC_XML_2007{sep}june_25{sep}written_sentence_per_line_with_punctuations" # .txt #type=str, help=CREATED: path for creating written sentences per line file from BNC with punctuation # example: "../processed_data/written_sentence_per_line_with_punctuations.txt
outfno= f"BNC_XML_2007{sep}june_25{sep}written_sentence_per_line_without_punctuations" # .txt #type=str, help=CREATED: path for creating written sentences per line file from BNC without punctuation
outf= f"BNC_XML_2007{sep}june_25{sep}written_sentence_tagged" # .txt #type=str,help=CREATED: path for creating tagged written sentences
bnc_root= f"" #type=str, help=INPUT: path to the directory with the BNC text files

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     PARAMETERS FOR add_null.py
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#og_file =  outfyes #type=str, help=INPUT: location of the POS-tagged corpus file, A .txt file with two columns, one for a word and the other for the POS-tag
og_file =  f"BNC_XML_2007{sep}sst_c5" #type=str, help=INPUT: location of the POS-tagged corpus file, A .txt file with two columns, one for a word and the other for the POS-tag
an_in_file=   f"BNC_XML_2007{sep}june_25{sep}pipeline_in_file" #type=str, help =CREATED: location of the POS-tagged corpus .txt file stored as sentence per line, each line contains sequences of tuples that form a sentence, the tuples contain a word and POS-tag
an_out_file=  f"pipeline_test" #type=str, help=CREATED: location of the output file. A .txt file with two columns, one for a word and the other for the POS-tag (with null article tags)
ta = f"source_sen" # type=str, help=CREATED: location of a file that includes all the sampled sentences, one per line.
sl = f"sources_list"


sa= False   #action='store_true', help=Sample random sentences from the in_file
con= True   #action='store_true', help=Sample random sentences from the in_file as well as r sentence before and l sentences after
so= True    #action='store_true', help= Give the source ID of this sentence - note that this requires a an og_file with soruce ids

se= 10  #type=int, default=10, help=a random seed - NOT IMPLEMENTED YET
n= 500  #type=int, default=500, help=number of sentences to sample (requires sample flag to be set)
c= -1   #type=int, default=-1, help=number of sentences before and after the sampled sentence to include
b= 3    #type=int, default=3, help=number of sentences before a sampled sentence to include
a= 3    #type=int, default=3, help=number of sentences after a sampled sentence to include


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     PARAMETERS FOR create_excel.py
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


ce_in_file = an_out_file #type=str, help = CREATED: location of the POS-tagged corpus .txt file stored as sentence per line, each line contains sequences of tuples that form a sentence, the tuples contain a word and POS-tag
ce_out_file = f"output_excel" #type =sen, help='CREATED: location of the output file. A .xlsx file with rows for each sentence, rows where the sentence is a context sentence will have multiple sentences in the "sentence" column'
ta = ta #type=str, help= INPUT: location of a file that includes all the sampled sentences, one per line.
sl = sl #type =str, help=INPUT: location of the .pkl that stores the list of source IDs
