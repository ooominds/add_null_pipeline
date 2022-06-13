from add_null import run as an_run
from create_excel import run as ce_run
from clean_bnc_xml import run as cbx_run
from parameter_file import *


def get_params(args):
    other_params = ""
    if args.con:
        other_params += " -con"
    if args.so:
        other_params += " -so"
    if args.b and args.a:
        other_params += f" -b {args.b}"
        other_params += f" -a {args.a}"
    if args.c:
        other_params += f" -c {args.c}"
    return(other_params)

def main():
    
    #python3 add_null.py BNC_XML_2007/wst_c5 BNC_XML_2007/sen_wst_c5 test_null -so -con -n 200 -b 4 -a 5
    parser = argparse.ArgumentParser()
    parser.add_argument('-cbx', action='store_true', help='run step 1: clean_bnc_xml.py')
    parser.add_argument('-an', action='store_true', help='run step 2: add_null.py')
    parser.add_argument('-ce', action='store_true', help='run step3: create_excel.py')

    args = parser.parse_args()

    if args.cbx:
        check_output(f"python{PY_VERSION} clean_bnc_xml.py {outfyes} {outfno} {outf} {bnc_root}", shell=True)
    if args.an:
        check_output(f"python{PY_VERSION} add_null.py {og_file} {in_file} {out_file} -n {n}{add_null_params}", shell=True)
    if args.ce:
        check_output(f"python{PY_VERSION} create_excel.py {og_file} {in_file} {out_file} -n {n}{add_null_params}", shell=True)
    
if __name__ == "__main__":
    main()