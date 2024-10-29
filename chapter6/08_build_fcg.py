# https://github.com/PegX/Hybroid/tree/main/apk_graph_corpus
# Reference from the hybroid code

#!/usr/bin/python

""" A module to build NX graph objects from APKs. """

import zipfile
import networkx as nx
import numpy as np

from progressbar import *
from modules.androguard.androlyze import *
from androlyze import *
from utils import get_sha256
import pz as pz

import sys

sys.path.append("../function_embedding/")
sys.path.append("../function_embedding/sif_function_embedding/")
sys.path.append("../function_embedding/sif_function_embedding/src/")
from function_embedding import Function_Embedding as FE


class FCG():

    def __init__(self, filename, inst_dir, size, fe, gc, out):
        # print("FCG initialization")
        # FCG(f,inst_dir, size,fe)
        self.filename = filename
        self.gc = gc
        self.out = out
        print("gc", self.gc)

        print("Androgurad starting!")
        try:
            self.a = APK(filename)
            self.d = DalvikVMFormat(self.a.get_dex())
            self.d.create_python_export()
            self.dx = VMAnalysis(self.d)
            self.gx = GVMAnalysis(self.dx, self.a)
        except zipfile.BadZipfile:
            # if file is not an APK, may be a dex object
            self.d, self.dx = AnalyzeDex(self.filename)
        self.d.set_vmanalysis(self.dx)
        self.d.set_gvmanalysis(self.gx)
        self.d.create_xref()
        self.d.create_dref()

        if self.gc == 'True':
            print("generatingCorpus for{}".format(self.filename))
            self.generatingCorpus()
        else:
            print("Constructing graph for{}".format(self.filename))
            self.graphConstructing(inst_dir, size, fe)
        print("Androgurad OKAY!")

    def generatingCorpus(self):
        methods = self.d.get_methods()
        print("Method length\n", len(methods))
        f = open(self.filename + ".opcode", "w")
        for method in methods:
            # find all instructions in method and encode using coloring
            instructions = []

            for i in method.get_instructions():
                instructions.append(i.get_name())
                f.write(i.get_name() + " ")
        f.close()

    def graphConstructing(self, inst_dir, size, fe):
        self.inst_function = inst_dir + "/" + self.filename + ".inst"
        # self.inst_function = filename+".inst"
        embedding_name = "embedding_matrix_opcode_" + size + ".npy"
        print(embedding_name)
        # self.embedding = np.load("embedding_matrix.npy")
        self.embedding = np.load(embedding_name)
        self.function_embedding = fe
        self.size = size
        self.FE = FE(self.function_embedding, self.size)
        self.index = []
        self.instr2index = []
        print("FE is created")
        with  open("instruction.txt", "r") as fd:
            inst2index = fd.readlines()
            for i in range(len(inst2index)):
                self.index.append(i)
                self.instr2index.append(inst2index[i][:-1])
        self.index2instuction = dict(zip(self.instr2index, self.index))

        # print("preapre g")
        self.g = self.build_fcg()
        fd.close()
        print("preapre to return")
        return self.g

    def build_fcg(self):
        """ Using NX and Androguard, build a directed graph NX object so that:
            - node names are method names as: class name, method name and
              descriptor
            - each node has a label that encodes the method behavior
        """

        fcg = nx.DiGraph()
        # f = open(self.inst_function,"w")
        methods = self.d.get_methods()
        print("Method length\n", len(methods))

        for method in methods:
            node_name = self.get_method_label(method)
            # find calls from this method
            children = []
            for cob in method.XREFto.items:
                remote_method = cob[0]
                children.append(self.get_method_label(remote_method))

            # find all instructions in method and encode using coloring
            instructions = []

            for i in method.get_instructions():
                instructions.append(i.get_name())
                # f.write(i.get_name()+" ")

            if len(instructions) == 0:
                # encoded_label2 =  np.zeros(self.size)
                pass
            else:
                encoded_label2 = self.functionNode2vec(self.embedding, self.index2instuction, self.instr2index,
                                                       instructions)

            # print("finishing the function embedding")
            fcg.add_node(node_name, label=encoded_label2)
            fcg.add_edges_from([(node_name, child) for child in children])

        print("graph returning")
        return fcg

    def functionNode2vec(self, embedding, index2instuction, instr2index, instructions):
        """ Transfrom the function/node in call graph to vector"""
        # First step: instruction2vec
        instrValues = []
        instrKeys = []
        for inst in instructions:
            if inst in instr2index:
                vector = embedding[index2instuction[inst]]
                instrKeys.append(inst)
                instrValues.append(vector)
            else:
                print(inst)
                instrKeys.append(inst)
                inst = 'UNK'
                vector = embedding[index2instuction[inst]]
                instrValues.append(vector)
        # Second step: function embedding: func2vec

        if self.function_embedding == 'mean':
            sum_average = np.zeros([len(vector)])
            for i in range(len(instrValues)):
                sum_average += instrValues[i]

            if len(instrKeys) != 0:
                sum_average = sum_average / len(instructions)
            else:
                pass
            function_embedding = sum_average
            return function_embedding
        elif self.function_embedding == 'sif':
            # print("SIF function embedding - start")
            function_embedding = self.FE.embedding(instructions)
            # print("SIF function embedding - end")
            return function_embedding
        elif self.function_embedding == 'rnn':
            print("RNN function embedding - start")
            # function_embedding = self.FE.embedding(instructions)
            function_embedding = self.FE.embedding(instrValues)
            print("RNN function embedding - end")
            return function_embedding
        else:
            pass

        # return function_embedding

    def get_method_label(self, method):
        """ Return the descriptive name of a method
        """
        return (method.get_class_name(),
                method.get_name(),
                method.get_descriptor())


