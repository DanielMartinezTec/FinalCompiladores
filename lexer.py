
import sys
sys.path.insert(0, "../..")

import ply.lex as lex


reserved = {
    'boolean': 'BOOLEAN', 'elif':'ELIF', 'else':'ELSE', 'false':'FALSE', 
    'float':'FLOAT', 'for':'FOR', 'if':'IF', 'int':'INT', 'print':'PRINT', 
    'string':'STRING', 'true':'TRUE', 'while':'WHILE',
}

tokens = tuple(reserved.values()) + (
    # Literals (identifier, integer constant, float constant, string constant)
    'ID', 'ICONST', 'FCONST', 'SCONST',

    # Operators (+, -, *, /, ^, <, <=, >, >=, ==, !=)
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'OR', 'AND', 
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

    # Assignment (=)
    'ASSIGN',

    # Delimeters ( ) { } ;
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'SEMI',
)

# Completely ignored characters
t_ignore = ' \t\x0c'

# Newlines

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Operators
t_PLUS             = r'\+'
t_MINUS            = r'-'
t_TIMES            = r'\*'
t_DIVIDE           = r'/'
t_POWER            = r'\^'
t_OR               = r'\|'
t_AND              = r'&'
t_LT               = r'<'
t_LE               = r'<='
t_GT               = r'>'
t_GE               = r'>='
t_EQ               = r'=='
t_NE               = r'!='

# Assignment operators

t_ASSIGN            = r'='

# Delimeters
t_LPAREN            = r'\('
t_RPAREN            = r'\)'
t_LBRACE            = r'\{'
t_RBRACE            = r'\}'
t_SEMI              = r';'

# Identifiers

# Type Tokens
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Floating literal

def t_FCONST(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Integer literal

def t_ICONST(t):
    r'\d+'
    t.value = int(t.value)
    return t

# String literal

def t_SCONST(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()