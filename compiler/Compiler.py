import sys
import os
from antlr4 import FileStream
from pathlib import Path
from compiler.While2IR import while2ir
from compiler.ControlFlow import controlflow
from compiler.Optimizer import optimizer
from compiler.CodeGen import codegen
from compiler.CFG2IR import cfg2ir
import logging
import compiler.util
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-optimizer", '-n', action="store_true", help="Disable optimizations.")
    parser.add_argument("--ir-only", '-i', action="store_true", help="Emit IR instead of machine code.")
    parser.add_argument("--verbose", '-v', action="store_true", help="Verbose debugging.")
    parser.add_argument("--quiet", '-q', action="store_true", help="Only report errors.")
    parser.add_argument("filename", help="The filename containing the While3Addr code.  Use \"-\" to read from stdin (which disables interactive mode automatically.")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    else:
        logging.getLogger().setLevel(logging.INFO)
    
    filename = args.filename
    filepath = Path(filename)
    stem = os.path.join(filepath.parent, filepath.stem)

    # parse and generate IR (.while -> list(Instruction))
    program = while2ir(FileStream(filename))
    # control flow analysis (list(Instruction -> CFG)
    cfg = controlflow(program.instructions)
    # optimization (CFG -> CFG)
    if not args.no_optimizer: cfg = optimizer(cfg)
    if args.ir_only:
        cfg2ir(sys.stdout, cfg)
    else:
        # code generation (CFG -> .asm)
        with open(f'{stem}.s', 'w') as outfile:
            logging.info(f"writing {stem}.s")
            codegen(filename, outfile, cfg)

if __name__ == '__main__':
    main()
