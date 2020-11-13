from flask import Flask, render_template, request
import ply.lex as lex

app = Flask(__name__)


#-----------------TOKENIZER FOR PYTHON------------------------------------
# Los tokens son los componentes léxicos de un lenguaje. Los tipos de token son: identificadores, 
# palabras clave, operadores y delimitadores. Para separar los tokens se utilizan espacios.
tokens = ['IDENTIFICADOR', 'NUMERO', 'MAS', 'MENOS', 'TIMES', 'DIVISION','LPAREN', 'RPAREN', 
    'MODULO', 'ASIGNACION', 'AND', 'OR', 'NOT', 'MENORQUE', 'MENORIGUAL', 'MAYORQUE',
   'MAYORIGUAL', 'IGUALA', 'DISTINTO', 'CORIZQ', 'CORDER', 'LLAIZQ', 'LLADER',
   'PUNTOCOMA', 'COMA', 'DOSPUNTOS', 'RESERVADA', 'OPERADORLOGICO'
]

# Palabras reservadas que no podremos utilizar para ningún tipo de identificador
reserved = {   'if' : 'IF', 'else' : 'ELSE', 'elif' : 'ELIF', 'for' : 'FOR',
    'while' : 'WHILE', 'in' : 'IN', 'print' : 'PRINT'
 }

tokens = tokens + list(reserved.values())

# Reglas de expresión regulares para los tokens simples.
# En cualquier caso, el nombre de la REGLA debe tener el prefijo t_ seguido del nombre
# de algun token de la lista de tokens.  
def t_MENORIGUAL(t):
    r'<='
    return t

def t_MAYORIGUAL(t):
    r'>='
    return t

def t_IGUALA(t):
    r'=='
    return t

def t_DISTINTO(t):
    r'!='
    return t

def t_RESERVADA(t):  
    r'return|import|def'
    return t

def t_OPERADORLOGICO(t): 
    r'and|or|not'
    return t

t_MAS    = r'\+'
t_MENOS   = r'-'
t_TIMES   = r'\*'
t_DIVISION  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'     
t_MODULO = r'\%'
t_ASIGNACION = r'='
t_AND = r'\&\&'
t_OR = r'\|{2}'
t_NOT = r'\!'
t_MENORQUE = r'<'
t_MAYORQUE = r'>' 
t_PUNTOCOMA = ';'
t_COMA = r','
t_DOSPUNTOS = r':'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_LLAIZQ = r'{'
t_LLADER = r'}'

# Reglas con algún código de acción
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFICADOR')  # Check for reserved words
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Definir una regla para que podamos rastrear los números de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Una cadena que contiene caracteres ignorados (espacios y tabulaciones)
t_ignore  = ' \t'
t_ignore_COMMENT = r'\#.*'
# Or
#def t_COMMENT(t):
#       r'\#.*'
#       pass  # No return value. Token discarded

# Regla de manejo de errores
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


#---------------TEST TOKENIZER---------------------------
# Para usar el lexer debe llenarlo con algún texto de entrada usando input(). 
# Después de eso, las llamadas repetidas a token() producen tokens. 
#my_file = open("examples/example-fibonacci-1.txt", "r")
my_file = open("examples/example-fibonacci-2.txt", "r")
#my_file = open("examples/example-is-prime.txt", "r")
data = my_file.read()
my_file.close()

# Dale al lexer alguna entrada
#lexer.input(data)
 
# Tokenize
#while True:
#    tok = lexer.token()
#    if not tok: 
#        break   # No more input       
#    line_start = data.rfind('\n', 0, tok.lexpos) + 1
#    num_column = (tok.lexpos - line_start) + 1
#    num_line = tok.lineno
#    print(tok.type, tok.value, num_line, num_column)
# Or
#for tok in lexer:
#    print(tok)


#----------------------ENDPOINTS-----------------------------
@app.route('/')
def main():
    return render_template('app.html')

@app.route('/', methods=['POST'])
def analize():
    if request.method == 'POST':
        #num1 = request.form['num1']                    
        lexer = lex.lex()
        lexer.input(data)
        return render_template('app.html', data=data, lexer=lexer)    


if __name__ == ' __main__':
    app.debug = True
    app.run()