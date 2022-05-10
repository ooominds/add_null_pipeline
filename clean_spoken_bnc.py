import os
import sys
import pandas as pd

def change_tagset(csv_df):
    tagset_rep = {"AJ0": ["JJ", "JK"],
                  "AJC": ["JJR"],
                  "AJS": ["JJT"],
                  "AT0": ["AT", "AT1"],
                  "AV0": ["RA", "REX", "RG", "RGA", "RGR", "RGT", "RL", "RP", "RPK", "RR", "RRR","RRT", "RT"],
                  "AVQ": ["RGQ", "RGQV","RRQ", "RRQV"],
                  "CJC": ["CC", "CCB", "CSN"],
                  "CJS": ["CS", "CSA", "CSA", "CSW"],
                  "CJT": ["CST"],
                  "CRD": ["MC", "MC-MC", "MC1", "MC2", "MF", "NNO", "NNO2"],
                  "DPS": ["APPGE"],
                  "DT0": ["DB", "DD1", "DD2","DD","DB2","DAT","DAR", "DA2T","DA2R","DA2", "DA1","DA"],
                  "DTQ": ["DDQ", "DDQGE", "DDQV"],
                  "EX0": ["EX"],
                  "ITJ": ["UH"],
                  "NN0": ["NN", "NNJ", "NNL", "NNU1","NNU2",],
                  "NN1": ["NN1", "NNL1"],
                  "NN2": ["NN2","NNJ2", "NNL2"],
                  "NP0": ["NP", "NP1", "NP2", "NPD1", "NPD2", "NPM1", "NPM2", "NNSA", "NNSB", "NNT1", "NNT2"],
                  "ORD": ["MD"],
                  "PNI": ["PN", "PN1"],
                  "PNP": ["PP$","PPH1", "PPH1", "PPHO1", "PPHO2", "PPHS1", "PPHS2", "PPIO1","PPIO2", "PPIS1", "PPIS2"],
                  "PNQ": ["PNQO", "PNQS", "PNQVS"],
                  "PNX": ["PNX1", "PPX1", "PPX2"],
                  "POS": [],
                  "PRF": ["IO"],
                  "PRP": ["II", "IW", "IF"],
                  "PUL": [],
                  "PUN": ["YQUE", "PUN"],
                  "PUQ": [],
                  "PUR": [],
                  "TO0" : ["TO"],
                  "UNC" : ["FU"],
                  "VBB" : ["VB0", "VBR", "VBM"],
                  "VBD" : ["VBDR", "VBDZ"],
                  "VBG" : ["VBG"],
                  "VBI" : ["VBI"],
                  "VBN" : ["VBN"],
                  "VBZ" : ["VBZ"],
                  "VDB" : ["VD0"],
                  "VDD" : ["VDD"],
                  "VDG" : ["VDG"],
                  "VDI" : ["VDI"],
                  "VDN" : ["VDN"],
                  "VDZ" : ["VDZ"],
                  "VHB" : ["VH0"],
                  "VHD" : ["VHD"],
                  "VHG" : ["VHG"],
                  "VHI" : ["VHI"],
                  "VHN" : ["VHN"],
                  "VHZ" : ["VHZ"],
                  "VM0" : ["VM", "VMK"],
                  "VVB" : ["VV0"],
                  "VVD" : ["VVD"],
                  "VVG" : ["VVG", "VVGK"],
                  "VVI" : ["VVI"],
                  "VVN" : ["VVN", "VVNK"],
                  "VVZ" : ["VVZ"],
                  "XX0": ["XX"],
                  "ZZ0": ["ZZ1", "ZZ2"],
                  "UNC": ["FU"]}

    tags = csv_df.iloc[:,0]
    for k,v in tagset_rep.items():
        # If the enriched tag is in the list associated with a standard BNC tag it is replaced with
        # that standard tag
        tags.mask(tags.isin(v), k, inplace=True)
        csv_df.iloc[:, 0] = tags
    return(csv_df)


def main(in_f='BNC.spoken.csv', out_f="BNC.spoken.clean.txt"):
    csv_file = pd.read_csv(in_f, sep="\t", encoding='utf-8', header=None)
    csv_file.drop(csv_file.columns[[2]], axis=1, inplace=True)
    csv_file.dropna(inplace=True)
    csv_file = change_tagset(csv_file)
    csv_file = csv_file[[1, 0]]
    csv_file.to_csv(out_f, sep="\t", encoding='utf-8', header=None, index=False)

#PPIS1	I
#VBM	'm
#VVGK	gon
#RRQV	whenever
#Extract n length sentences from a tagged dataset
if __name__ == "__main__":
    #input_file, output_file, length = sys.argv[1:4]
    #main(int(length), input_file, output_file)
    main()