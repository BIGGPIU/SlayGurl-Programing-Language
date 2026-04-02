import random

class NumberNode:
    def __init__(self, value):
        self.value = value

class StringNode:
    def __init__(self, value):
        self.value = value

class VariableNode:
    def __init__(self, name):
        self.name = name
class NoGirlMath:
    def __init__(self,expr):
        self.expr=expr
class BinaryOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryNode:
    def __init__(self, expr):
        self.expr = expr
class BlockNode:
    def __init__(self, statements):
        self.statements = statements

class VarDeclNode:
    def __init__(self, name):
        self.name = name

class VarAssignNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class VarDecAndAssignNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class PrintNewLineNode:
    def __init__(self):
        self.newline=True

class PrintNode:
    def __init__(self, expr,newline=False):
        self.expr = expr
        self.newline=newline
class InputNode:
    def __init__(self, var):
        self.var =var

class IfNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
class IfElseNode:
    def __init__(self, ifCondition, ifBody,elseBody):
        self.ifCondition = ifCondition
        self.ifBody =ifBody
        self.elseBody=elseBody
class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class FunctionNode:
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

class CallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class ReturnNode:
    def __init__(self, expr):
        self.expr = expr
class ReturnException(Exception):
    def __init__(self,value):
        self.value=value
class SyntaxParser:
    def __init__(self,tokens):
        self.tokens=tokens
        self.i=0
    def current(self):
        if self.i<len(self.tokens):
            return self.tokens[self.i]
        return None

    def eat(self):
        self.i+=1

    def expect(self, token_type):
        if self.current() and self.current()[0] == token_type:
            self.eat()
        else:
            raise Exception(f"Expected {token_type}, got {self.current()}")
    def parse_program(self):
        return self.parse_statements()
    
    def parse_statements(self):
        statements=[]
        while self.current() and self.current()[0]!="CLOSE_BLOCK":
            stmt=self.parse_statement()
            statements.append(stmt)
        return BlockNode(statements)
    
    def parse_statement(self):
        token=self.current()

        #declare and/or assign value to variable
        if token[0]=="VAR_DEC":
            self.eat()
            name=self.current()[1]
            self.eat()
            if self.current() and self.current()[0]=="ASSIGN":
                self.eat()
                expr=self.parse_expression()
                self.expect("END")
                return VarDecAndAssignNode(name,expr)
            self.expect("END")
            return VarDeclNode(name)
        
        #assign to existing variable
        if token[0] == "VARIABLE":
            name = token[1]
            self.eat()
            if self.current() and self.current()[0] == "ASSIGN":
                self.eat()
                expr = self.parse_expression()
                self.expect("END")
                return VarAssignNode(name, expr)
            # function call
            args=[]
            if self.current() and self.current()[0] == "LPAREN":
                self.eat()
                if self.current() and self.current()[0] == "RPAREN":
                    return CallNode(name,args)
                while True:
                    expr=self.parse_expression()
                    args.append(expr)
                    if self.current() and self.current()[0]=="RPAREN":
                        break
                    self.expect("COMMA")
                self.expect("RPAREN")
                if self.current() and self.current()[0]=="END":
                    self.eat()
                return CallNode(name,args)
        #print to console
        if token[0] == "PRINT":
            self.eat()
            newline=False
            expr=None
            if self.current() and self.current()[0]=="NEWLINE":
                newline=True
                self.eat()
            else:
                expr = self.parse_expression()
            if self.current() and self.current()[0]=="NEWLINE":
                newline=True
                self.eat()
            self.expect("END")
            if expr is None:
                return PrintNewLineNode()
            return PrintNode(expr,newline)
        
        if token[0]=="INPUT":
            self.eat()
            if self.current() and self.current()[0]=="VARIABLE":
                variable=self.current()[1]
                self.eat()
                self.expect("END")
                return InputNode(variable)
            else:
                raise Exception(f"Expected VARIABLE at {self.current()[1]}")
        
        if token[0]=="IF":
            self.eat()
            expr=self.parse_expression()
            self.expect("OPEN_BLOCK")
            body=self.parse_statements()
            self.expect("CLOSE_BLOCK")
            if self.current() and self.current()[0]=="ELSE":
                self.eat()
                self.expect("OPEN_BLOCK")
                elseBody=self.parse_statements()
                self.expect("CLOSE_BLOCK")
                return IfElseNode(expr,body,elseBody)
            return IfNode(expr,body)
        
        if token[0]=="WHILE":
            self.eat()
            expr=self.parse_expression()
            self.expect("OPEN_BLOCK")
            body=self.parse_statements()
            self.expect("CLOSE_BLOCK")
            return WhileNode(expr,body)
        
        if token[0]=="FUNCTION":
            self.eat()
            name=self.current()[1]
            self.eat()
            self.expect("LPAREN")
            args={}
            if self.current() and self.current()[0]!="RPAREN":    
                while True:
                    self.expect("VAR_DEC")
                    args[self.current()[1]]=None
                    self.eat()
                    if self.current() and self.current()[0]=="RPAREN":
                        break
                    self.expect("COMMA")
            self.eat()
            self.expect("OPEN_BLOCK")
            body=self.parse_statements()
            self.expect("CLOSE_BLOCK")
            return FunctionNode(name,args,body)
        
        if token[0]=="RETURN":
            self.eat()
            expr=self.parse_expression()
            self.expect("END")
            return ReturnNode(expr)
        
        raise Exception(f"Unknown statement: {token}")

    def parse_expression(self):
        return self.parse_logical()
    
    def parse_logical(self):
        left=self.parse_comparison()
        while self.current() and self.current()[0] in ("AND","OR"):
            op=self.current()[0]
            self.eat()
            right=self.parse_comparison()
            left=BinaryOpNode(left,op,right)
        return left
    
    def parse_comparison(self):
        left=self.parse_term()
        if self.current() and self.current()[0] in ("GRATER","GRATERE","LESSER","LESSERE","EQUEL","NEQUEL"):
            op=self.current()[0]
            self.eat()
            right=self.parse_term() 
            return BinaryOpNode(left,op,right)
        return left
    
    def parse_term(self):
        left=self.parse_factor()
        while self.current() and self.current()[0] in ("PLUS","MINUS"):
            op=self.current()[0]
            self.eat()
            right=self.parse_factor()
            left=BinaryOpNode(left,op,right)
        return left
    
    def parse_factor(self):
        left=self.parse_unary()
        while self.current() and self.current()[0] in ("TIMES","DIVIDED","MODULO"):
            op=self.current()[0]
            self.eat()
            right=self.parse_unary()
            left=BinaryOpNode(left,op,right)
        return left

    def parse_unary(self):
        if self.current() and self.current()[0]=="NEGATE":
            self.eat()
            return UnaryNode(self.parse_unary())
        return self.parse_primary()
    
    def parse_primary(self):
        token=self.current()

        if token is None:
            raise Exception("Unexpected end of input")
        
        if token[0]=="NOGIRLMATH":
            self.eat()
            expr=self.parse_expression()
            return NoGirlMath(expr)
        
        if token[0]=="INT":
            self.eat()
            return NumberNode(token[1])
        
        if token[0]=="STRING":
            self.eat()
            return StringNode(token[1])
        
        if token[0]=="VARIABLE":
            name=token[1]
            args=[]
            self.eat()
            if self.current() and self.current()[0]=="LPAREN":
                self.eat()
                if self.current() and self.current()[0] == "RPAREN":
                    return CallNode(name,args)
                while True:
                    expr=self.parse_expression()
                    args.append(expr)
                    if self.current() and self.current()[0]=="RPAREN":
                        break
                    self.expect("COMMA")
                self.expect("RPAREN")
                #if self.current() and self.current()[0]=="END":
                #    self.eat()
                return CallNode(name,args)
            return VariableNode(token[1])
        
        if token[0]=="LPAREN":
            self.eat()
            expr=self.parse_expression()
            if self.current() and self.current()[0]=="RPAREN":
                self.eat()
                return expr
            else:
                raise Exception("Missing ')'")
        raise Exception(f"Unexpected token {token}")
    
