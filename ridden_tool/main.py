import argparse
import sys
from .ridden_function import infer_receptor_activity,get_output_file_name

def positive_int(value):
    ivalue = int(value)
    if ivalue < 1:
        raise argparse.ArgumentTypeError(f"Invalid value: {value}. The value must be greater than or equal to 1.")
    return ivalue

def cli():

    parser = argparse.ArgumentParser(description="Run RIDDEN, the Data-driven inference of receptor activity for cell-cell communication studies")
    parser.add_argument("input", type=argparse.FileType('r'), default='-', help="Path to the input file. The input file format is csv and it contains gene symbols in columns and cells or samples in rows.")
    parser.add_argument("-p", "--number-of-permutation", type=positive_int, default=100, help="Number of permutations (default: 100)")
    parser.add_argument("-c", "--chunk-size", type=positive_int, default=100, help="Size of data processing chunks (default: 100)")
    parser.add_argument("-o", "--output-name", default="output", help="Name for the output file (default: output). The output file format is csv.")
    parser.add_argument("--debug", action="store_true", help="Print debug information")
    args = parser.parse_args()

    perm_message = "default 100" if args.number_of_permutation == 100 else str(args.number_of_permutation)
    chunk_message = "default 100" if args.chunk_size == 100 else str(args.chunk_size)
    output_message = "default name output.csv" if args.output_name == "output.csv" else get_output_file_name(args.output_name)

    print(f"RIDDEN is run on '{args.input.name}' with {perm_message} permutations, size of chunks is {chunk_message} and result is saved to {output_message}")

    try:
        infer_receptor_activity(args.input, args.number_of_permutation, args.chunk_size, args.output_name)
    except Exception as e:
        sys.stderr.write('Inferring receptor activities failed. For troubleshooting, please get in touch with the authors.\n')
        if args.debug:
            sys.stderr.write(f'Error: {e}\n')
        sys.exit(1)

if __name__ == "__main__":
    cli()