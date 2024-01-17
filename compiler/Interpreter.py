import logging
from compiler.While3Addr import *
import compiler.util as util

class Interpreter:
  def __init__(self, prog, mem={}):
    self.prog = prog
    self.pc = 0
    self.mem = mem

  def step(self):
    if not self.done():
      self.run(self.prog[self.pc])
    else:
      # program is already over
      pass

  def done(self):
    return self.pc >= len(self.prog)

  def state(self):
    currentsym = "*** "
    progstr = ""
    for pc in range(0, len(self.prog)):
      if pc == self.pc:
        progstr += currentsym
      progstr += f'{pc}: {self.prog[pc]}\n'
    progstr += (currentsym if self.done() else "") + f'{len(self.prog)}: halt'
      
    memstr = "\n".join([ f'{x}: {self.mem[x]}' for x in self.mem.keys() ]) + "\n"
    pcstr = f'PC = {self.pc}\n' if not self.done() else "DONE"
    instrstr = f'Instruction = {self.prog[self.pc]}\n' if not self.done() else "DONE\n"
    # resultstr = f'\f\f\fMEM:\n{memstr}\n{pcstr}\n{instrstr}\nPROG:\n{progstr}\n'
    resultstr = f'\f\f\fMEM:\n{memstr}\nPROG:\n{progstr}\n'
    return resultstr

  def run(self, instr: Instruction):
    match instr:
      case Const(var, num):
        self.mem[var] = num
        self.pc += 1
      case Assign(var, fromvar):
        self.mem[var] = self.mem[fromvar]
        self.pc += 1
      case Op(var, left, op, right):
        self.mem[var] = aop_map[op](self.mem[left], self.mem[right])
        self.pc += 1
      case Goto(pc):
        self.pc = pc
      case IfGoto(var, opr, pc):
        rop_map = {Relational.EQUALTO: lambda x, y: x == y,
                   Relational.LESSTHAN: lambda x, y: x < y}
        if rop_map[opr](self.mem[var], 0):
          self.pc = pc
        else:
          self.pc += 1
      case Nop():
        self.pc += 1
        
def main():
  import sys
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("--non-interactive", "-n", action="store_true", help="Disable interactive mode.")
  parser.add_argument("filename", help="The filename containing the While3Addr code.  Use \"-\" to read from stdin (which disables interactive mode automatically.")
  parser.add_argument("inputvalue", nargs="?", default=0, help="An optional input value for the program.  Defaults to 0.")
  args = parser.parse_args()

  non_interactive = args.non_interactive
  filename = args.filename
  inputvalue = int(args.inputvalue)

  if filename == "-":
    non_interactive = True
    logging.info("reading from stdin")
  
  # TODO: interactive mode not supported when piping from stdin, turn off in that case
  f = sys.stdin if filename == "-" else open(filename, "r")
  prog = parseWhile3Addr(f.readlines())
  # print("\n".join([ f'{x}: {prog[x]}' for x in range(0, len(prog)) ]))
  mem = {util.input_variable: inputvalue}
  interp = Interpreter(prog, mem)
  while not interp.done():
    print(interp.state())
    if not non_interactive:
      input("press enter to continue...")
    interp.step()
  print(interp.state())
  if util.output_variable in interp.mem:
    print(f"Output: {interp.mem[util.output_variable]}")
  
if __name__ == '__main__':
  main()