def evaluate(node,variables=None,realMath=False):
    if variables is None:
        variables={}
    
    if isinstance(node,NoGirlMath):
        return evaluate(node.expr,variables,realMath=True)

    if isinstance(node,NumberNode):
        return node.value
    
    if isinstance(node,StringNode):
        return node.value
    if isinstance(node,VariableNode):
        if node.name in variables:
            return variables[node.name]
        else:
            raise Exception(f"Undefined variable: {node.name}")
    if isinstance(node, UnaryNode):
        value=evaluate(node.expr,variables,realMath)
        return not value
    
    if isinstance(node, CallNode):
        return execute(node, variables,realMath)
    
    if isinstance(node,BinaryOpNode):
        
        left=evaluate(node.left,variables,realMath)
        right=evaluate(node.right,variables,realMath)

        real_result=None
        # math
        if node.op == "PLUS":
            if isinstance(left,str) or isinstance(right,str):
                real_result= str(left)+str(right)
            else:
                real_result= left + right
        if node.op == "MINUS":
            real_result= left - right
        if node.op == "TIMES":
            real_result= left * right
        if node.op == "DIVIDED":
            real_result= left / right
        if node.op == "MODULO":
            real_result= left % right

        # comparison
        if node.op == "GRATER":
            real_result= left > right
        if node.op == "GRATERE":
            real_result= left >= right
        if node.op == "LESSER":
            real_result= left < right
        if node.op == "LESSERE":
            real_result= left <= right
        if node.op == "EQUEL":
            real_result= left == right
        if node.op == "NEQUEL":
            real_result= left != right

        # logical
        if node.op == "AND":
            real_result= left and right
        if node.op == "OR":
            real_result= left or right

        if not realMath:
            if isinstance(real_result,str):
                return random.random()
            return random.randint(0,real_result)
        return real_result
    raise Exception (f"Unknown node: {node}")
    
