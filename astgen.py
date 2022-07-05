import ast
import visitor
import transformer
import sys,getopt

def process(filename,out):
    infile = open(filename,encoding='utf-8')
    outfile = open(out,"w")
    tree = ast.parse(infile.read())
    
    x=visitor.v(outfile)
    func_def_v = visitor.func_def_visitor(outfile)
    frame_gen = visitor.frame_generator(outfile)
    
    #print(ast.dump(tree,indent=4))
    tree = transformer.trans().visit(tree)
    tree = transformer.trans().visit(tree)
    tree = transformer.trans_loop().visit(tree)
    tree = transformer.trans_main().visit(tree)
    tree = transformer.trans_listcomp().visit(tree)
    tree = transformer.trans_file_files().visit(tree)
    tree = transformer.trans_str_files().visit(tree)
    #print(ast.dump(tree,indent=4))

    func_def_v.visit(tree)
    frame_gen.visit(tree)
    frame_gen.show_frame()
    printed_frame = frame_gen.printed_frame()
    x.visit(tree)
    if(printed_frame):
        outfile.write(")")

def main(argv):
    outfile = "default.m"
    try:
        opts,args=getopt.getopt(argv,"i:o:h",[])
    except getopt.GetoptError:
        print('-h help\n-o output file\n-i input file\n')
        sys.exit(2)
    for opt,arg in opts:
        if opt=='-h':
            print('-h help\n-o output file\n-i input file\n')
            sys.exit(2)
        if opt=='-o':
            outfile = arg
        if opt=='-i':
            process(arg,outfile)
            return

    print('-h help\n-o output file\n-i input file\n')
    
if __name__ == "__main__":
   main(sys.argv[1:])