def process_dir(read_dir, out_dir, inst_dir, size, function_embedding, generate_corpus, mode='FCG'):
    """ Convert a series of APK into graph objects. Load all
    APKs in a dir subtree and create graph objects that are pickled
    for later processing and learning.
    """
    sys.setrecursionlimit(100000)
    files = []

    # check if pdg doesnt exist yet and mark the file to be processed
    for dirName, subdirList, fileList in os.walk(read_dir):
        for f in fileList:
            files.append(os.path.join(dirName, f))

    # set up progress bar
    print("\nProcessing {} APK files in dir {}".format(len(files), read_dir))
    widgets = ['Building graphs: ',
               Percentage(), ' ',
               Bar(marker='#', left='[', right=']'),
               ' ', ETA(), ' ']

    pbar = ProgressBar(widgets=widgets, maxval=len(files))
    pbar.start()
    progress = 0

    # loop through .apk files and save them in .pdg.pz format
    for f in files:

        f = os.path.realpath(f)
        print('[] Loading {0}'.format(f))
        try:
            if mode is 'FCG':
                # print("Here")
                graph = FCG(f, inst_dir, size, function_embedding, generate_corpus, out_dir)
                print("After graph constructing")

        # if an exception happens, save the .apk in the corresponding dir
        except Exception as e:
            err = e.__class__.__name__
            err_dir = err + "/"
            d = os.path.join(read_dir, err_dir)
            if not os.path.exists(d):
                os.makedirs(d)
            cmd = "cp {} {}".format(f, d)
            os.system(cmd)
            print("[*] {} error loading {}".format(err, f))
            continue

        h = get_sha256(f)
        if out_dir:
            out = out_dir
        else:
            out = read_dir
        fnx = os.path.join(out, "{}.pz".format(h))
        if generate_corpus != 'True':
            pz.save(graph.g, fnx)
            print("[*] Saved {}\n".format(fnx))
        progress += 1
        pbar.update(progress)
    pbar.finish()
    print("Done.")