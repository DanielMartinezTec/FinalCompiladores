
import ply.yacc as yacc
import lexer
import tac
from tac import threeAddressCode
from lexer import tokens

import sys
sys.path.insert(0,"../..")

import argparse

# Precedence rules for the arithmetic operators

precedence = (
    ('left', 'AND', 'OR'),
    ('nonassoc', 'EQ', 'NE', 'GE', 'LE', 'GT', 'LT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'POWER'),
    ('right', 'UMINUS'),
)

abstractTree = {}
names=[]

def p_initializer(p):
    '''initializer : statement'''
    global abstractTree
    abstractTree = p[1]


def p_statement(p):
    '''statement : conditional statement
                 | while_loop statement
                 | for_loop statement
                 | declaration_specifier_1 SEMI statement
                 | print SEMI statement
                 | empty'''
    if len(p) > 2:  # not empty
        if p[2] == ';':
            p[2] = p[3]
        p[0] = (p[1], ) + p[2]
    else:
        p[0] = ()


def p_empty(p):
    'empty :'
    pass


def p_selection_statement(p):
    '''conditional : if_stmt elif_stmt else_stmt'''
    p[0] = ('conditional', p[1], p[2], p[3])


def p_if(p):
    '''if_stmt : IF LPAREN expression RPAREN LBRACE statement RBRACE '''
    p[0] = ('if', p[3], p[6])


def p_elif(p):
    '''elif_stmt : ELIF LPAREN expression RPAREN LBRACE statement RBRACE elif_stmt
                 | empty'''
    
    if len(p) > 2:
        p[0] = (('elif', p[3], p[6]), ) + p[8]
    else:
        p[0] = ()

def p_else(p):
    '''else_stmt : ELSE LBRACE statement RBRACE
                 | empty'''
    
    if len(p) > 2: 
        p[0] = ('else', p[3])


def p_while(p):
    '''while_loop : WHILE LPAREN expression RPAREN LBRACE statement RBRACE'''
    p[0] = ('while', p[3], p[6])


def p_for(p):
    '''for_loop : FOR LPAREN declaration_specifier_3 SEMI expression SEMI declaration_specifier_4 RPAREN LBRACE statement RBRACE'''
    p[0] = ('for', p[3], p[5], p[7], p[10])


def p_type_specifier(p):
    '''type : INT
            | FLOAT
            | STRING
            | BOOLEAN'''
    p[0] = p[1]


def p_declaration_specifier_1(p):
    '''declaration_specifier_1  : declaration_specifier_2
                                | declaration_specifier_3
                                | declaration_specifier_4'''
    p[0] = p[1]


def p_declaration_specifier_2(p):
    '''declaration_specifier_2 : type ID'''
    p[0] = ('declare', p[1], p[2])
    names.append({"type": p[1],"value": p[2] if p[2] is None else 0})


def p_declaration_specifier_3(p):
    '''declaration_specifier_3 : type ID ASSIGN expression'''
    p[0] = ('declare_assign', p[1], p[2], p[4])


def p_declaration_specifier_4(p):
    '''declaration_specifier_4 : ID ASSIGN expression'''
    p[0] = ('assign', p[1], p[3])


def p_print(p):
    'print : PRINT expression'
    p[0] = ('print', p[2])
    print


def p_unary_operator(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POWER expression
                  | expression OR expression
                  | expression AND expression
                  | expression EQ expression
                  | expression NE expression
                  | expression GE expression
                  | expression LE expression
                  | expression GT expression
                  | expression LT expression'''
    p[0] = ('operation', p[1], p[2], p[3])

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]


def p_direct_declarator(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    '''expression : ICONST
                  | FCONST
                  | SCONST
                  | BOOLCONST'''
    p[0] = p[1]


def p_BOOLEAN(p):
    '''BOOLCONST : TRUE
               | FALSE'''
    if p[1] == "true":
        p[0] = True
    elif p[1] == "false":
        p[0] = False


def p_expression_name(p):
    "expression : ID"
    p[0] = p[1]


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


yacc.yacc()

# Main

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('filename', type=argparse.FileType('r'), help="File to Compile")
    args = parse.parse_args()

    if args.filename is not None:

        # print(args.filename.name)
        f = open(args.filename.name)
        r = f.read()
        f.close()
        yacc.parse(r)
        w = open('AST.txt','w')
        for node in abstractTree:
            w.write(str(node)+'\n')
        
        try:
            for node in abstractTree:
                tac.threeAddressCode(node)
        except:
            print ("Error trying to compile Three Address Code")

        w.close()

    else:
        print(args.filename)


# Execution


if __name__ == '__main__':
    main()