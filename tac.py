# ----------------------------------------------------------------
#
# Three address code
#
# ----------------------------------------------------------------

w = open('ThreeDirectionCode', 'w')

tmp = -1
label = -1

def nextL():
    global label
    label += 1
    return "L" + str(label)

def nextT():
    global tmp
    tmp += 1
    return "T" + str(tmp)
    

def threeAddressCode(abstractSyntaxTree):
    if type(abstractSyntaxTree) is not tuple:
        return abstractSyntaxTree
    reservedToken = abstractSyntaxTree[0]
# declaration statement with assignment type

    if reservedToken == "declare_assign":
        varType = abstractSyntaxTree[1]
        varName = abstractSyntaxTree[2]
        w.write(str(varType) + " " + str(varName) + "\n")
        resValue = threeAddressCode(abstractSyntaxTree[3])
        w.write(str(varName) + "=" + str(resValue) + "\n")

# declaration statement with no parameters

    elif reservedToken == "declare":
        varType = abstractSyntaxTree[1]
        varName = abstractSyntaxTree[2]
        w.write(str(varType) + " "+  str(varName) + "\n")

# declaration statement assignation only

    elif reservedToken == "assign":
        varName = abstractSyntaxTree[1]
        resValue = threeAddressCode(abstractSyntaxTree[2])
        w.write(str(varName) + "=" + str(resValue) + "\n")
    
# operator statement for cases as +, -, *, /, ^,

    elif reservedToken == "operation":
        res1 = threeAddressCode(abstractSyntaxTree[1])
        op = abstractSyntaxTree[2]
        res2 = threeAddressCode(abstractSyntaxTree[3])
        currT = nextT()
        w.write(str(currT) + '=' + str(res1) + " " + str(op) + " " + str(res2) + "\n")
        return currT

# expression statement for print

    elif reservedToken == "print":
        resValue = threeAddressCode(abstractSyntaxTree[1])
        w.write("print" + " " + str(resValue) + "\n")

# conditional statement for conditionals

    elif reservedToken == "conditional":
        if_stmt = abstractSyntaxTree[1]
        elif_arr = abstractSyntaxTree[2]
        else_stmt = abstractSyntaxTree[3]

#conditional statement if

        cond = threeAddressCode(if_stmt[1])
        currL = nextL()
        endL = nextL()
        stmts = if_stmt[2]
        w.write("if not" + " " + str(cond) + " " + "go to" + " " + str(currL) + "\n")
        for stmt in stmts:
            threeAddressCode(stmt)
        w.write("go to" + " " + str(endL) + "\n")
        w.write("label" + " " + str(currL) + "\n")

#conditional statement ELIF

        for elif_stmt in elif_arr:
            cond = threeAddressCode(elif_stmt[1])
            stmts = elif_stmt[2]
            currL = nextL()
            w.write("if not" + " " + str(cond) + " " + "go to" + " " + str(currL) + "\n")
            for stmt in stmts:
                threeAddressCode(stmt)
            w.write("go to" + " " + str(endL) + "\n")
            w.write("label" + " " + str(currL) + "\n")

# conditional statement ELSE

        if else_stmt is not None:
            stmts = else_stmt[1]
            for stmt in stmts:
                threeAddressCode(stmt)
        w.write("label" + " " + str(endL) + "\n")

# conditional statement FOR

    elif reservedToken == "for":
        init = threeAddressCode(abstractSyntaxTree[1])
        loop = abstractSyntaxTree[3]
        stmts = abstractSyntaxTree[4]
        loopL = nextL()
        endL = nextL()
        w.write("label" + " " + str(loopL) + "\n")
        cond = threeAddressCode(abstractSyntaxTree[2])
        w.write("if not" + " " + str(cond) + " " + "go to" + " " + str(endL) + "\n")
        for stmt in stmts:
            threeAddressCode(stmt)
        w.write("go to" + " " + str(loopL) + "\n")
        w.write("label" + " " + str(endL) + "\n")
    
# conditional statement WHILE

    elif reservedToken == "while":
        stmts = abstractSyntaxTree[2]
        loopL = nextL()
        endL = nextL()
        w.write("label" + " " + str(loopL) + "\n")
        cond = threeAddressCode(abstractSyntaxTree[1])
        w.write("if not" + " " + str(cond) + " " + "go to" + " " + str(endL) + "\n")
        for stmt in stmts:
            threeAddressCode(stmt)
        w.write("go to" + " " + str(loopL) + "\n")
        w.write("label" + " " + str(endL) + "\n")