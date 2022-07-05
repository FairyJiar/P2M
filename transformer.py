import ast

class trans(ast.NodeTransformer):

    def visit_AugAssign(self, node):
        return ast.Assign(
            targets=[node.target],
            value=ast.BinOp(
                left=node.target,
                op=node.op,
                right=node.value
                ))

    def visit_Name(self, node):
        if(node.id == "lcm"):
            node.id = "lcm1"
        if(node.id == "string"):
            node.id = "str"
        return node

    def visit_Attribute(self, node):
        if(node.attr == "keys"):
            node.attr = "merge_keys"
        if(node.attr == "values"):
            node.attr = "merge_values"
        return node

    def visit_Call(self, node):
        BIF = ['abs','all','any','ascii','bin','bool','breakpoint','bytearray',
                'bytes','callable','chr','classmethod','compile','complex','delattr',
                'dict','dir','divmod','enumerate','eval','exec','filter','float','format',
                'frozenset','getattr','globals','hasattr','hash','help','hex','id','input',
                'int','isinstance','issubclass','iter','len','list','locals','map','max',
                'memoryview','min','next','object','oct','ord','pow','print','property',
                'range','repr','reversed','round','set','setattr','slice','sorted','staticmethod',
                'str','sum','super','tuple','vars','zip','__import__']

        if(isinstance(node.func,ast.Name)):
            if node.func.id in BIF:
                node.func.id = "extpy "+node.func.id
            else:
                self.visit(node.func)

        for state in node.args:
            self.visit(state)

        return node

class trans_file_files(ast.NodeTransformer):
    def visit_Call(self, node):
        if(isinstance(node.func,ast.Attribute)):
            if(node.func.attr == 'fileno' or node.func.attr == 'seek' or 
                    node.func.attr == 'write' or node.func.attr == 'writelines' or 
                    node.func.attr == 'tell' or node.func.attr == 'read' or 
                    node.func.attr == 'readline' or node.func.attr == 'readlines' or 
                    node.func.attr == 'truncate' or node.func.attr == 'flush' or 
                    node.func.attr == 'close'):
                if(node.func.attr == 'write'):
                    node.args.insert(1,node.func.value)
                else:
                    node.args.insert(0,node.func.value)
                node.func = ast.Name(id=node.func.attr)
                node.func.id = "f"+node.func.id
                if(node.func.id == "ffileno"):
                    node.func.id = "fileno"
                if(node.func.id == "fwrite"):
                    node.func.id = "fputs"

        self.generic_visit(node)
        return node

class trans_str_files(ast.NodeTransformer):
    def visit_Call(self, node):
        if(isinstance(node.func,ast.Attribute)):
            if(node.func.attr == 'capitalize' or node.func.attr == 'count' or 
                    node.func.attr == "center" or node.func.attr == "endswith" or 
                    node.func.attr == "isalnum" or node.func.attr == "isalpha" or 
                    node.func.attr == "isdigit" or node.func.attr == "isspace" or 
                    node.func.attr == "islower" or node.func.attr == "isupper" or 
                    node.func.attr == "istitle" or node.func.attr == "expandtabs" or 
                    node.func.attr == "ljust" or node.func.attr == "rjust" or 
                    node.func.attr == "replace" or node.func.attr == "join" or 
                    node.func.attr == "lower" or node.func.attr == "upper" or 
                    node.func.attr == "lstrip" or node.func.attr == "rstrip" or 
                    node.func.attr == "strip" or node.func.attr == "max" or 
                    node.func.attr == "min" or node.func.attr == "split" or 
                    node.func.attr == "splitlines" or node.func.attr == "startswith" or
                    node.func.attr == "swapcase" or node.func.attr == "title" or 
                    node.func.attr == "zfill" or node.func.attr == "isdecimal" or 
                    node.func.attr == "find" or node.func.attr == "isnumeric"):
                node.args.insert(0,node.func.value)
                node.func = ast.Name(id=node.func.attr)
                node.func.id = "str"+node.func.id.capitalize()
                if(node.func.id == "strFind"):
                    node.func.id = "find"
                if(node.func.id == "strIsupper"):
                    node.func.id = "strIssuper"
                if(node.func.id == "strIsnumeric"):
                    node.func.id = "strIsdecimal"


        self.generic_visit(node)
        return node

