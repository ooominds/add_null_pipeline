


PY_VERSION =  "3" # python version being used 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     PARAMETERS FOR clean_bnc_xml.py
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

outfyes= #type=str, help=INPUT: path for creating written sentences per line file from BNC with punctuation
outfno= #type=str, help=INPUT: path for creating written sentences per line file from BNC without punctuation
outf= #type=str,help=INPUT: path for creating tagged written sentences
bnc_root= #type=str, help=INPUT: path to the directory with the BNC text files

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     PARAMETERS FOR add_null.py
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

og_file =   #type=str, help=INPUT: location of the POS-tagged corpus file, A .txt file with two columns, one for a word and the other for the POS-tag
in_file=    #type=str, helpCREATED: location of the POS-tagged corpus .txt file stored as sentence per line, each line contains sequences of tuples that form a sentence, the tuples contain a word and POS-tag
out_file=   #type=str, help=CREATED: location of the output file. A .txt file with two columns, one for a word and the other for the POS-tag (with null article tags)

sa= False   #action='store_true', help=Sample random sentences from the in_file
con= True   #action='store_true', help=Sample random sentences from the in_file as well as r sentence before and l sentences after
so= True    #action='store_true', help=Give the source ID of this sentence

se= 10  #type=int, default=10, help=a random seed - NOT IMPLEMENTED YET
n= 500  #type=int, default=500, help=number of sentences to sample (requires sample flag to be set)
c= -1   #type=int, default=-1, help=number of sentences before and after the sampled sentence to include
b= 3    #type=int, default=3, help=number of sentences before a sampled sentence to include
a= 3    #type=int, default=3, help=number of sentences after a sampled sentence to include


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     PARAMETERS FOR create_excel.py
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
