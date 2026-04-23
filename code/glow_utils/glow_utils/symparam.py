########################################################################
#
# Copyright 2026 Dr. Dušan Grujić (dusan.grujic@etf.bg.ac.rs)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################

import ast
import _ast
from collections import ChainMap

class Symparam:
    """
    Symbolic parameter class, used to evaluate circuit parameters.

    Global parameters are stored in a dictionary:
    {paramName : paramInstance}
    where paramName must be unique, and paramInstance is an instace of Symparam class.
    """
    # --------------------------------------------------------------------------
    class variableExpander(ast.NodeTransformer):
       """
       Subclass to walk the nodes of AST expression and perform variable expansion.
       """
       def __init__(self, paramDict, fnDict, fullExpansion=True):
            """
            Initialize parameter dictionary
            If fullExpansion is False, the variable expansion is performed up to the last symbol,
            i.e. symbolic substitution is pefrormed.
            """
            self.paramDict = paramDict
            self.fnDict = fnDict
            self.fullExpansion = fullExpansion
                      
       def visit_Name(self, node):
            """
            We are at named node, which might be a variable or a function node.
            node.id contains the name which should be expanded from parameter dictionary.
            """
            parExpr = self.paramDict.get(node.id)  # Get parameter expression
            if parExpr == None:
                parExpr = self.fnDict.get(node.id) # Get function
                if callable(parExpr):                  # Check if current node is a function
                    return node                        # This node is a function, do not try to expand it
                else:
                    raise ValueError("Unknown symbol: "+str(node.id))
            # Add exception handling
            parExprParsed = ast.parse(str(parExpr), mode='eval')  # Parse parameter expression
            #if not(isinstance(parExprParsed.body, _ast.Num) and not self.fullExpansion):
            if not(isinstance(parExprParsed.body, _ast.Constant) and not self.fullExpansion):
                # If the node does not evaluate to number continue recursive traversing. 
                # When full expansion is not requested, stop the recursion if the symbol evaluates to numeric value.
                expr = self.visit(parExprParsed) # Recursively evaluate parameters
                node = expr.body
            return node
    # --------------------------------------------------------------------------
    def printAstExpression(self, astTree):
        """
        Print AST tree to string representation
        """
        code = self.astToCode(astTree)
        return code.exprString

    class astToCode(ast.NodeVisitor):
        """
        Subclass to walk the nodes of AST tree and emit the Python code of expression
        """
        binOp = { _ast.Add      : '+',
                  _ast.Mult     : '*',
                  _ast.LShift   : '<<',
                  _ast.BitAnd   : '&',
                  _ast.Sub      : '-',
                  _ast.Div      : '/',
                  _ast.RShift   : '>>',
                  _ast.BitOr    : '|',
                  _ast.Mod      : '%',
                  _ast.BitXor   : '^',
                  _ast.FloorDiv : '//',
                  _ast.Pow      : '**'
                  }

        boolOp = { _ast.And     : 'and',
                   _ast.Or      : 'or',
                  }

        cmpOp =  {  _ast.Eq     : '==',
                    _ast.Gt     : '>',
                    _ast.GtE    : '>=',
                    _ast.In     : 'in',
                    _ast.Is     : 'is',
                    _ast.NotEq  : '!=',
                    _ast.Lt     : '<',
                    _ast.LtE    : '<=',
                    _ast.NotIn  : 'not_in',
                    _ast.IsNot  : 'is_not'
                  }

        unaryOp = { _ast.UAdd   : '+',
                    _ast.USub   : '-',
                    _ast.Invert : '~',
                    _ast.Not    : 'not'
                  }

        def __init__(self, astTree):
            """
            astToCode constructor.
            Traverses the AST tree and constructs the string expression in exprString.
            If an unimplemented node is encountered an exception is raised.
            """
            self.astTree = astTree  # AST tree to traverse
            self.exprString = ""    # Expression string
            self.visit(astTree)     # Start the AST tree traversing. Nodes emit the string expression to expString
            
        def visit_Expression(self, node):
            self.visit(node.body)   # Just visit the next node

        def visit_Name(self, node):
            self.exprString += node.id  # Append variable name
            
        def visit_Str(self, node):
            self.exprString += repr(node.s) # Append string value
            
        def visit_Num(self, node):
            num = node.n
            if num<0:
                numStr = '('+repr(num)+')'  # power operator has precedce, so (-x)**y yields correct result
            else:
                numStr = repr(num)
            self.exprString += numStr
        
        def visit_BinOp(self, node):
            self.exprString += '('
            self.visit(node.left)
            self.exprString += self.binOp[node.op.__class__]    # Retrieve the string representation of operator
            self.visit(node.right)
            self.exprString += ')'

        def visit_UnaryOp(self, node):
            self.exprString += '('
            self.exprString += self.unaryOp[node.op.__class__]    # Retrieve the string representation of operator            
            self.exprString += '('
            self.visit(node.operand)
            self.exprString += ')'                        
            self.exprString += ')'

        def visit_Call(self, node):
            self.visit(node.func)
            self.exprString += '('
            i = 0
            for arg in node.args:
                if i>0:
                    self.exprString += ','
                self.visit(arg)
                i += 1
            i = 0
            for keyword in node.keywords:
                if i>0:
                    self.exprString += ','
                self.visit(keyword.arg)
                self.exprString += '='
                self.visit(keyword.value)
                i += 1
            if node.starargs:
                self.exprString += ', *'
                self.visit(starargs)
            if node.kwargs:
                self.exprString += ', **'
                self.visit(kwargs)
            self.exprString += ')'
        
        def generic_visit(self, node):  # Catch the undefined node types
            raise ValueError("Node type "+str(node.__class__)+" not implemented")
    # --------------------------------------------------------------------------    
    def __init__(self, paramDict, fnDict):
        """
        Parameter evaluator class constructor.
        ParamDict and fnDict will be used in subsequent parameter evaluation.
        """
        self.paramDict = paramDict
        self.fnDict = fnDict
        
    def substitute(self, paramExpr, instanceFns = {}):
        """
        Perform symbolic substitution of variables.
        The result is a string expression where all symbols evaluate to numbers.
        Argument instanceFns is per-instance function dictionary
        """
        if isinstance(paramExpr, float):
            return paramExpr
        
        if isinstance(paramExpr, int):
            return paramExpr
        
        parsedExpr = ast.parse(paramExpr, mode='eval')
        expr = self.variableExpander(self.paramDict, ChainMap(self.fnDict, instanceFns), fullExpansion=False).visit(parsedExpr)
        return self.printAstExpression(expr)

    def evaluate(self, paramExpr, instanceFns = {}):
        """
        Evaluate parameter expression in the scope of parameters given in dictionary paramDict and functions given in dictionary fnDict.
        Argument instanceFns is per-instance function dictionary
        The result is a number.
        """
        if isinstance(paramExpr, float):
            return paramExpr
        
        if isinstance(paramExpr, int):
            return paramExpr
        
        parsedExpr = ast.parse(paramExpr, mode='eval')
        expr = self.variableExpander(self.paramDict, ChainMap(self.fnDict, instanceFns)).visit(parsedExpr)
        code = compile(expr, 'temp', 'eval')
        # If all is ok, while we get here all parameters are already evaluated,
        # only the evaluation of functions is remaining
        value = eval(code, {}, ChainMap(self.fnDict, instanceFns))
        return value

