#This cell loads the Penn Treebank corpus from nltk into a list variable named penn_treebank.

#No need to install nltk in google colab since it is preloaded in the environments.
#!pip install nltk
import nltk

#Ensure that the treebank corpus is downloaded
nltk.download('bnc')

#Load the treebank corpus class
from nltk.corpus import bnc

#Now we iterate over all samples from the corpus (the fileids - that are equivalent to sentences) 
#and retrieve the word and the pre-labeled PoS tag. This will be added as a list of tuples with 
#a list of words and a list of their respective PoS tags (in the same order).
penn_treebank = []
for fileid in treebank.fileids():
  tokens = []
  tags = []
  for word, tag in treebank.tagged_words(fileid):
    tokens.append(word)
    tags.append(tag)
  penn_treebank.append((tokens, tags))

#This cell loads the Universal Dependecies Treekbank corpus. It'll download all the packages, but we'll only use the GUM
#english package. We'll also install the conllu package, that was developed to parse data in the conLLu format, a 
#format common of linguistic annotated files. We'll also have a list variable, but now named ud_treebank.

#Install conllu package, download the UD Treebanks corpus and unpack it.
!pip install conllu
!wget https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3105/ud-treebanks-v2.5.tgz
!tar zxf ud-treebanks-v2.5.tgz

#The imports needed to open and parse (interpret) the conllu file. At the end we'll have a list of dicts.
from io import open
from conllu import parse_incr

#Open the file and load the sentences to a list.
data_file = open("ud-treebanks-v2.5/UD_English-GUM/en_gum-ud-train.conllu", "r", encoding="utf-8")
ud_files = []
for tokenlist in parse_incr(data_file):
    ud_files.append(tokenlist)

#Now we iterate over all samples from the corpus and retrieve the word and the pre-labeled PoS tag (upostag). This will 
#be added as a list of tuples with a list of words and a list of their respective PoS tags (in the same order).
ud_treebank = []
for sentence in ud_files:
  tokens = []
  tags = []
  for token in sentence:
    tokens.append(token['form'])
    tags.append(token['upostag'])
  ud_treebank.append((tokens, tags))

  #Regex module for checking alphanumeric values.
import re
def extract_features(sentence, index):
  return {
      'word':sentence[index],
      'is_first':index==0,
      'is_last':index ==len(sentence)-1,
      'is_capitalized':sentence[index][0].upper() == sentence[index][0],
      'is_all_caps': sentence[index].upper() == sentence[index],
      'is_all_lower': sentence[index].lower() == sentence[index],
      'is_alphanumeric': int(bool((re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])',sentence[index])))),
      'prefix-1':sentence[index][0],
      'prefix-2':sentence[index][:2],
      'prefix-3':sentence[index][:3],
      'prefix-3':sentence[index][:4],
      'suffix-1':sentence[index][-1],
      'suffix-2':sentence[index][-2:],
      'suffix-3':sentence[index][-3:],
      'suffix-3':sentence[index][-4:],
      'prev_word':'' if index == 0 else sentence[index-1],
      'next_word':'' if index < len(sentence) else sentence[index+1],
      'has_hyphen': '-' in sentence[index],
      'is_numeric': sentence[index].isdigit(),
      'capitals_inside': sentence[index][1:].lower() != sentence[index][1:]
  }


  #Ater defining the extract_features, we define a simple function to transform our data in a more 'datasetish' format.
#This function returns the data as two lists, one of Dicts of features and the other with the labels.
def transform_to_dataset(tagged_sentences):
  X, y = [], []
  for sentence, tags in tagged_sentences:
    sent_word_features, sent_tags = [],[]
    for index in range(len(sentence)):
        sent_word_features.append(extract_features(sentence, index)),
        sent_tags.append(tags[index])
    X.append(sent_word_features)
    y.append(sent_tags)
  return X, y

#We divide the set BEFORE encoding. Why? To have full sentences in training/testing sets. When we encode, we do not encode
#a sentence, but its words instead.

#First, for the Penn treebank.
penn_train_size = int(0.8*len(penn_treebank))
penn_training = penn_treebank[:penn_train_size]
penn_testing = penn_treebank[penn_train_size:]
X_penn_train, y_penn_train = transform_to_dataset(penn_training)
X_penn_test, y_penn_test = transform_to_dataset(penn_testing)

#Then, for UD Treebank.
ud_train_size = int(0.8*len(ud_treebank))
ud_training = ud_treebank[:ud_train_size]
ud_testing = ud_treebank[ud_train_size:]
X_ud_train, y_ud_train = transform_to_dataset(ud_training)
X_ud_test, y_ud_test = transform_to_dataset(ud_testing)

#Third step, vectorize datasets. For that we use sklearn DictVectorizer
#WARNING


#Ignoring some warnings for the sake of readability.
import warnings
warnings.filterwarnings('ignore')

#First, install sklearn_crfsuite, as it is not preloaded into Colab. 
!pip install sklearn_crfsuite
from sklearn_crfsuite import CRF

#This loads the model. Specifics are: 
#algorithm: methodology used to check if results are improving. Default is lbfgs (gradient descent).
#c1 and c2:  coefficients used for regularization.
#max_iterations: max number of iterations (DUH!)
#all_possible_transitions: since crf creates a "network", of probability transition states,
#this option allows it to map even "connections" not present in the data.
penn_crf = CRF(
    algorithm='lbfgs',
    c1=0.01,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)
#The fit method is the default name used by Machine Learning algorithms to start training.
print("Started training on Penn Treebank corpus!")
penn_crf.fit(X_penn_train, y_penn_train)
print("Finished training on Penn Treebank corpus!")

#Same for UD
ud_crf = CRF(
    algorithm='lbfgs',
    c1=0.01,
    c2=0.1,
    max_iterations=100,
    all_possible_transitions=True
)
print("Started training on UD corpus!")
ud_crf.fit(X_ud_train, y_ud_train)
print("Finished training on UD corpus!")