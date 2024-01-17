## One-time setup

```
# run from the root of the repository
sudo apt install -y python3 python3-pip python3-venv curl graphviz libgraphviz-dev openjdk-19-jre-headless
mkdir lib
(cd lib/; curl -O 'https://www.antlr.org/download/antlr-4.13.1-complete.jar')
python3 -m venv .env/
source .env/bin/activate
export CLASSPATH=$PWD/lib/antlr-4.13.1-complete.jar:$CLASSPATH
make -C compiler/grammar/
pip3 install -e ./
```

## Examples

### While2IR

Translate While program to IR and save to a file.
```
cat tests/fact.while | while2ir > tests/fact.ir
```

Interpret the resulting output IR with input 10.
```
interpreter <(cat tests/fact.while | while2ir) 10
```

### ControlFlow

Generate a control-flow graph for the While program, saving it to a file.
```
cat tests/fact.while | while2ir | controlflow > tests/fact.cfg
cat tests/fact.ir | controlflow > tests/fact.cfg # component-only
```

Generate a control-flow graph and visualize it.
```
cat tests/fact.while | while2ir | controlflow | graphview tests/fact.png
cat tests/fact.ir | controlflow | graphview tests/fact.png # component-only
```

Interpret the IR generated from the control-flow graph, inputting 10.
```
interpreter <(cat tests/fact.while | while2ir | controlflow | cfg2ir) 10
interpreter <(cat tests/fact.ir | controlflow | cfg2ir) 10 # component-only
```

### Optimizer

Generate an optimized control-flwo graph for the While program, saving it to a file.
```
cat tests/fact.while | while2ir | controlflow | optimizer > tests/fact.opt.cfg
cat tests/fact.cfg | optimizer > tests/fact.opt.cfg # component-only
```

Interpreter the optimized While program IR, inputting 10.
```
interpreter <(cat tests/fact.while | while2ir | controlflow | optimizer | cfg2ir) 10
interpreter <(cat tests/fact.cfg | optimizer | cfg2ir) 10 # component-only
```

Compare the optimized and unoptimized IR.
```
diff -y <(cat tests/dce.while | while2ir | controlflow | cfg2ir) <(cat tests/dce.while | while2ir | controlflow | optimizer | cfg2ir)
```

### CodeGen

Compile the While program to an optimized assembly file.
```
	cat tests/fact.while | while2ir | controlflow | optimizer | codegen > tests/fact.s
	cat tests/fact.opt.cfg | codegen > tests/fact.s # component-only
```

### Complete Compiler

```
compiler tests/fact.while
gcc -o tests/fact tests/fact.s runtime/io.c
echo "10" | ./tests/fact # output: 3628800
```

```
compiler tests/dce.while
gcc -o tests/dce tests/dce.s runtime/io.c
echo "23" | ./tests/dce # output: 17
```
