import ast

class frame_generator(ast.NodeVisitor):
    def __init__(self, outfile):
        self.var = set()
        self.file = outfile
        self.rval = False

    def visit_Name(self, node):
        self.var.add(node.id)

    def visit_FunctionDef(self, node):
        for item in ast.walk(node):
            if(isinstance(item,ast.Return)):
                if(item.value):
                    self.rval=True
        return

    def visit_Call(self, node):
        return

    def show_frame(self):
        var_len = len(self.var)
        if(var_len != 0):
            self.file.write("frame(")
            if(self.rval):
                for v in self.var:
                    self.file.write(v+",")
                self.file.write("RVal) and (\n")
            else:
                index = 0
                for v in self.var:
                    if(index < var_len-1):
                        self.file.write(v+",")
                    else:
                        break
                    index += 1
                self.file.write(v+") and (\n")
        else:
            if(self.rval):
                self.file.write("frame(")
                self.file.write("RVal) and (\n")

    def printed_frame(self):
        var_len = len(self.var)
        if(var_len == 0 and not self.rval):
            return False
        else:
            return True


class func_def_visitor(ast.NodeVisitor):
    def __init__(self, outfile):
        self.out = outfile
        self.import_module = []

    def visit_FunctionDef(self, node):
        f=v(self.out)
        f.import_module = self.import_module
        self.out.write("function ")
        if(node.name == "lcm"):
            self.out.write("lcm1")
        else:
            self.out.write(node.name)
        self.out.write(" -> (")
        RVal_flag = 0
        for state in ast.walk(node):
            if(isinstance(state,ast.Return)):
                if(state.value):
                    RVal_flag = 1
                    break
        if(RVal_flag == 1):
            for state in node.args.args:
                f.visit(state)
                self.out.write(",")
            self.out.write("RVal) {\n")
        else:
            arg_len = len(node.args.args)
            index = 0
            if(arg_len != 0):
                for state in node.args.args:
                    if(index < arg_len-1):
                        f.visit(state)
                        self.out.write(",")
                    else:
                        break
                    index += 1
                f.visit(node.args.args[arg_len-1])
            self.out.write(") {\n")

        f.level += 1
        f.print_body(node.body)
        f.level -= 1
        f.level_print("};",1)
        del f

    def visit_Import(self, node):
        self.out.write("importpy ")
        for state in node.names:
            self.out.write("\""+state.name+"\"\n")
            self.import_module.append(str(state.name))


