from enum import Enum
from dataclasses import dataclass
import re
import logging
import compiler.util

Arithmetic = Enum('Arithmetic', ["ADD", "SUBTRACT", "MULTIPLY", "DIVIDE"])
Relational = Enum('Relational', ["LESSTHAN", "EQUALTO"])

Arithmetic.__str__ = lambda self: {Arithmetic.ADD.value: '+', Arithmetic.SUBTRACT.value: '-', Arithmetic.MULTIPLY.value: '*', Arithmetic.DIVIDE.value: '/'}[self.value]
Relational.__str__ = lambda self: {Relational.LESSTHAN.value: '<', Relational.EQUALTO.value: '='}[self.value]

aop_map = {Arithmetic.ADD: lambda x, y: x + y,
           Arithmetic.SUBTRACT: lambda x, y: x - y,
           Arithmetic.MULTIPLY: lambda x, y: x * y,
           Arithmetic.DIVIDE: lambda x, y: x / y}

@dataclass
class Const:
  # x := n
  var: str
  num: int

  def __str__(self):
    return f'{self.var} := {self.num}'

  def __eq__(self, other):
    if isinstance(other, Const): return self.var == other.var and self.num == other.num
    else: return False

  def __hash__(self):
    return hash(str(self))

  def __repr__(self):
    return str(self)

  @staticmethod
  def parse(s):
    result = re.match("^([A-Za-z_][A-Za-z0-9_]*) := ([0-9]+)$", s)
    if result == None: return None
    var = result.group(1)
    num = int(result.group(2))
    return Const(var, num)
    
# print(Const.parse("_t1 := 55"))

@dataclass
class Assign:
  # x := y
  var: str
  fromvar: str

  def __str__(self):
    return f'{self.var} := {self.fromvar}'

  def __eq__(self, other):
    if isinstance(other, Assign): return self.var == other.var and self.fromvar == other.fromvar
    else: return False

  def __hash__(self):
    return hash(str(self))

  def __repr__(self):
    return str(self)

  @staticmethod
  def parse(s):
    result = re.match("^([A-Za-z_][A-Za-z0-9_]*) := ([A-Za-z_][A-Za-z0-9_]*)$", s)
    if result == None: return None
    var = result.group(1)
    fromvar = result.group(2)
    return Assign(var, fromvar)

# print(Assign.parse("_t1 := x"))

@dataclass
class Op:
  # x := y op z
  var: str
  left: str
  op: Arithmetic
  right: str

  def __str__(self):
    return f'{self.var} := {self.left} {self.op} {self.right}'

  def __eq__(self, other):
    if isinstance(other, Op): return self.var == other.var and self.left == other.left and self.op == other.op and self.right == other.right
    else: return False

  def __hash__(self):
    return hash(str(self))

  def __repr__(self):
    return str(self)

  @staticmethod
  def parse(s):
    result = re.match("^([A-Za-z_][A-Za-z0-9_]*) := ([A-Za-z_][A-Za-z0-9_]*) ([\+\-\*\/]) ([A-Za-z_][A-Za-z0-9_]*)$", s)
    if result == None: return None
    var = result.group(1)
    left = result.group(2)
    op = {'+': Arithmetic.ADD,
          '-': Arithmetic.SUBTRACT,
          '*': Arithmetic.MULTIPLY,
          '/': Arithmetic.DIVIDE}[result.group(3)]
    right = result.group(4)
    return Op(var, left, op, right)

# print(Op.parse("_t1 := x + y"))

@dataclass
class Goto:
  # goto n
  pc: int

  def __str__(self):
    return f'goto {self.pc}'

  def __eq__(self, other):
    if isinstance(other, Goto): return self.pc == other.pc
    else: return False

  def __hash__(self):
    return hash(str(self))

  def __repr__(self):
    return str(self)

  @staticmethod
  def parse(s):
    result = re.match("^goto ([0-9]+)$", s)
    if result == None: return None
    pc = int(result.group(1))
    return Goto(pc)

# print(Goto.parse("goto 2"))

@dataclass
class IfGoto:
  # if x op_r 0 goto n
  var: str
  opr: Relational
  pc: int

  def __str__(self):
    return f'if {self.var} {self.opr} 0 goto {self.pc}'

  def __eq__(self, other):
    if isinstance(other, IfGoto): return self.var == other.var and self.opr == other.opr and self.pc == other.pc
    else: return False

  def __hash__(self):
    return hash(str(self))

  def __repr__(self):
    return str(self)

  @staticmethod
  def parse(s):
    result = re.match("^if ([A-Za-z_][A-Za-z0-9_]*) ([\=\<]) 0 goto ([0-9]+)$", s)
    if result == None: return None
    var = result.group(1)
    opr = {'=': Relational.EQUALTO,
           '<': Relational.LESSTHAN}[result.group(2)]
    pc = int(result.group(3))
    return IfGoto(var, opr, pc)

@dataclass
class Test:
  # test x op_r 0
  var: str
  opr: Relational

  def __str__(self):
    return f'test {self.var} {self.opr} 0'

  def __eq__(self, other):
    if isinstance(other, Test): return self.var == other.var and self.opr == other.opr
    else: return False

  def __hash__(self):
    return hash(str(self))

  def __repr__(self):
    return str(self)

  @staticmethod
  def parse(s):
    result = re.match("^test ([A-Za-z_][A-Za-z0-9_]*) ([\=\<]) 0$", s)
    if result == None: return None
    var = result.group(1)
    opr = {'=': Relational.EQUALTO,
           '<': Relational.LESSTHAN}[result.group(2)]
    return Test(var, opr)

@dataclass
class Nop:
  def __str__(self):
    return f'nop'

  def __eq__(self, other):
    if isinstance(other, Nop): return True
    else: return False

  def __hash__(self):
    return hash(str(self))

  def __repr__(self):
    return str(self)

  @staticmethod
  def parse(s):
    result = re.match("^nop$", s)
    if result == None: return None
    return Nop()

# print(IfGoto.parse("if _t1 = 0 goto 2"))
# print(IfGoto.parse("if _t1 < 0 goto 2"))

Instruction = Const | Assign | Op | Goto | IfGoto | Test

class Program:
    """A While3Addr Program contains a list of instructions, provides temporary variable generation, and reports the program counter"""

    def __init__(self):
        def tempgen():
            counter = 0
            while True:
                yield f'_t{counter}'
                counter += 1
        self.tempgenobj = tempgen()
        self.instructions = list()

    def temp(self):
        """Get a new temp var"""
        return next(self.tempgenobj)

    def add(self, instr):
        """Add a new instruction"""
        self.instructions.append(instr)

    def pc(self):
        """Get the index of the next program counter in the current list of
instructions"""
        return len(self.instructions)

    def __str__(self):
        return "\n".join([ f'{x}: {str(self.instructions[x])}' for x in range(0, len(self.instructions)) ])
      
def parseWhile3Addr(lines):
  """Turn a list of lines (e.g., from readlines) into a list of while3addr instructions"""
  prog = []
  parsers = [Const.parse, Assign.parse, Op.parse, Goto.parse, IfGoto.parse, Nop.parse]
  pc_validate = 0
  for line in lines:
    result = re.match("^([0-9]+): (.*)$", line)
    pc = int(result.group(1))
    instrstr = result.group(2)

    instr = None
    for parser in parsers:
      instr = parser(instrstr)
      if instr != None:
        break
    if instr == None:
      # parse error
      logging.error(f'while3addr parse error: {instrstr}\n')
      assert True
    else:
      assert pc == pc_validate
      prog.append(instr)
      pc_validate += 1

  logging.debug(prog)
      
  return prog
