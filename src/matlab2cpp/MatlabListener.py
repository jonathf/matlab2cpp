"""
Build token tree from matlab-code
"""

from antlr4 import *

import collection as col

class MatlabListener(ParseTreeListener):

    def enterProgram(self, ctx):
        ctx.program = col.Program()
        ctx.program["backend"] = "program"
        ctx.program["names"] = []

        includes = col.Includes(ctx.program)
        includes["backend"] = "program"
        includes["names"] = []

        i1 = col.Include(includes, "armadillo")
        i1["value"] = "#include <armadillo>"
        i1["backend"] = "program"

        i2 = col.Include(includes, "usingarma")
        i2["value"] = "using namespace arma;"
        i2["backend"] = "program"

        func = col.Func(ctx.program, "main")
        declares = col.Declares(func)
        returns = col.Returns(func)
        params = col.Params(func)

        func["backend"] = "func_return"
        declares["backend"] = "func_return"
        returns["backend"] = "func_return"
        params["backend"] = "func_return"

        declares["names"] = []
        returns["names"] = ["_retval"]
        params["names"] = ["argc", "argv"]

        var = col.Var(returns, "_retval")
        var.type("int")
        var["backend"] = "int"
        var.declare(var)

        argc = col.Var(params, "argc")
        argc.type("int")
        argc["backend"] = "int"

        argv = col.Var(params, "argv")
        argv.type("char")
        argv["backend"] = "char"
        argv["pointer"] = 2

        ctx.node = func

    def exitProgram(self, ctx):
        ctx.program["names"].append("main")
        cs = ctx.program.children
        ctx.program.children = cs[:1] + cs[2:] + cs[1:2]

        block = ctx.node[3]
        assign = col.Assign(block)
        var = col.Var(assign, "_retvar")
        var.type("int")
        i = col.Int(assign, "0")
        i.type("int")
        i["backend"] = "int"

    def enterFunction(self, ctx):
        program = ctx.parentCtx.node.program
        name = ctx.ID().getText()
        program["names"].append(name)
        ctx.node = col.Func(program, name)
        declares = col.Declares(ctx.node)
        declares["names"] = []

    def exitFunction(self, ctx):

        if len(ctx.node[1]) == 1:
            ctx.node["backend"] = "func_return"
            ctx.node[0]["backend"] = "func_return"
            ctx.node[1]["backend"] = "func_return"
            ctx.node[2]["backend"] = "func_return"
        else:
            ctx.node["backend"] = "func_returns"
            ctx.node[0]["backend"] = "func_returns"
            ctx.node[1]["backend"] = "func_returns"
            ctx.node[2]["backend"] = "func_returns"

        for var in ctx.node[1][:]:
            var.declare()

    def enterFunction_returns(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Returns(pnode)
        ctx.node["names"] = []
        for n in xrange((ctx.getChildCount()-2)/2 or 1):
            name = ctx.ID(n).getText()
            col.Var(ctx.node, name)
            ctx.node["names"].append(name)

    def exitFunction_returns(self, ctx):
        pass

    def enterFunction_params(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Params(pnode)
        ctx.node["names"] = []
        for n in xrange((ctx.getChildCount()+1)/2):
            name = ctx.ID(n).getText()
            col.Var(ctx.node, name)
            ctx.node["names"].append(name)

    def exitFunction_params(self, ctx):
        pass

    def enterCodeline(self, ctx):
        ctx.node = ctx.parentCtx.node

    def exitCodeline(self, ctx):
        pass

    def enterCodeblock(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Block(pnode)
        ctx.node["backend"] = "code_block"

    def exitCodeblock(self, ctx):
        pass

    def enterBranch(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Branch(pnode)
        ctx.node["backend"] = "code_block"

    def exitBranch(self, ctx):
        pass

    def enterBranch_if(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.If(pnode)
        ctx.node["backend"] = "code_block"

    def exitBranch_if(self, ctx):
        pass

    def enterBranch_elif(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Elif(pnode)
        ctx.node["backend"] = "code_block"

    def exitBranch_elif(self, ctx):
        pass

    def enterBranch_else(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Else(pnode)
        ctx.node["backend"] = "code_block"

    def exitBranch_else(self, ctx):
        pass

    def enterCondition(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Cond(pnode)
        ctx.node["backend"] = "code_block"

    def exitCondition(self, ctx):
        pass

    def enterSwitch_(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Switch(pnode)
        ctx.node["backend"] = "code_block"

    def exitSwitch_(self, ctx):
        pass

    def enterSwitch_case(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Case(pnode)
        ctx.node["backend"] = "code_block"

    def exitSwitch_case(self, ctx):
        pass

    def enterSwitch_otherwise(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Otherwise(pnode)
        ctx.node["backend"] = "code_block"

    def exitSwitch_otherwise(self, ctx):
        pass

    def enterLoop(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.For(pnode)
        ctx.node["backend"] = "code_block"

    def exitLoop(self, ctx):
        pass

    def enterLoop_range(self, ctx):
        pnode = ctx.parentCtx.node
        col.Var(pnode, ctx.ID().getText()).declare()
        ctx.node = pnode
        ctx.node["backend"] = "code_block"

    def exitLoop_range(self, ctx):
        pass

    def enterWloop(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.While(pnode)
        ctx.node["backend"] = "code_block"

    def exitWloop(self, ctx):
        pass

    def enterTry_(self, ctx):
        pnode = ctx.parentCtx.node
        node = col.Tryblock(pnode)
        ctx.node = col.Try(node)
        ctx.node["backend"] = "code_block"

    def exitTry_(self, ctx):
        pass

    def enterCatchid(self, ctx):
        ppnode = ctx.parentCtx.parentCtx.node
        ctx.node = col.Catch(ppnode, ctx.ID().getText())
        ctx.node["backend"] = "code_block"

    def exitCatchid(self, ctx):
        pass

    def enterCatch_(self, ctx):
        ppnode = ctx.parentCtx.parentCtx.node
        ctx.node = col.Catch(ppnode)
        ctx.node["backend"] = "code_block"

    def exitCatch_(self, ctx):
        pass

    def enterStatement(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Statement(pnode)
        ctx.node["backend"] = "code_block"

    def exitStatement(self, ctx):
        pass

    def enterAssign(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Assign(pnode)
        col.Var(ctx.node, ctx.ID().getText()).declare()
        ctx.node["backend"] = "unknown"

    def exitAssign(self, ctx):
        pass

    def enterAssigns(self, ctx):
        pnode = ctx.parentCtx.node
        assigns = col.Assigns(pnode)
        assigns["backend"] = "code_block"

        assigned = col.Assigned(assigns)
        assigned["backend"] = "code_block"
        for i in xrange((ctx.getChildCount()-2)/2):
            col.Var(assigned, ctx.ID(i).getText()).declare()

        ctx.node = assigns

    def exitAssigns(self, ctx):
        name = ctx.node[1]["name"]
        if name:
            ctx.node["name"] = name

    def enterSet1(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Set(pnode, ctx.ID().getText())
        ctx.node["backend"] = "unknown"

    def exitSet1(self, ctx):
        pass

    def enterSet2(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Set2(pnode, ctx.ID().getText())
        ctx.node["backend"] = "unknown"

    def exitSet2(self, ctx):
        pass

    def enterSet3(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Set3(pnode, ctx.ID().getText())
        ctx.node["backend"] = "unknown"

    def exitSet3(self, ctx):
        pass

    def enterSets(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Sets(pnode)
        ctx.node["backend"] = "code_block"

    def exitSets(self, ctx):
        pass

    def enterExpr(self, ctx):
        ctx.node = ctx.parentCtx.node

    def exitExpr(self, ctx):
        pass

    def enterInfix(self, ctx):

        opr = ctx.OPR().getText()
        parent = ctx.parentCtx
        if hasattr(parent, "opr") and opr == parent.opr:
            ctx.node = parent.node
        else:
            pnode = parent.node

            if opr == "||":     node = col.Lor(pnode)
            elif opr == "&&":   node = col.Land(pnode)
            elif opr == "|":    node = col.Bor(pnode)
            elif opr == "&":    node = col.Band(pnode)
            elif opr == "%%":   node = col.Eq(pnode)
            elif opr == "<=":   node = col.Le(pnode)
            elif opr == ">=":   node = col.Ge(pnode)
            elif opr == "<":    node = col.Lt(pnode)
            elif opr == ">":    node = col.Gt(pnode)
            elif opr == "<>":   node = col.Ne(pnode)
            elif opr == ":":    node = col.Colon(pnode)
            elif opr == "/":    node = col.Div(pnode)
            elif opr == "./":   node = col.Eldiv(pnode)
            elif opr == "\\":   node = col.Rdiv(pnode)
            elif opr == ".\\":  node = col.Elrdiv(pnode)
            elif opr == "*":    node = col.Mul(pnode)
            elif opr == ".*":   node = col.Elmul(pnode)
            elif opr == "^":    node = col.Exp(pnode)
            elif opr == ".^":   node = col.Elexp(pnode)
            elif opr == "+":
#                  rhs = ctx.getChild(2)
#                  if hasattr(rhs, "PRE") and rhs.PRE().getText() == "-":
#                      node = col.Minus(pnode)
#                  else:
                    node = col.Plus(pnode)

            ctx.node = node
            ctx.node["backend"] = "expression"
            ctx.opr = opr

    def exitInfix(self, ctx):
        pass

    def enterIfloat(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Ifloat(pnode, ctx.getText())
        ctx.node["backend"] = "ifloat"

    def exitIfloat(self, ctx):
        pass

    def enterFloat(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Float(pnode, ctx.getText())
        ctx.node.type("float")
        ctx.node["backend"] = "float"

    def exitFloat(self, ctx):
        pass

    def enterEnd(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.End(pnode)
        ctx.node["backend"] = "expression"

    def exitEnd(self, ctx):
        pass

    def enterGet1(self, ctx):
        pnode = ctx.parentCtx.node
        name = ctx.ID().getText()
        ctx.node = col.Get(pnode, name)
        ctx.node["backend"] = "unknown"

    def exitGet1(self, ctx):
        pass

    def enterGet2(self, ctx):
        pnode = ctx.parentCtx.node
        name = ctx.ID().getText()
        ctx.node = col.Get2(pnode, name)
        ctx.node["backend"] = "unknown"

    def exitGet2(self, ctx):
        pass

    def enterGet3(self, ctx):
        pnode = ctx.parentCtx.node
        name = ctx.ID().getText()
        ctx.node = col.Get3(pnode, name)
        ctx.node["backend"] = "unknown"

    def exitGet3(self, ctx):
        pass

    def enterPrefix(self, ctx):
        pre = ctx.PRE().getText()
        parent = ctx.parentCtx
        pnode = parent.node
        if pre == "-":
            if hasattr(parent, "opr") and \
                    parent.opr == "+":
                ctx.node = pnode
            else:
                ctx.node = col.Neg(pnode)
        else:
            ctx.node = col.Not(pnode)
        ctx.node["backend"] = "expression"

    def exitPrefix(self, ctx):
        pass

    def enterParen(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Paren(pnode)
        ctx.node["backend"] = "expression"

    def exitParen(self, ctx):
        pass

    def enterIint(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Iint(pnode, ctx.IINT().getText())
        ctx.node["backend"] = "iint"

    def exitIint(self, ctx):
        pass

    def enterString(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.String(pnode, ctx.STRING().getText())
        ctx.node["backend"] = "string"

    def exitString(self, ctx):
        pass

    def enterVar(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Var(pnode, ctx.ID().getText())
        ctx.node.declare()
        ctx.node["backend"] = "unknown"

    def exitVar(self, ctx):
        pass

    def enterInt(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Int(pnode, ctx.INT().getText())
        ctx.node.type("int")
        ctx.node["backend"] = "int"

    def exitInt(self, ctx):
        pass

    def enterPostfix(self, ctx):
        pnode = ctx.parentCtx.node
        post = ctx.POST().getText()
        if post == "'":
            ctx.node = col.Ctranspose(pnode)
        else:
            ctx.node = col.Transpose(pnode)
        ctx.node["backend"] = "expression"

    def exitPostfix(self, ctx):
        pass

    def enterMatri(self, ctx):
        ctx.node = ctx.parentCtx.node

    def exitMatri(self, ctx):
        pass

    def enterLlist(self, ctx):
        ctx.node = ctx.parentCtx.node

    def exitLlist(self, ctx):
        pass

    def enterListone(self, ctx):
        ctx.node = ctx.parentCtx.node

    def exitListone(self, ctx):
        pass

    def enterListmore(self, ctx):
        ctx.node = ctx.parentCtx.node

    def exitListmore(self, ctx):
        pass

    def enterListall(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.All(pnode)
        ctx.node["backend"] = "expression"

    def exitListall(self, ctx):
        pass

    def enterMatrix(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Matrix(pnode)
        ctx.node["backend"] = "matrix"

    def exitMatrix(self, ctx):
        pass

    def enterMatrix_(self, ctx):
        ctx.node = ctx.parentCtx.node

    def exitMatrix_(self, ctx):
        pass

    def enterVector(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Vector(pnode)
        ctx.node["backend"] = "matrix"

    def exitVector(self, ctx):
        pass