functions = {}
def execute(node,variables=None,realMath=False):
    if variables is None:
        variables = {}
    #-------------BLOCK--------------
    if isinstance(node,BlockNode):
        for stmt in node.statements:
            execute(stmt,variables,realMath);
        return
    
    #--------VAR DECLARE AND ASSIGN-------
    if isinstance(node,VarDecAndAssignNode):
        variables[node.name]=None
        value=evaluate(node.value,variables,realMath)
        variables[node.name]=value
        return
    #--------VAR DECLARE-------------
    if isinstance(node,VarDeclNode):
        variables[node.name]=None
        return
    
    #---------VAR ASSIGN-------------
    if isinstance(node,VarAssignNode):
        if node.name not in variables:
            raise Exception(f"Undefined variable {node.name}")
        value=evaluate(node.value,variables,realMath)
        variables[node.name]=value
        return

    #---------PRINT------------------
    if isinstance(node,PrintNode):
        value=evaluate(node.expr,variables,realMath)
        if node.newline:
            end="\n"
        else:
            end=""
        print(value,end=end)
        return
    
    #----------PRINT NEW LINE--------
    if isinstance(node,PrintNewLineNode):
        print(end="\n")
        return

    #--------INPUT-------------------
    if isinstance(node,InputNode):
        
        if node.var not in variables:
            raise Exception(f"Undefined variable {node.var}")
        inputData=input()
        if not inputData.isalpha():
            if "." in inputData:
                variables[node.var]=float(inputData)
            else:
                variables[node.var]=int(inputData)
        else:
            variables[node.var]=str(inputData)
        return
    #------IF------------------------
    if isinstance(node,IfNode):
        expr=evaluate(node.condition,variables,realMath)
        if expr:
            execute(node.body,variables,realMath)
        return
    
    #-------IF ELSE------------
    if isinstance(node,IfElseNode):
        expr=evaluate(node.ifCondition,variables,realMath)
        if expr:
            execute(node.ifBody,variables,realMath)
        else:    
            execute(node.elseBody,variables,realMath)
        return
    
    #--------WHILE--------------
    if isinstance(node,WhileNode):
        while evaluate(node.condition,variables,realMath):
            execute(node.body,variables,realMath)
        return
    #-------FUNCTION------------
    if isinstance(node,FunctionNode):
        functions[node.name]=node

        return
    #--------FUNCTION CALL------
    if isinstance(node,CallNode):   
        if node.name not in functions:
            raise Exception(f"Function '{node.name}' not declated!")
        func=functions[node.name]
        if len(func.args)!=len(node.args):
            raise Exception(f"Wront number of arguments")
        values = [evaluate(arg, variables,realMath) for arg in node.args]
        local_vars={}
        local_vars=variables.copy()

        for i, key in enumerate(func.args.keys()):
            local_vars[key]=values[i]
        
        try:
            execute(func.body,local_vars,realMath)
        except ReturnException as r:
            return r.value
        return None
    #-------RETURN--------------
    if isinstance(node,ReturnNode):
        value=evaluate(node.expr,variables,realMath)
        raise ReturnException(value)

    raise Exception (f"Unknown node: {node}")

    
        