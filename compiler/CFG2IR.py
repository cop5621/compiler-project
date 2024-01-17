import sys
from compiler.While3Addr import *
import networkx as nx
import pickle
import logging
import compiler.util
from compiler.GraphView import *

def cfg2ir(outf, cfg):
  # logging.debug(textualize_graph(cfg))

  # we no longer need the artificial entry block
  cfg.remove_node(0)
  
  # precompute start pc for each basic block so we can fill in gotos
  bbpc = {}

  # ensure exit node is last
  sortednodes = sorted(cfg.nodes)

  # TODO: do we need halt instruction?

  pc = 0
  for node in sortednodes:
    bbpc[node] = pc
    # get length of basic block
    # logging.debug(f'node: {node}')
    # logging.debug(len(cfg[node]))
    if len(cfg[node]) == 0: # exit block
      pc += len(cfg.nodes[node]['instrs'])
    elif len(cfg[node]) == 1: # unconditional branch block
      # add one for the goto we need to add
      pc += len(cfg.nodes[node]['instrs']) + 1
    elif len(cfg[node]) == 2: # conditional branch block
      # we will replace the last instruction with an ifgoto and add a goto
      pc += len(cfg.nodes[node]['instrs']) + 1
    else:
      # there shouldn't be any more than 2 edges
      assert False
      
  # logging.debug(bbpc)

  pc = 0
  for node in sortednodes:
    instrs = cfg.nodes[node]['instrs']
    if len(cfg[node]) == 0: # exit block
      # no need to add goto to an exit block
      pass
    elif len(cfg[node]) == 1: # unconditional branch block
      # we need to add a goto to the pc of the successor block
      successor = bbpc[list(cfg[node].keys())[0]]
      instrs.append(Goto(successor))
    elif len(cfg[node]) == 2: # conditional branch block
      # we will replace the last instruction with an ifgoto and add a goto
      trueedge = list(cfg[node])[0] if cfg[node][list(cfg[node])[0]]['condition'] else list(cfg[node])[1]
      falseedge = list(cfg[node])[0] if not cfg[node][list(cfg[node])[0]]['condition'] else list(cfg[node])[1]
      truesuccessor = bbpc[trueedge]
      falsesuccessor = bbpc[falseedge]
      testinstr = instrs[-1]
      instrs = instrs[:-1]
      instrs.append(IfGoto(testinstr.var, testinstr.opr, truesuccessor))
      instrs.append(Goto(falsesuccessor))
    else:
      # there shouldn't be any more than 2 edges
      assert False
    for instr in instrs:
      outf.write(f'{pc}: {instr}\n')
      pc = pc + 1

def main():
  cfg = pickle.loads(sys.stdin.buffer.read())

  cfg2ir(sys.stdout, cfg)
  
if __name__ == '__main__':
  main()
