from parameter_file import *
from subprocess import check_output
from argparse import ArgumentParser

def an_flag_args():
    args_str = ""
    if sa:
        args_str += "-sa "
    if con:
        args_str += "-con "
    if so:
        args_str += "-so "
    if c != -1:
        args_str += f"-c {c}"
    else:
        args_str += f"-b {b} -a {a}"
    return(args_str)
def main():
    
    #python3 add_null.py BNC_XML_2007/wst_c5 BNC_XML_2007/sen_wst_c5 test_null -so -con -n 200 -b 4 -a 5
    parser = ArgumentParser()
    parser.add_argument('-cbx', action='store_true', help='run step 1: clean_bnc_xml.py')
    parser.add_argument('-an', action='store_true', help='run step 2: add_null.py')
    parser.add_argument('-ce', action='store_true', help='run step3: create_excel.py')

    args = parser.parse_args()

    if args.cbx:
        check_output(f"python{PY_VERSION} clean_bnc_xml.py {outfyes} {outfno} {outf} {bnc_root}", shell=True)
    if args.an:
        check_output(f"python{PY_VERSION} add_null.py {og_file} {an_in_file} {an_out_file} {an_ta} {an_sl} -n {n} {an_flag_args()}", shell=True)
    if args.ce:
        check_output(f"python{PY_VERSION} create_excel.py {ce_in_file} {ce_out_file} {ce_ta} {ce_sl}", shell=True)
    
if __name__ == "__main__":
    main()