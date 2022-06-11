from add_null import run as an_run
from create_excel import run as ce_run
from clean_bnc_xml import run as cbx_run

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

main():
    #python3 add_null.py BNC_XML_2007/wst_c5 BNC_XML_2007/sen_wst_c5 test_null -so -con -n 200 -b 4 -a 5
    parser = argparse.ArgumentParser()
    parser.add_argument("outfyes", type=str, help="INPUT: path for creating written sentences per line file from BNC with punctuation")
    parser.add_argument("outfno", type=str, help="INPUT: path for creating written sentences per line file from BNC without punctuation")
    parser.add_argument("outf", type=str,help="INPUT: path for creating tagged written sentences")
    parser.add_argument("pyv", type=int, default=3, help="INPUT: python version - should be '2' or '3'")


    parser.add_argument('-sa', action='store_true', help='Sample random sentences from the in_file')
    parser.add_argument('-con', action='store_false', help='Sample random sentences from the in_file as well as r sentence before and l sentences after')
    parser.add_argument('-so', action='store_false', help='Give the source ID of this sentence')
    parser.add_argument('-n', type=int, default=500, help='number of sentences to sample (requires sample flag to be set)')
    parser.add_argument('-c', type=int, default=-1, help='number of sentences before and after the sampled sentence to include')
    parser.add_argument('-b', type=int, default=3, help='number of sentences before a sampled sentence to include')
    parser.add_argument('-a', type=int, default=3, help='number of sentences after a sampled sentence to include')

    add_null_params = get_params(args)
    check_output(f"python{py_version} add_null.py {outfyes} {in_file} {out_file} -n {n}{add_null_params}", shell=True)
    check_output(f"python{py_version} add_null.py {outfyes} {in_file} {out_file} -n {n}{add_null_params}", shell=True)
    
if __name__ == "__main__":
    main()