class trans_listcomp(ast.NodeTransformer):

#transform list comprehension
#eg L = [ i**2 for i in range(1,11)]

    def transListComp(self,body):
        for elements in body.copy():
            if(isinstance(elements,ast.Assign) and isinstance(elements.value,ast.ListComp)):
                index = body.index(elements)
                body.remove(elements)
                body.insert(index,ast.Assign(
                                        targets=[
                                            elements.targets[0]],
                                        value=ast.List(elts=[], ctx=ast.Load())))
                if(len(elements.value.generators[0].ifs)!=0):
                    body.insert(index+1,ast.For(
                                        target=elements.value.generators[0].target,
                                        iter=elements.value.generators[0].iter,
                                        body=[
                                             ast.If(
                                                 test=elements.value.generators[0].ifs[0],
                                                 body=[
                                                   ast.Expr(
                                                     value=ast.Call(
                                                        func=ast.Attribute(
                                                            value=ast.Name(id=elements.targets[0].id, ctx=ast.Load()),
                                                            attr='append',
                                                            ctx=ast.Load()),
                                                        args=[
                                                            elements.value.elt],
                                                        keywords=[]))],
                                                 orelse=[])],
                                        orelse=[]))
                elif(isinstance(elements.value.elt,ast.IfExp)):
                    body.insert(index+1,ast.For(
                                        target=elements.value.generators[0].target,
                                        iter=elements.value.generators[0].iter,
                                        body=[
                                             ast.If(
                                                 test=elements.value.elt.test,
                                                 body=[
                                                   ast.Expr(
                                                     value=ast.Call(
                                                        func=ast.Attribute(
                                                            value=ast.Name(id=elements.targets[0].id, ctx=ast.Load()),
                                                            attr='append',
                                                            ctx=ast.Load()),
                                                        args=[
                                                            elements.value.elt.body],
                                                        keywords=[]))],
                                                 orelse=[
                                                     ast.Expr(
                                                        value=ast.Call(
                                                            func=ast.Attribute(
                                                                value=ast.Name(id=elements.targets[0].id, ctx=ast.Load()),
                                                                attr='append',
                                                                ctx=ast.Load()),
                                                            args=[
                                                                elements.value.elt.orelse],
                                                            keywords=[]))])],
                                        orelse=[]))
                elif(len(elements.value.generators)!=1):
                    body.insert(index+1,ast.For(
                                        target=elements.value.generators[0].target,
                                        iter=elements.value.generators[0].iter,
                                        body=[
                                            ast.For(
                                                target=elements.value.generators[1].target,
                                                iter=elements.value.generators[1].iter,
                                                body=[
                                                    ast.Expr(
                                                        value=ast.Call(
                                                            func=ast.Attribute(
                                                                value=ast.Name(id=elements.targets[0].id, ctx=ast.Load()),
                                                                attr='append',
                                                                ctx=ast.Load()),
                                                            args=[
                                                                elements.value.elt],
                                                            keywords=[]))],
                                                orelse=[])],
                                        orelse=[]))
                else:
                    body.insert(index+1,ast.For(
                                        target=elements.value.generators[0].target,
                                        iter=elements.value.generators[0].iter,
                                        body=[
                                            ast.Expr(
                                                value=ast.Call(
                                                    func=ast.Attribute(
                                                        value=ast.Name(id=elements.targets[0].id, ctx=ast.Load()),
                                                        attr='append',
                                                        ctx=ast.Load()),
                                                    args=[
                                                        elements.value.elt],
                                                    keywords=[]))],
                                        orelse=[])) 
                                        
    def visit_Module(self, node):
        self.transListComp(node.body)
        return node


class trans_loop(ast.NodeTransformer):

