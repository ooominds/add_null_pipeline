




### Example commands:

`>python3 add_null.py BNC_XML_2007/wst_c5 BNC_XML_2007/sen_wst_c5 test_null`

Create a file ("_test_null.txt_") that is the same as "_wst_c5.txt_" but with null-article tags added.
An intemermediate file "BNC_XML_2007/sen_wst_c5 test_null.txt" is also created, this has the word/token tag pairs that make up the columns of "_wst_c5.txt_" as sentences that each occupy a line each.

`>python3 add_null.py BNC_XML_2007/wst_c5 BNC_XML_2007/sen_wst_c5 test_null -sa -n 500`

Create a file ("_test_null.txt_") that has **500 sentences sampled** from "_wst_c5.txt_" but with null-article tags added.
An intemermediate file "BNC_XML_2007/sen_wst_c5 test_null.txt" is also created, this has the word/token tag pairs that make up the columns of "_wst_c5.txt_" as sentences that each occupy a line each.

`>python3 add_null.py BNC_XML_2007/wst_c5 BNC_XML_2007/sen_wst_c5 test_null -sr -n 200 -b 4 -a 5`

Create a file ("_test_null.txt_") that has **200 sentences each with the previous 4 sentences and following 5 sentences sampled** from "_wst_c5.txt_" but with null-article tags added. An intemermediate file "BNC_XML_2007/sen_wst_c5 test_null.txt" is also created, this has the word/token tag pairs that make up the columns of "_wst_c5.txt_" as sentences that each occupy a line each.


## Parameters

og_file
: location of the POS-tagged corpus file, A .txt file with two columns, one for a word and the other for the POS-tag
This is the first argument, since it is a positional parameter you do not need to name the parameter. **do not** include the file extension (this should be ".txt") when filling out this parameter.
This file should be formatted in two columns, the left column should be words while the right-column should be part of speech tags.
Separate these two columns with a tab ("\t") character.

in_file
:
This is the second argument, **do not** include the file extension (this should be ".txt") when filling out this parameter.
This sets the file path to the location of the POS-tagged corpus .txt file stored as sentence per line, each line contains sequences of tuples that form a sentence, the tuples contain a word and POS-tag.

out_file
:
This is the third argument, **do not** include the file extension (this should be ".txt") when filling out this parameter.
location of the output file. A .txt file with two columns, one for a word and the other for the POS-tag (with null article tags)



## Flags

These are all optional flags that manage the sampling process.

-sa
:   Sample random individual sentences from the in_file, this is a flag and does not take any values, by default this is False

-sr
:   Sample random sequences of sentences from the in_file, this is a flag and does not take any values, by default this is False

-se
:  **This has not been implemented yet**: this sets the random seed for the sampling.

-n
:   The number of individual sentences to sample, by default this is **500**

-c
:   The number of sentences before and after the sampled sentence to include (this is only necessary to set if the sr flag is also set). By default this is **3** so if it is not set and -sr is True, the three previous and three following sentences of a randomly sampled sentence will be added to the out_file.

-b
:   The number of sentences before the sampled sentence to include, this is only necessary to set if the sr flag is also set and is unecessary to set if the -c flag is set. By default this is **3** so if it is not set and -sr is True, the three previous sentences of a randomly sampled sentence will be added to the out_file.

-a
:   The number of sentences after the sampled sentence to include (this is only necessary to set if the sr flag is also set). By default this is **3** so if it is not set and -sr is True, the three following sentences of a randomly sampled sentence will be added to the out_file.