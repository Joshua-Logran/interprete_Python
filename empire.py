import ply.lex as lex
import ply.yacc as yacc
import cmath  # Para manejar números complejos
import sys

flag_Interactivo = False

# Tokens
tokens = (
    'ID', 'NUM', 'COMPLEX',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN',
    'ASSIGN',
    'SQRT', 'PRINT'
)

# Definición de símbolos
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'='
t_ignore = ' \t'

# Reconocer números complejos
def t_COMPLEX(t):
    r'-?\d+(\.\d+)?[+-]\d+(\.\d+)?j'
    t.value = complex(t.value)  # Convierte el token directamente a número complejo
    return t

# Reconocer números reales
def t_NUM(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)  # Convierte el token a número flotante
    return t

# Reconocer palabras clave (SQRT y PRINT)
def t_SQRT(t):
    r'sqrt'
    return t

def t_PRINT(t):
    r'print'
    return t

# Reconocer identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_error(t):
    print(f"Token desconocido ({t.value})")
    t.lexer.skip(1)

lexer = lex.lex()

# Precedencia de operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# Diccionario de variables
variables = {}

# Gramática
def p_statement_asignacion(p):
    'statement : ID ASSIGN expresion'
    variables[p[1]] = evaluar_postfijo(p[3])
    if flag_Interactivo is True:
        print(f"{p[1]} = {variables[p[1]]}\n")

def p_statement_impresion(p):
    'statement : PRINT LPAREN expresion RPAREN'
    print(f"Resultado: {evaluar_postfijo(p[3])}")

def p_expresion_binop(p):
    '''expresion : expresion PLUS expresion
                     | expresion MINUS expresion
                     | expresion TIMES expresion
                     | expresion DIVIDE expresion'''
    p[0] = f"{p[1]} {p[3]} {p[2]}"

def p_expresion_unario(p):
    'expresion : MINUS expresion %prec UMINUS'
    p[0] = f"{p[2]} -u"

def p_expresion_grupo(p):
    'expresion : LPAREN expresion RPAREN'
    p[0] = p[2]

def p_expresion_numero(p):
    'expresion : NUM'
    p[0] = str(p[1])

def p_expresion_complejo(p):
    'expresion : COMPLEX'
    p[0] = str(p[1])

def p_expresion_id(p):
    'expresion : ID'
    if p[1] in variables:
        p[0] = str(variables[p[1]])
    else:
        print(f"Error: Variable '{p[1]}' not defined.")
        p[0] = '0'

def p_expresion_sqrt(p):
    'expresion : SQRT LPAREN expresion RPAREN'
    p[0] = f"{p[3]} sqrt"

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}, value {p.value}")
    else:
        print("Syntax error at end of input")

parser = yacc.yacc(debug=False, tabmodule = None)

# Función para evaluar notación postfija
def evaluar_postfijo(postfijo):
    stack = []
    for token in postfijo.split():
        if token.replace('.', '', 1).isdigit() or 'j' in token:  # Soporte para números complejos
            stack.append(complex(token) if 'j' in token else float(token))
        elif token == '-u':  # Negación unaria
            stack.append(-stack.pop())
        elif token in ('+', '-', '*', '/'):  # Operadores binarios
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a / b)
        elif token == 'sqrt':  # Raíz cuadrada (soporte para números complejos)
            stack.append(cmath.sqrt(stack.pop()))
        else:
            print(f"Error: Unknown token {token}")
    return stack[0]

def main():
    if len(sys.argv) > 1:
        # Leer desde archivo
        print("Static interpreter mode.")
        with open(sys.argv[1], 'r') as file:
            contenido = file.read()
        for linea in contenido.strip().split('\n'):
            parser.parse(linea)
    else:
        global flag_Interactivo
        flag_Interactivo = True
        # Modo interactivo
        print("Interactive interpreter mode. Type 'exit' to exit.")
        while True:
            try:
                entrada = input('> ')
                if entrada.lower() == 'exit':
                    break
                if entrada.strip():  # Ignorar entradas vacías
                    resultado = parser.parse(entrada)
                    if resultado is not None:
                        print(f"Result: {resultado}")
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()