class v(ast.NodeVisitor):
    def __init__(self, outfile):
        self.level = 0
        self.out = outfile
        self.import_module = []
        self.varible_need_reference = set()

    def append_module(self, module):
        self.import_module.append(module)

    def level_print(self,content,enter):
        if(enter == 1):
            self.out.write(self.level*4*" " + content + "\n")
        if(enter == 0):
            self.out.write(self.level*4*" " + content)

    def print_one_line(self, node, semicolon):
        if(semicolon == 0):
            self.level_print("",0)
            self.visit(node)
            self.out.write("\n")
        if(semicolon == 1):
            self.level_print("",0)
            if(self.visit(node)!=2):
                self.out.write(";\n")

    def print_body(self, List):
        bodylen = len(List)
        index = 0
        for state in List:
            if(index < bodylen-1):
                self.print_one_line(state,1)
            else:
                break
            index += 1
        self.print_one_line(List[bodylen-1],0)

    def visit_Expr(self,node):
        if(isinstance(node.value,ast.Constant)):
            self.out.write("/*")
            self.out.write(node.value.value)
            self.out.write("*/\n")
            return 2
        else:
            self.generic_visit(node)

    def op_value(self,op):
        value = 0
        if(isinstance(op,ast.Pow)):
            value = 1
        if(isinstance(op,ast.Mult)):
            value = 2
        if(isinstance(op,ast.Div)):
            value = 2
        if(isinstance(op,ast.Mod)):
            value = 2
        if(isinstance(op,ast.FloorDiv)):
            value = 2
        if(isinstance(op,ast.Add)):
            value = 3
        if(isinstance(op,ast.Sub)):
            value = 3
        if(isinstance(op,ast.LShift)):
            value = 4
        if(isinstance(op,ast.RShift)):
            value = 4
        if(isinstance(op,ast.BitAnd)):
            value = 5
        if(isinstance(op,ast.BitXor)):
            value = 6
        if(isinstance(op,ast.BitOr)):
            value = 7

        return value

    def need_brackets(self,op,subtree,bias):
        self_value = self.op_value(op)-bias
        if(isinstance(subtree,ast.BinOp)):
            subtree_value = self.op_value(subtree.op)
            if(self_value < subtree_value):
                return True

    def visit_Constant(self, node):
        if(type(node.value) == str):
            self.out.write("\""+ast.unparse(node)[1:-1]+"\"")
        elif(type(node.value) == bool):
            if(node.value == True):
                self.out.write("true")
            else:
                self.out.write("false")
        else:
            self.out.write(str(node.value))

    def visit_Call(self, node):
        arglen = len(node.args)
        index = 0
        if(isinstance(node.func,ast.Name)):
            if( node.func.id[:5] == "extpy" or node.func.id == "type" or 
                    node.func.id == "open" or node.func.id == "fileno" or 
                    node.func.id == "fseek" or node.func.id == "fputs" or 
                    node.func.id == "fwritelines" or node.func.id == "ftell" or 
                    node.func.id == "fread" or node.func.id == "freadline" or 
                    node.func.id == "freadlines" or node.func.id == "ftruncate" or 
                    node.func.id == "fflush" or node.func.id == "fclose" or 
                    node.func.id == "strCapitalize" or node.func.id == "strCount" or 
                    node.func.id == "strCenter" or node.func.id == "strEndswith" or 
                    node.func.id == "strIsalnum" or node.func.id == "strIsalpha" or 
                    node.func.id == "strIsdigit" or node.func.id == "strIsspace" or 
                    node.func.id == "strIslower" or node.func.id == "strIssuper" or 
                    node.func.id == "strIstitle" or node.func.id == "strExpandtabs" or 
                    node.func.id == "strLjust" or node.func.id == "strRjust" or 
                    node.func.id == "strReplace" or node.func.id == "strJoin" or 
                    node.func.id == "strLower" or node.func.id == "strUpper" or 
                    node.func.id == "strLstrip" or node.func.id == "strRstrip" or 
                    node.func.id == "strStrip" or node.func.id == "strMax" or 
                    node.func.id == "strMin" or node.func.id == "strSplit" or 
                    node.func.id == "strSplitlines" or node.func.id == "strStartswith" or
                    node.func.id == "strSwapcase" or node.func.id == "strTitle" or 
                    node.func.id == "strZfill" or node.func.id == "strIsdecimal" or 
                    node.func.id == "find"):
                if(node.func.id == "open"):
                    self.out.write("fopen")
                else:
                    self.visit(node.func)
                self.out.write("(")
                if(arglen != 0):
                    index = 0
                    for state in node.args:
                        if(index < arglen-1):
                            self.visit(state)
                            self.out.write(",")
                        else:
                            break
                        index += 1
                    self.visit(node.args[arglen-1])
                self.out.write(")")
            elif(node.func.id == "print"):
                self.out.write("mout(")
                if(len(node.args)==0):
                    self.out.write("\"\\n\")")
                else:
                    index = 0
                    for state in node.args:
                        if(index < arglen-1):
                            if(isinstance(state,ast.BinOp)):
                                if(isinstance(state.op,ast.Add)):
                                    self.visit(state.left)
                                    self.out.write(",")
                                    self.visit(state.right)
                                else:
                                    self.visit(state)
                            else:
                                self.visit(state)
                            self.out.write(",")
                        else:
                            break
                        index += 1
                    if(isinstance(node.args[arglen - 1],ast.BinOp)):
                        if(isinstance(node.args[arglen - 1].op,ast.Add)):
                            self.visit(node.args[arglen - 1].left)
                            self.out.write(",")
                            self.visit(node.args[arglen - 1].right)
                        else:
                            self.visit(node.args[arglen-1])
                    else:
                        self.visit(node.args[arglen-1])
                    if(len(node.keywords) != 0):
                        if(node.keywords[0].value.value==''):
                            self.out.write(")")
                        else:
                            self.out.write(",")
                            self.visit(node.keywords[0].value)
                            self.out.write(")")
                    else:
                        self.out.write(");\n")
                        self.level_print("mout(\"\\n\")",0)
            elif(node.func.id == "len"):
                self.out.write(node.args[0].id+".size()")
            elif(node.func.id == "ord"):
                self.out.write("(int)")
                self.visit(node.args[0])
            elif(node.func.id == "chr"):
                self.out.write("(char)")
                self.visit(node.args[0])
            elif(node.func.id == "int"):
                self.out.write("((int)")
                self.visit(node.args[0])
                self.out.write(")")
            elif(node.func.id == "float"):
                self.out.write("((float)")
                self.visit(node.args[0])
                self.out.write(")")
            elif(node.func.id == "str"):
                self.out.write("to_string(")
                self.visit(node.args[0])
                self.out.write(")")
            else:
                self.visit(node.func)
                self.out.write("(")
                if(arglen != 0):
                    for state in node.args:
                        if(isinstance(state,ast.Name) and str(state.id) in self.varible_need_reference):
                            self.out.write("&")
                        self.visit(state)
                        self.out.write(",")
                    self.out.write("RVal)")
                else:
                    self.out.write(")")
        elif(isinstance(node.func,ast.Attribute)):
            if(node.func.attr == "insert"):
                self.visit(node.func)
                self.out.write("(")
                self.visit(node.args[1])
                self.out.write(",")
                self.visit(node.args[0])
                self.out.write(")")
            elif(node.func.attr == "sort" and len(node.keywords) != 0 and node.keywords[0].arg == "reverse"):
                if(node.keywords[0].value.value == True):
                    self.out.write(node.func.value.id+"."+node.func.attr+"(-1)")
                elif(node.keywords[0].value.value == False):
                    self.out.write(node.func.value.id+"."+node.func.attr+"(1)")
            elif(node.func.attr == 'copy'):
                self.visit(node.func)
            elif(node.func.attr == 'conjugate'):
                self.visit(node.func)
            else:
                if(node.func.value.id in self.import_module):
                    self.out.write("extpy ")
                self.visit(node.func)
                self.out.write("(")
                if(arglen != 0):
                    index = 0
                    for state in node.args:
                        if(index < arglen-1):
                            self.visit(state)
                            self.out.write(",")
                        else:
                            break
                        index += 1
                    self.visit(node.args[arglen-1])
                self.out.write(")") 
    
    def visit_If(self, node):
        if(isinstance(node.test,ast.Compare)):
            if(isinstance(node.test.ops[0], ast.In)):
                self.out.write("if ("+node.test.comparators[0].id+".haskey(")
                self.visit(node.test.left)
                self.out.write(")) then {\n")
            elif(isinstance(node.test.ops[0], ast.NotIn)):
                self.out.write("if (!"+node.test.comparators[0].id+".haskey(")
                self.visit(node.test.left)
                self.out.write(")) then {\n")
            else:
                self.out.write("if (")
                self.visit(node.test)
                self.out.write(") then {\n")
        else:
            self.out.write("if (")
            self.visit(node.test)
            self.out.write(") then {\n")
        self.level += 1
        self.print_body(node.body)
        self.level -= 1
        self.level_print("}",0)
        if(node.orelse):
            self.out.write("\n")
            self.level_print("else {",1)
            self.level += 1
            self.print_body(node.orelse)
            self.level -= 1
            self.level_print("}",0)
        else:
            self.out.write("\n")
            self.level_print("else {",1)
            self.level += 1
            self.level_print("empty",1)
            self.level -= 1
            self.level_print("}",0)
    
    def visit_While(self, node):
        self.out.write("while (")
        self.visit(node.test)
        self.out.write(") {\n")
        self.level += 1
        self.print_body(node.body)
        self.level -= 1
        if(node.orelse):
            self.level_print("};",1)
            self.print_body(node.orelse)
        else:
            self.level_print("}",0)

    def find_break(self, node):
        for item in ast.walk(node):
            if(isinstance(item,ast.Assign)):
                if(isinstance(item.targets[0],ast.Name)):
                    if(item.targets[0].id == "break_flag" and item.value.value == 1):
                        return True
        return False

    def find_return(self, node):
        for item in ast.walk(node):
            if(isinstance(item,ast.Assign)):
                if(isinstance(item.targets[0],ast.Name)):
                    if(item.targets[0].id == "return_flag" and item.value.value == 1):
                        return True
        return False

    def visit_For(self, node):
        i=node.target.id
        has_break = self.find_break(node)
        has_return = self.find_return(node)
        if(isinstance(node.iter,ast.Call)):
            if(node.iter.func.id == 'extpy range'):
                arg_len = len(node.iter.args)
                if(arg_len == 1):
                    self.out.write("for("+i+"=0;"+i+"<")
                    self.visit(node.iter.args[0])
                    if(has_return and has_break):
                        self.out.write(" and !break_flag and !return_flag;"+i+"="+i+"+1) {\n")
                    elif(has_return):
                        self.out.write(" and !return_flag;"+i+"="+i+"+1) {\n")
                    elif(has_break):
                        self.out.write(" and !break_flag;"+i+"="+i+"+1) {\n")
                    else:
                        self.out.write(";"+i+"="+i+"+1) {\n")
                elif(arg_len == 2):
                    self.out.write("for("+i+"=")
                    self.visit(node.iter.args[0])
                    self.out.write(";"+i+"<")
                    self.visit(node.iter.args[1])
                    if(has_return and has_break):
                        self.out.write(" and !break_flag and !return_flag;"+i+"="+i+"+1) {\n")
                    elif(has_return):
                        self.out.write(" and !return_flag;"+i+"="+i+"+1) {\n")
                    elif(has_break):
                        self.out.write(" and !break_flag;"+i+"="+i+"+1) {\n")
                    else:
                        self.out.write(";"+i+"="+i+"+1) {\n")
                elif(arg_len == 3):
                    self.out.write("for("+i+"=")
                    self.visit(node.iter.args[0])
                    if(isinstance(node.iter.args[2],ast.UnaryOp)):
                        self.out.write(";"+i+">")
                    else:
                        self.out.write(";"+i+"<")
                    self.visit(node.iter.args[1])
                    if(has_return and has_break):
                        self.out.write(" and !break_flag and !return_flag;"+i+"="+i+"+1) {\n")
                    elif(has_return):
                        self.out.write(" and !return_flag;"+i+"="+i+"+1) {\n")
                    elif(has_break):
                        self.out.write(" and !break_flag;"+i+"="+i+"+1) {\n")
                    else:
                        self.out.write(";"+i+"="+i+"+")
                    self.visit(node.iter.args[2])
                    self.out.write(") {\n")
                self.level += 1
                self.print_body(node.body)
                self.level -= 1
        if(node.orelse):
            self.level_print("};",1)
            self.print_body(node.orelse)
        else:
            self.level_print("}",0)
    
    def visit_Assign(self, node):
        if(isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Name)):
            if(node.value.func.id == "int"):
                if(isinstance(node.value.args[0],ast.Call) and node.value.args[0].func.id == "input"):
                    self.out.write("mout(")
                    index = 0
                    arglen = len(node.value.args[0].args)
                    for state in node.value.args[0].args:
                        if(index < arglen-1):
                            self.visit(state)
                            self.out.write(",")
                        else:
                            break
                        index += 1
                    self.visit(node.value.args[0].args[arglen-1])
                    self.out.write(");\n")
                    self.visit(node.targets[0])
                    self.out.write("=0;\n")
                    self.out.write("mscan(")
                    self.visit(node.targets[0])
                    self.out.write(")")
                else:
                    self.visit(node.targets[0])
                    self.out.write("=")
                    self.out.write("((int)")
                    for state in node.value.args:
                        self.visit(state)
                    self.out.write(")")
            elif(node.value.func.id == "float"):
                if(node.value.args[0].func.id == "input"):
                    self.out.write("mout(")
                    index = 0
                    arglen = len(node.value.args[0].args)
                    for state in node.value.args[0].args:
                        if(index < arglen-1):
                            self.visit(state)
                            self.out.write(",")
                        else:
                            break
                        index += 1
                    self.visit(node.value.args[0].args[arglen-1])
                    self.out.write(");\n")
                    self.visit(node.targets[0])
                    self.out.write("=0.0;\n")
                    self.out.write("mscan(")
                    self.visit(node.targets[0])
                    self.out.write(")")
            elif(node.value.func.id == "input"):
                self.out.write("mout(")
                index = 0
                arglen = len(node.value.args)
                for state in node.value.args:
                    if(index < arglen-1):
                        self.visit(state)
                        self.out.write(",")
                    else:
                        break
                    index += 1
                self.visit(node.value.args[arglen-1])
                self.out.write(");\n")
                self.visit(node.targets[0])
                self.out.write("=\" \";\n")
                self.out.write("mscan(")
                self.visit(node.targets[0])
                self.out.write(")")
            else:
                self.visit(node.targets[0])
                self.out.write(" = ")
                self.visit(node.value)

        elif(isinstance(node.value,ast.Tuple) and isinstance(node.targets[0],ast.Tuple)):
            for i in range(len(node.value.elts)):
                self.out.write("temp"+str(i)+"=")
                self.visit(node.value.elts[i])
                self.out.write(";\n")
            for i in range(len(node.targets[0].elts)-1):
                self.visit(node.targets[0].elts[i])
                self.out.write("=")
                if(not(isinstance(node.value.elts[i],ast.Constant))):
                    self.out.write("temp"+str(i)+";\n")
                else:
                    self.visit(node.value.elts[i])
                    self.out.write(";\n")
            self.visit(node.targets[0].elts[len(node.targets[0].elts)-1])
            self.out.write("=")
            if(not(isinstance(node.value.elts[len(node.targets[0].elts)-1],ast.Constant))):
                self.out.write("temp"+str(len(node.targets[0].elts)-1))
            else:
                self.visit(node.value.elts[len(node.targets[0].elts)-1])
        elif(isinstance(node.targets[0],ast.Tuple)):
            index = 0
            for state in node.targets[0].elts:
                if(index < len(node.targets[0].elts)-1):
                    self.visit(state)
                    self.out.write(" = ")
                    self.visit(node.value)
                    self.out.write(";\n")
                else:
                    break
                index+=1
            self.visit(node.targets[0].elts[len(node.targets[0].elts)-1])
            self.out.write(" = ")
            self.visit(node.value)
        else:
            if(isinstance(node.targets[0],ast.Name) and 
                    (isinstance(node.value,ast.List) or isinstance(node.value,ast.Dict) or 
                    isinstance(node.value,ast.Subscript) 
                    # or 
                    #(isinstance(node.value,ast.Call) and (node.value.func.id == 'list' or node.value.func.id == 'dict') ) 
                    ) ):
                self.varible_need_reference.add(str(node.targets[0].id))
            index = 0
            for state in node.targets:
                if(index < len(node.targets)-1):
                    self.visit(state)
                    self.out.write(" = ")
                    self.visit(node.value)
                    self.out.write(";\n")
                else:
                    break
                index+=1
            self.visit(node.targets[len(node.targets)-1])
            self.out.write(" = ")
            self.visit(node.value)
    
    def visit_Return(self, node):
        if(node.value):
            self.out.write("RVal = ")
            self.visit(node.value)

    def visit_Name(self, node):
        self.out.write(node.id)

    def visit_Module(self, node):
        self.print_body(node.body)

    def visit_Subscript(self, node):
        if(isinstance(node.slice,ast.Constant)):
            if(type(node.slice.value) == str):
                self.visit(node.value)
                self.out.write("[")
                self.visit(node.slice)
                self.out.write("]")
            else:
                self.out.write(ast.unparse(node).replace("][",","))
        else:
            self.out.write(ast.unparse(node))

    def visit_BoolOp(self, node):
        index = 0
        values_len = len(node.values)
        for state in node.values:
            if(index < values_len-1):
                self.out.write("(")
                self.visit(state)
                self.out.write(")")
                self.visit(node.op)
            else:
                break
            index += 1
        self.out.write("(")
        self.visit(node.values[values_len-1])       
        self.out.write(")")

    def visit_Compare(self, node):
        self.visit(node.left)
        index = 0
        for i in range(len(node.ops)):
            self.visit(node.ops[i])
            self.visit(node.comparators[i])

    def visit_UnaryOp(self,node):
        self.out.write("(")
        self.visit(node.op)
        self.visit(node.operand)       
        self.out.write(")")

    def visit_BinOp(self, node):
        left_brackets = self.need_brackets(node.op,node.left,0)
        right_brackets = self.need_brackets(node.op,node.right,1)
        '''
        if(isinstance(node.op,ast.Div)):
            self.out.write("((float)")
            self.visit(node.left)
            self.out.write(")/")
            if(right_brackets):
                self.out.write("(")
            self.visit(node.right)
            if(right_brackets):
                self.out.write(")")
        elif(isinstance(node.op,ast.Pow)):
        '''
        if(isinstance(node.op,ast.Pow)):
            self.out.write("pow(")
            self.visit(node.left)
            self.out.write(",")
            self.visit(node.right)
            self.out.write(")")
        else:
            if(left_brackets):
                self.out.write("(")
            self.visit(node.left)
            if(left_brackets):
                self.out.write(")")
            self.visit(node.op)
            if(right_brackets):
                self.out.write("(")
            self.visit(node.right)
            if(right_brackets):
                self.out.write(")")

    def visit_arg(self, node):
        self.out.write(node.arg)

    def visit_Add(self,node):
        self.out.write(" + ")
    
    def visit_Sub(self,node):
        self.out.write(" - ")
    
    def visit_Mult(self,node):
        self.out.write(" * ")

    def visit_FloorDiv(self,node):
        self.out.write(" / ")

    def visit_Div(self,node):
        self.out.write(" / ")
    
    def visit_Mod(self,node):
        self.out.write(" % ")
    
    def visit_LShift(self,node):
        self.out.write(" << ")
    
    def visit_RShift(self,node):
        self.out.write(" >> ")
    
    def visit_BitOr(self,node):
        self.out.write(" | ")
    
    def visit_BitXor(self,node):
        self.out.write(" ^ ")
    
    def visit_BitAnd(self,node):
        self.out.write(" & ")

    def visit_UAdd(self,node):
        self.out.write("+")
    
    def visit_USub(self,node):
        self.out.write("-")

    def visit_Not(self,node):
        self.out.write("!")

    def visit_Invert(self,node):
        self.out.write("~")

    def visit_And(self,node):
        self.out.write(" and ")

    def visit_Or(self,node):
        self.out.write(" or ")

    def visit_Eq(self,node):
        self.out.write("==")

    def visit_NotEq(self,node):
        self.out.write("!=")

    def visit_Lt(self,node):
        self.out.write("<")

    def visit_LtE(self,node):
        self.out.write("<=")

    def visit_Gt(self,node):
        self.out.write(">")

    def visit_GtE(self,node):
        self.out.write(">=")

    def visit_FunctionDef(self, node):
        return 2

    def visit_List(self, node):
        self.out.write("< ")
        elts_len = len(node.elts)
        if(elts_len != 0):
            index = 1
            for state in node.elts:
                if(index < elts_len):
                    self.visit(state)
                    self.out.write(",")
                index += 1
            self.visit(node.elts[elts_len-1])
        self.out.write(" >")

    def visit_Tuple(self, node):
        self.out.write("</ ")
        elts_len = len(node.elts)
        if(elts_len != 0):
            index = 1
            for state in node.elts:
                if(index < elts_len):
                    self.visit(state)
                    self.out.write(",")
                index += 1
            self.visit(node.elts[elts_len-1])
        self.out.write(" />")

    def visit_Set(self, node):
        self.out.write("{/ ")
        elts_len = len(node.elts)
        if(elts_len != 0):
            index = 1
            for state in node.elts:
                if(index < elts_len):
                    self.visit(state)
                    self.out.write(",")
                index += 1
            self.visit(node.elts[elts_len-1])
        self.out.write(" /}")
    def visit_Attribute(self, node):
        if(node.attr == 'add'):
            self.out.write(node.value.id+".append")
        elif(node.attr == 'copy'):
            self.out.write(node.value.id)
        elif(node.attr == 'union'):
            self.out.write(node.value.id+".set_union")
        elif(node.attr == 'discard'):
            self.out.write(node.value.id+".remove")
        elif(node.attr == 'real'):
            self.out.write(node.attr+"("+node.value.id+")")
        elif(node.attr == 'imag'):
            self.out.write(node.attr+"("+node.value.id+")")
        elif(node.attr == 'conjugate'):
            self.out.write("conj"+"("+node.value.id+")")
        else:
            self.out.write(node.value.id+"."+node.attr)

    def visit_Dict(self, node):
        self.out.write("{")
        if(len(node.keys) != 0):
            for i in range(len(node.keys)-1):
                self.visit(node.keys[i])
                self.out.write(":")
                self.visit(node.values[i])
                self.out.write(",")
            self.visit(node.keys[len(node.keys)-1])
            self.out.write(":")
            self.visit(node.values[len(node.keys)-1])
        self.out.write("}")

    def visit_Delete(self, node):
        self.visit(node.targets[0].value)
        self.out.write(".del(")
        self.visit(node.targets[0].slice)
        self.out.write(")")

    def visit_JoinedStr(self, node):
        v_len = len(node.values)
        index = 0
        for state in node.values:
            if(index < v_len-1):
                self.visit(state)
                self.out.write(",")
            else:
                break
            index += 1
        self.visit(node.values[v_len-1])

    def visit_FormattedValue(self, node):
        self.visit(node.value)

    def visit_Pass(self, node):
        self.out.write("empty")

    def visit_Import(self, node):
        for state in node.names:
            self.import_module.append(str(state.name))
        return 2