#transform break, continue and return;
#1: let all if be mutually exclusive
#2: add a flag for break
#3: add else for continue break and return

    analyze_list = list()

    def find_break(self, node):
        for item in ast.walk(node):
            if(isinstance(item,ast.Break)):
                return True
        return False

    def find_continue(self, node):
        for item in ast.walk(node):
            if(isinstance(item,ast.Continue)):
                return True
        return False

    def find_return(self, node):
        for item in ast.walk(node):
            if(isinstance(item,ast.Return)):
                return True
        return False

    def recall(self, node, parents):
        has_break = self.find_break(node)
        has_continue = self.find_continue(node)
        has_return = self.find_return(node)
        has_orelse = False
        index = parents.index(node)
        if(not isinstance(node,ast.FunctionDef)):
            has_orelse = bool(node.orelse)
        if(has_break):
            parents.insert(index,ast.Assign(
                        targets=[ast.Name(id="break_flag")],
                        value=ast.Constant(value=0)))
            parents.insert(index+2,ast.Assign(
                        targets=[ast.Name(id="break_flag")],
                        value=ast.Constant(value=0)))
            if(has_orelse):
                parents.insert(index+2,ast.If(
                    test=ast.UnaryOp(
                        op=ast.Not(),
                        operand=ast.Name(id="break_flag")),
                    body=node.orelse.copy(),
                    orelse=list()))
                node.orelse.clear()
        if(has_continue):
            node.body.insert(0,ast.Assign(
                        targets=[ast.Name(id="continue_flag")],
                        value=ast.Constant(value=0)))
        if(has_return):
            index = parents.index(node)
            parents.insert(index,ast.Assign(
                        targets=[ast.Name(id="return_flag")],
                        value=ast.Constant(value=0)))
        if(has_break or has_continue or has_return):
            temp_list = self.analyze_list
            self.visit(node)
            self.analyze_list = temp_list
        return

    def reduce_JumpStatements(self, body):
    #if there are continue break or return in if-block, add an orelse to if-block
    
        break_aftermath = list()
        continue_aftermath = list()
        return_aftermath = list()
        if_has_break = False
        if_has_continue = False
        if_has_return = False
        for elements in body.copy():

            # Deal with cases that break or continue occur alone
            if(if_has_break):
                break_aftermath.append(elements)
                continue
            if(if_has_continue):
                continue_aftermath.append(elements)
                continue
            if(if_has_return):
                return_aftermath.append(elements)
                continue
            if(isinstance(elements,ast.Continue)):
            # find continue                          
                continue_index = body.index(elements)
                for remove_elements in body[continue_index:]:
                    body.remove(remove_elements)
                body.insert(continue_index+1,ast.Assign(
                            targets=[ast.Name(id="continue_flag")],
                            value=ast.Constant(value=1)))
                break

            elif(isinstance(elements,ast.Break)):
            # find break
                break_index = body.index(elements)
                for remove_elements in body[break_index:]:
                    body.remove(remove_elements)
                body.insert(break_index+1,ast.Assign(
                            targets=[ast.Name(id="break_flag")],
                            value=ast.Constant(value=1)))
                break

            elif(isinstance(elements,ast.Return)):
            # find return
                return_index = body.index(elements)
                if(not elements.value):
                    return_index-=1
                for remove_elements in body[return_index+1:]:
                    body.remove(remove_elements)
                body.insert(return_index+1,ast.Assign(
                            targets=[ast.Name(id="return_flag")],
                            value=ast.Constant(value=1)))
                break

            #Deal with cases where break continue or return does not occur alone
            elif(isinstance(elements,ast.While) or isinstance(elements,ast.For)):
            # find while-statement
                #Recursive call
                if_has_return = self.find_return(elements)
                self.recall(elements,body)

            elif(isinstance(elements,ast.FunctionDef)):
            # find while-statement
                #Recursive call
                temp_list = self.analyze_list
                self.visit(elements)
                self.analyze_list = temp_list

            elif(isinstance(elements,ast.If)):
            # find if-statement
                if_has_break = self.find_break(elements)
                if_has_continue = self.find_continue(elements)
                if_has_return = self.find_return(elements)
                self.analyze_list.append(elements)
                if(elements.orelse):
                    self.reduce_JumpStatements(elements.orelse)

        if(break_aftermath and continue_aftermath):
            for item in break_aftermath:
                body.remove(item)
            body.append(ast.If(
                test=ast.BoolOp(
                    op=ast.Or(),
                    values=[ast.UnaryOp(
                        op=ast.Not(),
                        operand=ast.Name(id="break_flag")),
                        ast.UnaryOp(
                        op=ast.Not(),
                        operand=ast.Name(id="continue_flag"))]),
                body=break_aftermath.copy(),
                orelse=list()
                ))
            self.analyze_list.append(body[-1])
        elif(break_aftermath):
            for item in break_aftermath:
                body.remove(item)
            body.append(ast.If(
                test=ast.UnaryOp(
                        op=ast.Not(),
                        operand=ast.Name(id="break_flag")),
                body=break_aftermath.copy(),
                orelse=list()
                ))
            self.analyze_list.append(body[-1])
        elif(continue_aftermath):
            for item in continue_aftermath:
                body.remove(item)
            body.append(ast.If(
                test=ast.UnaryOp(
                        op=ast.Not(),
                        operand=ast.Name(id="continue_flag")),
                body=continue_aftermath.copy(),
                orelse=list()
                ))
            self.analyze_list.append(body[-1])
        elif(return_aftermath):
            for item in return_aftermath:
                body.remove(item)
            body.append(ast.If(
                test=ast.UnaryOp(
                        op=ast.Not(),
                        operand=ast.Name(id="return_flag")),
                body=return_aftermath.copy(),
                orelse=list()
                ))
            self.analyze_list.append(body[-1])
        return

    def visit_While(self, node):
        has_break = self.find_break(node)
        has_return = self.find_return(node)
        self.analyze_list = list()
        self.analyze_list.append(node)
        while(self.analyze_list):
            self.reduce_JumpStatements(self.analyze_list[0].body)
            del self.analyze_list[0]
        if(has_break and has_return):
            node.test=ast.BinOp(
                    left=node.test,
                    op=ast.And(),
                    right=ast.BinOp(
                        left=ast.UnaryOp(
                            op=ast.Not(),
                            operand=ast.Name(id="break_flag")),
                        op=ast.And(),
                        right=ast.UnaryOp(
                            op=ast.Not(),
                            operand=ast.Name(id="return_flag"))))
        elif(has_break):
            node.test=ast.BinOp(
                    left=node.test,
                    op=ast.And(),
                    right=ast.UnaryOp(
                        op=ast.Not(),
                        operand=ast.Name(id="break_flag")))
        elif(has_return):
            node.test=ast.BinOp(
                    left=node.test,
                    op=ast.And(),
                    right=ast.UnaryOp(
                        op=ast.Not(),
                        operand=ast.Name(id="return_flag")))
        return node

    def visit_For(self, node):
        self.analyze_list = list()
        has_return = self.find_return(node)
        self.analyze_list.append(node)
        while(self.analyze_list):
            self.reduce_JumpStatements(self.analyze_list[0].body)
            del self.analyze_list[0]
        return node

    def visit_FunctionDef(self, node):
        self.analyze_list = list()
        self.analyze_list.append(node)
        while(self.analyze_list):
            self.reduce_JumpStatements(self.analyze_list[0].body)
            del self.analyze_list[0]
        return node

    def visit_Module(self, node):
        self.analyze_list = list()
        self.analyze_list.append(node)
        while(self.analyze_list):
            self.reduce_JumpStatements(self.analyze_list[0].body)
            del self.analyze_list[0]
        return node

class trans_main(ast.NodeTransformer):

    def visit_If(self, node):
        if(isinstance(node.test,ast.Compare)):
            if(isinstance(node.test.left,ast.Name)):
                if(node.test.left.id == "__name__"):
                    return node.body 
        return node
