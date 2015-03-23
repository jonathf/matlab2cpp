"""
Build token tree from matlab-code
"""

from antlr4 import *

import collection as col

class MatlabListener(ParseTreeListener):

    def enterProgram(self, ctx):
        ctx.program = col.Program()

        includes = col.Includes(ctx.program)

        i1 = col.Include(includes, "armadillo")
        i1["value"] = "#include <armadillo>"

        i2 = col.Include(includes, "usingarma")
        i2["value"] = "using namespace arma;"

        func = col.Func(ctx.program, "main")
        declares = col.Declares(func)
        returns = col.Returns(func)
        params = col.Params(func)

        func["backend"] = "func_return"
        declares["backend"] = "func_return"
        returns["backend"] = "func_return"
        params["backend"] = "func_return"

        var = col.Var(returns, "_retval")
        var.type("int")
        var.declare()

        argc = col.Var(params, "argc")
        argc.type("int")

        argv = col.Var(params, "argv")
        argv.type("char")
        argv["backend"] = "char"
        argv.pointer(2)

        ctx.node = func

    def exitProgram(self, ctx):
        cs = ctx.program.children[1:]

        cs = cs[1:] + cs[:1]
        for i in xrange(len(cs)-1):
            if cs[i]["name"][0] == "_":
                cs = cs[i:i+1] + cs[:i] + cs[i+1:]

        ctx.program.children = [ctx.program[0]] + cs
        ctx.program["names"] = [n["name"] for n in ctx.program]

        if len(ctx.node) != 4:
            block = col.Block(ctx.node)

        block = ctx.node[3]
        assign = col.Assign(block)
        var = col.Var(assign, "_retval")
        var.type("int")
        i = col.Int(assign, "0")

    def enterFunction(self, ctx):
        program = ctx.parentCtx.node.program
        name = ctx.ID().getText()

        ctx.node = col.Func(program, name)
        col.Declares(ctx.node)

        if ctx.function_returns() is None:
            col.Returns(ctx.node)

            if ctx.function_params() is None:
                col.Params(ctx.node)

    def exitFunction(self, ctx):

        node = ctx.node

        if len(node[1]) == 1:
            node["backend"] = "func_return"
            node[0]["backend"] = "func_return"
            node[1]["backend"] = "func_return"
            node[2]["backend"] = "func_return"
        else:
            node["backend"] = "func_returns"
            node[0]["backend"] = "func_returns"
            node[1]["backend"] = "func_returns"
            node[2]["backend"] = "func_returns"

        for var in node[1][:]:
            var.declare()

    def enterFunction_returns(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Returns(pnode)

        count = ctx.getChildCount()
        for n in xrange((count-2)/2 or 1):
            name = ctx.ID(n).getText()
            col.Var(ctx.node, name)

        if ctx.parentCtx.function_params() is None:
            col.Params(pnode)

    def exitFunction_returns(self, ctx):
        pass

    def enterFunction_params(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Params(pnode)
        for n in xrange((ctx.getChildCount()+1)/2):
            name = ctx.ID(n).getText()
            col.Var(ctx.node, name)

    def exitFunction_params(self, ctx):
        pass

    def enterLambda_func(self, ctx):
        pnode = ctx.parentCtx.node
        program = pnode.program
        name = "_%s_%03d" % (pnode.func["name"], len(program))

        ctx.node = func = col.Func(program, name)
        col.Declares(func)
        col.Returns(func)

    def exitLambda_func(self, ctx):
        func = ctx.node.func
        declares, returns, params, block = func

        func["backend"] = "func_lambda"
        returns["backend"] = "func_lambda"
        params["backend"] = "func_lambda"
        declares["backend"] = "func_lambda"

        var = col.Var(returns, "_retval")
        var.declare()

        name = ctx.ID().getText()
        pnode = ctx.parentCtx.node

        lamb = col.Lambda(pnode, name)
        lamb.type("func_lambda")
        lamb.declare()
        lamb.reference.reference = func

    def enterLambda_params(self, ctx):
        func = ctx.parentCtx.node
        params = col.Params(func)
        for n in xrange((ctx.getChildCount()+1)/2):
            name = ctx.ID(n).getText()
            col.Var(params, name)

        block = col.Block(func)

        assign = col.Assign(block)
        ctx.parentCtx.node = assign
        col.Var(assign, "_retval")

    def exitLambda_params(self, ctx):
        pass

    def enterCodeline(self, ctx):
        ctx.node = ctx.parentCtx.node

    def exitCodeline(self, ctx):
        pass

    def enterCodeblock(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Block(pnode)

    def exitCodeblock(self, ctx):
        pass

    def enterBranch(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Branch(pnode)

    def exitBranch(self, ctx):
        pass

    def enterBranch_if(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.If(pnode)

    def exitBranch_if(self, ctx):
        pass

    def enterBranch_elif(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Elif(pnode)

    def exitBranch_elif(self, ctx):
        pass

    def enterBranch_else(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Else(pnode)

    def exitBranch_else(self, ctx):
        pass

    def enterCondition(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Cond(pnode)

    def exitCondition(self, ctx):
        pass

    def enterSwitch(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Switch(pnode)

    def exitSwitch(self, ctx):
        pass

    def enterSwitch_case(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Case(pnode)

    def exitSwitch_case(self, ctx):
        pass

    def enterSwitch_otherwise(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Otherwise(pnode)

    def exitSwitch_otherwise(self, ctx):
        pass

    def enterLoop(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.For(pnode)
        col.Var(ctx.node, ctx.ID().getText()).declare()

    def exitLoop(self, ctx):
        pass

#      def enterLoop_range(self, ctx):
#          pnode = ctx.parentCtx.node
#          col.Var(pnode, ctx.ID().getText()).declare()
#          ctx.node = pnode

    def enterWloop(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.While(pnode)

    def exitWloop(self, ctx):
        pass

    def enterTry(self, ctx):
        pnode = ctx.parentCtx.node
        node = col.Tryblock(pnode)
        ctx.node = col.Try(node)

    def exitTry(self, ctx):
        pass

    def enterCatchid(self, ctx):
        ppnode = ctx.parentCtx.parentCtx.node
        ctx.node = col.Catch(ppnode, ctx.ID().getText())

    def exitCatchid(self, ctx):
        pass

    def enterCatch_(self, ctx):
        ppnode = ctx.parentCtx.parentCtx.node
        ctx.node = col.Catch(ppnode)

    def exitCatch_(self, ctx):
        pass

    def enterStatement(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Statement(pnode)

    def exitStatement(self, ctx):
        pass

    def enterAssignment(self, ctx):
        ctx.node = ctx.parentCtx.node

    def exitAssignment(self, ctx):
        pass

    def enterAssign(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Assign(pnode)
        col.Var(ctx.node, ctx.ID().getText()).declare()

    def exitAssign(self, ctx):
        pass

    def enterAssigns(self, ctx):
        pnode = ctx.parentCtx.node
        assigns = col.Assigns(pnode)

        assigned = col.Assigned(assigns)
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
        ctx.node.declare()

    def exitSet1(self, ctx):
        pass

    def enterSet2(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Set2(pnode, ctx.ID().getText())
        ctx.node.declare()

    def exitSet2(self, ctx):
        pass

    def enterSet3(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Set3(pnode, ctx.ID().getText())
        ctx.node.declare()

    def exitSet3(self, ctx):
        pass

    def enterSets(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Sets(pnode)

    def exitSets(self, ctx):
        pass

    def enterExpr(self, ctx):
        ctx.node = ctx.parentCtx.node

    def exitExpr(self, ctx):
        pass

    def enterLor(self, ctx):
        if ctx.parentCtx.node["class"] == "Lor":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Lor(ctx.parentCtx.node)

    def exitLor(self, ctx):
        pass


    def enterLand(self, ctx):
        if ctx.parentCtx.node["class"] == "Land":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Land(ctx.parentCtx.node)

    def exitLand(self, ctx):
        pass


    def enterBor(self, ctx):
        if ctx.parentCtx.node["class"] == "Bor":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Bor(ctx.parentCtx.node)

    def exitBor(self, ctx):
        pass


    def enterBand(self, ctx):
        if ctx.parentCtx.node["class"] == "Band":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Band(ctx.parentCtx.node)

    def exitBand(self, ctx):
        pass


    def enterEq(self, ctx):
        if ctx.parentCtx.node["class"] == "Eq":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Eq(ctx.parentCtx.node)

    def exitEq(self, ctx):
        pass


    def enterLe(self, ctx):
        if ctx.parentCtx.node["class"] == "Le":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Le(ctx.parentCtx.node)

    def exitLe(self, ctx):
        pass


    def enterGe(self, ctx):
        if ctx.parentCtx.node["class"] == "Ge":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Ge(ctx.parentCtx.node)

    def exitGe(self, ctx):
        pass


    def enterLt(self, ctx):
        if ctx.parentCtx.node["class"] == "Lt":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Lt(ctx.parentCtx.node)

    def exitLt(self, ctx):
        pass


    def enterGt(self, ctx):
        if ctx.parentCtx.node["class"] == "Gt":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Gt(ctx.parentCtx.node)

    def exitGt(self, ctx):
        pass


    def enterNe(self, ctx):
        if ctx.parentCtx.node["class"] == "Ne":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Ne(ctx.parentCtx.node)

    def exitNe(self, ctx):
        pass


    def enterColon(self, ctx):
        if ctx.parentCtx.node["class"] == "Colon":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Colon(ctx.parentCtx.node)

    def exitColon(self, ctx):
        pass


    def enterDiv(self, ctx):
        if ctx.parentCtx.node["class"] == "Div":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Div(ctx.parentCtx.node)

    def exitDiv(self, ctx):
        pass


    def enterEldiv(self, ctx):
        if ctx.parentCtx.node["class"] == "Eldiv":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Eldiv(ctx.parentCtx.node)

    def exitEldiv(self, ctx):
        pass


    def enterRdiv(self, ctx):
        if ctx.parentCtx.node["class"] == "Rdiv":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Rdiv(ctx.parentCtx.node)

    def exitRdiv(self, ctx):
        pass


    def enterElrdiv(self, ctx):
        if ctx.parentCtx.node["class"] == "Elrdiv":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Elrdiv(ctx.parentCtx.node)

    def exitElrdiv(self, ctx):
        pass


    def enterMul(self, ctx):
        if ctx.parentCtx.node["class"] == "Mul":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Mul(ctx.parentCtx.node)

    def exitMul(self, ctx):
        pass


    def enterElmul(self, ctx):
        if ctx.parentCtx.node["class"] == "Elmul":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Elmul(ctx.parentCtx.node)

    def exitElmul(self, ctx):
        pass


    def enterExp(self, ctx):
        if ctx.parentCtx.node["class"] == "Exp":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Exp(ctx.parentCtx.node)

    def exitExp(self, ctx):
        pass


    def enterElexp(self, ctx):
        if ctx.parentCtx.node["class"] == "Elexp":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Elexp(ctx.parentCtx.node)

    def exitElexp(self, ctx):
        pass


    def enterPlus(self, ctx):
        if ctx.parentCtx.node["class"] == "Plus":
            ctx.node = ctx.parentCtx.node
        else:
            ctx.node = col.Plus(ctx.parentCtx.node)

    def exitPlus(self, ctx):
        pass


    def enterMinus(self, ctx):
        ctx.node = col.Neg(ctx.parentCtx.node)

    def exitMinus(self, ctx):
        pass


    def enterNegate(self, ctx):
        ctx.node = col.Not(ctx.parentCtx.node)

    def exitNegate(self, ctx):
        pass


    def enterIfloat(self, ctx):
        pnode = ctx.parentCtx.node
        val = ctx.IFLOAT().getText()
        if "d" in val: val = val.replace("d", "e")
        if "D" in val: val = val.replace("D", "e")
        if "E" in val: val = val.replace("E", "e")
        ctx.node = col.Ifloat(pnode, val)

    def exitIfloat(self, ctx):
        pass

    def enterFloat(self, ctx):
        pnode = ctx.parentCtx.node
        val = ctx.FLOAT().getText()
        if "d" in val: val = val.replace("d", "e")
        if "D" in val: val = val.replace("D", "e")
        if "E" in val: val = val.replace("E", "e")
        ctx.node = col.Float(pnode, val)

    def exitFloat(self, ctx):
        pass

    def enterEnd(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.End(pnode)

    def exitEnd(self, ctx):
        pass

    def enterGet1(self, ctx):
        pnode = ctx.parentCtx.node
        name = ctx.ID().getText()
        ctx.node = col.Get(pnode, name)

    def exitGet1(self, ctx):
        pass

    def enterGet2(self, ctx):
        pnode = ctx.parentCtx.node
        name = ctx.ID().getText()
        ctx.node = col.Get2(pnode, name)

    def exitGet2(self, ctx):
        pass

    def enterGet3(self, ctx):
        pnode = ctx.parentCtx.node
        name = ctx.ID().getText()
        ctx.node = col.Get3(pnode, name)

    def exitGet3(self, ctx):
        pass

    def enterPrefix(self, ctx):
        pre = ctx.PRE().getText()
        parent = ctx.parentCtx
        pnode = parent.node
        if pre == "-":
#              if hasattr(parent, "opr") and \
#                      parent.opr == "+":
#                  ctx.node = pnode
#              else:
                ctx.node = col.Neg(pnode)
        else:
            ctx.node = col.Not(pnode)

    def exitPrefix(self, ctx):
        pass

    def enterParen(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Paren(pnode)

    def exitParen(self, ctx):
        pass

    def enterIint(self, ctx):
        pnode = ctx.parentCtx.node
        val = ctx.IINT().getText()
        if "d" in val: val = val.replace("d", "e")
        if "D" in val: val = val.replace("D", "e")
        if "E" in val: val = val.replace("E", "e")
        ctx.node = col.Iint(pnode, val)

    def exitIint(self, ctx):
        pass

    def enterString(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.String(pnode, ctx.STRING().getText())

    def exitString(self, ctx):
        pass

    def enterVar(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Var(pnode, ctx.ID().getText())
        ctx.node.declare()

    def exitVar(self, ctx):
        pass

    def enterInt(self, ctx):
        pnode = ctx.parentCtx.node
        val = ctx.INT().getText()
        if "d" in val: val = val.replace("d", "e")
        if "D" in val: val = val.replace("D", "e")
        if "E" in val: val = val.replace("E", "e")
        ctx.node = col.Int(pnode, val)

    def exitInt(self, ctx):
        pass

    def enterCtranspose(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Ctranspose(pnode)

    def exitCtranspose(self, ctx):
        pass

    def enterTranspose(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Transpose(pnode)

    def exitTranspose(self, ctx):
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

    def exitListall(self, ctx):
        pass

    def enterMatrix(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Matrix(pnode)

    def exitMatrix(self, ctx):
        pass

    def enterVector(self, ctx):
        pnode = ctx.parentCtx.node
        ctx.node = col.Vector(pnode)

    def exitVector(self, ctx):
        pass

    def enterBreak(self, ctx):
        ctx.node = col.Break(ctx.parentCtx.node)

    def exitBreak(self, ctx):
        pass

    def enterReturn(self, ctx):
        ctx.node = col.Return(ctx.parentCtx.node)

    def exitReturn(self, ctx):
        pass
