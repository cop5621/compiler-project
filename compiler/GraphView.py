import networkx as nx
import pickle
import logging
import compiler.util

def visualize_graph(cfg, filename="graph.png"):
  # visualize graph
  A = nx.nx_agraph.to_agraph(cfg)
  # A.layout()
  A.draw(filename, prog="dot")

def textualize_graph(cfg):
  text = "Control Flow Graph\n"
  for node in sorted(cfg.nodes):
    text += f'BB{node}'
    text += str(", ".join([ f'->BB{x}{cfg[node][x]}' for x in cfg[node].keys() ]))
    text += "\n"
    text += "\n".join([ str(instr) for instr in cfg.nodes[node]["instrs"] ])
    text += "\n" if len(cfg.nodes[node]["instrs"]) > 0 else ""
    text += "\n"
  return text

def main():
  import sys
  
  cfg = pickle.loads(sys.stdin.buffer.read())

  if len(sys.argv) > 1:
    filename = sys.argv[1]
  else:
    filename = "graph.png"

  print(textualize_graph(cfg))
  visualize_graph(cfg, filename)

if __name__ == '__main__':
  main()
