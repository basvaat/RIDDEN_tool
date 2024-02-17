import argparse
import sys
from .ridden_function import infer_receptor_activity

def cli():

    parser = argparse.ArgumentParser(description="Run RIDDEN, the Data-driven inference of receptor activity for cell-cell communication studies")
    parser.add_argument("input", type=argparse.FileType('r'), default='-', help="Path to the input file. The input file format is csv and it contains gene symbols in columns and cells or samples in rows.")
    parser.add_argument("-p", "--number-of-permutation", type=int, default=100, help="Number of permutations (default: 100)")
    parser.add_argument("-c", "--chunk-size", type=int, default=100, help="Size of data processing chunks (default: 100)")
    parser.add_argument("-o", "--output-name", default="output", help="Name for the output file (default: output). The output file format is csv.")

    args = parser.parse_args()

    perm_message = "default 100" if args.number_of_permutation == 100 else str(args.number_of_permutation)
    chunk_message = "default 100" if args.chunk_size == 100 else str(args.chunk_size)
    output_message = "default name output" if args.output_name == "output" else str(args.output_name)

    print(f"RIDDEN is run on '{args.input}' with {perm_message} permutations, size of chunks is {chunk_message} and result is saved to {output_message}.csv")

    try:
        infer_receptor_activity(args.input, args.number_of_permutation, args.chunk_size, args.output_name)
    except:
        sys.stderr.write('Inferring receptor activities failed. For troubleshooting, please get in touch with the authors.\n')
        sys.exit(1)

if __name__ == "__main__":
    cli()