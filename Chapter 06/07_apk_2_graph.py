# https://github.com/PegX/Hybroid/tree/main/apk_graph_corpus
# Reference from the hybroid code

import sys
import os

# Dependence on the androguard to analyze the Android application
sys.path.insert(0, os.path.abspath("modules/androguard"))
import argparse
from graphs import process_dir

def exit():
    parser.print_help()
    sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detecting and classifying Android malware for graph embedding')

    parser.add_argument("-d", "--dir", default="",
                        help="Load APK/DEX files from this directory.")

    parser.add_argument("-o", "--out", default="data/fcg",
                        help="Select output directory for generated graphs.\
                        If no directory is given, they will be written\
                        to the data/fcg directory.")

    parser.add_argument("-i", "--inst", default="data/inst",
                        help="Select output directory for extracted instruction.\
                        If no directory is given, they will be written\
                        to the data/inst directory.")

    parser.add_argument("-s", "--size", default="64",
                        help="Indicate the size of instruction/opcode embedding")

    parser.add_argument("-e", "--function_embedding", default="mean",
                        help="Indicate the algorithm of function embedding: mean, sif, rnn")

    parser.add_argument("-g", "--generate_corpus", default="False",
                        help="Indicate to generate opcode corpus or not")

    fcga = parser.add_argument_group('CALL GRAPHS ANALYSIS')
    fcga.add_argument("-f", "--fcgraphs", action="store_true",
                      help="Extract function call graphs from all APK/DEX files\
                     in the given directory.")

    args = parser.parse_args()

    mode = ""
    if args.fcgraphs:
        args.out = os.path.realpath(args.out)
        mode = 'FCG'

    if mode:
        process_dir(args.dir, args.out, args.inst, args.size, args.function_embedding, args.generate_corpus, mode)

    else:
        exit()