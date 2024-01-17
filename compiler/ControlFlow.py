import sys
from compiler.While3Addr import *
from compiler.GraphView import *
import networkx as nx
import pickle
import compiler.util
import logging

def controlflow(prog):
  cfg = nx.DiGraph()
  # TODO
  return cfg

def main():
  logging.basicConfig(level=logging.DEBUG)

  prog = parseWhile3Addr(sys.stdin.readlines())
  logging.debug("\n".join([ f'{x}: {prog[x]}' for x in range(0, len(prog)) ]))
  cfg = controlflow(prog)

  logging.debug(textualize_graph(cfg))

  sys.stdout.buffer.write(pickle.dumps(cfg))
  
if __name__ == '__main__':
  main()
