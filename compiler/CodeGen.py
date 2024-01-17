from compiler.While3Addr import *
import networkx as nx
import pickle
import logging
import compiler.util as util

def codegen(filename, outfile, cfg):
  # TODO
  pass

def main():
  import sys
  cfg = pickle.loads(sys.stdin.buffer.read())
  codegen("stdin", sys.stdout, cfg)
  
if __name__ == '__main__':
  main()

