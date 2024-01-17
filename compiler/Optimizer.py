import sys
from compiler.While3Addr import *
import networkx as nx
import pickle
import logging
import compiler.util as util
from compiler.GraphView import *
from collections import defaultdict, deque
from functools import reduce

def optimizer(cfg):
  # TODO
  return cfg

def main():
  import sys
  logging.basicConfig(level=logging.DEBUG)

  cfg = pickle.loads(sys.stdin.buffer.read())

  cfg = optimizer(cfg)
    
  sys.stdout.buffer.write(pickle.dumps(cfg))
  
if __name__ == '__main__':
  main()
