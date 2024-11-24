import ply.lex as lex  # Imports the lex module from the PLY library for lexical analysis.
import ply.yacc as yacc  # Imports the yacc module from the PLY library for syntax parsing.
import cmath  # Imports the cmath library for complex number calculations.
import sys  # Imports the sys module to handle command-line arguments.

flag_Interactivo = False  # A flag to indicate whether the program runs in interactive mode.

# Tokens
tokens = (
    'ID', 'NUM', 'COMPLEX',  # Identifiers, real numbers, and complex numbers.
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',  # Arithmetic operators.
    'LPAREN', 'RPAREN',  # Parentheses.
    'ASSIGN',  # Assignment operator.
    'SQRT', 'PRINT'  # Keywords for square root and printing.
)

# Token definitions using regular expressions
t_PLUS = r'\+'  # Matches the '+' operator.
t_MINUS = r'-'  # Matches the '-' operator.
t_TIMES = r'\*'  # Matches the '*' operator.
t_DIVIDE = r'/'  # Matches the '/' operator.
t_LPAREN = r'\('  # Matches the '(' symbol.
t_RPAREN = r'\)'  # Matches the ')' symbol.
t_ASSIGN = r'='  # Matches the '=' operator.
t_ignore = ' \t'  # Ignores spaces and tabs.

# Recognizes complex numbers
def t_COMPLEX(t):
    r'-?\d+(\.\d+)?[+-]\d+(\.\d+)?j'  # Matches a complex number pattern.
    t.value = complex(t.value)  # Converts the token to a complex number.
    return t

# Recognizes real numbers
def t_NUM(t):
    r'\d+(\.\d+)?'  # Matches a real number.
    t.value = float(t.value)  # Converts the token to a floating-point number.
    return t

# Recognizes the 'sqrt' keyword
def t_SQRT(t):
    r'sqrt'  # Matches the 'sqrt' keyword.
    return t

# Recognizes the 'print' keyword
def t_PRINT(t):
    r'print'  # Matches the 'print' keyword.
    return t

# Recognizes identifiers
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'  # Matches variable names or identifiers.
    return t

# Handles errors in tokenization
def t_error(t):
    print(f"Unknown token ({t.value})")  # Prints an error message for unrecognized tokens.
    t.lexer.skip(1)  # Skips the erroneous character.

# Initialize the lexer
lexer = lex.lex()

# Operator precedence rules
precedence = (
    ('left', 'PLUS', 'MINUS'),  # '+' and '-' are left-associative.
    ('left', 'TIMES', 'DIVIDE'),  # '*' and '/' are left-associative.
    ('right', 'UMINUS'),  # Unary minus has right-associative precedence.
)

# Dictionary to store variables
variables = {}

# Grammar rules
def p_statement_asignacion(p):
    'statement : ID ASSIGN expresion'  # Handles variable assignment.
    variables[p[1]] = evaluar_postfijo(p[3])  # Evaluates and stores the result in the variable.
    if flag_Interactivo is True:  # If in interactive mode, print the variable value.
        print(f"{p[1]} = {variables[p[1]]}\n")

def p_statement_impresion(p):
    'statement : PRINT LPAREN expresion RPAREN'  # Handles print statements.
    print(f"Resultado: {evaluar_postfijo(p[3])}")  # Prints the evaluated expression.

def p_expresion_binop(p):
    '''expresion : expresion PLUS expresion
                     | expresion MINUS expresion
                     | expresion TIMES expresion
                     | expresion DIVIDE expresion'''
    p[0] = f"{p[1]} {p[3]} {p[2]}"  # Converts the expression to postfix notation.

def p_expresion_unario(p):
    'expresion : MINUS expresion %prec UMINUS'  # Handles unary negation.
    p[0] = f"{p[2]} -u"

def p_expresion_grupo(p):
    'expresion : LPAREN expresion RPAREN'  # Handles grouped expressions in parentheses.
    p[0] = p[2]

def p_expresion_numero(p):
    'expresion : NUM'  # Matches a number.
    p[0] = str(p[1])

def p_expresion_complejo(p):
    'expresion : COMPLEX'  # Matches a complex number.
    p[0] = str(p[1])

def p_expresion_id(p):
    'expresion : ID'  # Matches a variable.
    if p[1] in variables:  # Checks if the variable exists.
        p[0] = str(variables[p[1]])
    else:  # Error if the variable is undefined.
        print(f"Error: Variable '{p[1]}' not defined.")
        p[0] = '0'

def p_expresion_sqrt(p):
    'expresion : SQRT LPAREN expresion RPAREN'  # Handles square root operations.
    p[0] = f"{p[3]} sqrt"

# Handles syntax errors
def p_error(p):
    if p:
        print(f"Syntax error at token {p.type}, value {p.value}")
    else:
        print("Syntax error at end of input")

# Initialize the parser
parser = yacc.yacc(debug=False, tabmodule=None)

# Function to evaluate postfix notation
def evaluar_postfijo(postfijo):
    stack = []
    for token in postfijo.split():
        if token.replace('.', '', 1).isdigit() or 'j' in token:  # Handles numbers (real and complex).
            stack.append(complex(token) if 'j' in token else float(token))
        elif token == '-u':  # Handles unary negation.
            stack.append(-stack.pop())
        elif token in ('+', '-', '*', '/'):  # Handles binary operators.
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
        elif token == 'sqrt':  # Handles square root operation.
            stack.append(cmath.sqrt(stack.pop()))
        else:  # Error for unknown tokens.
            print(f"Error: Unknown token {token}")
    return stack[0]  # Returns the final result.

# Main function
def main():
    if len(sys.argv) > 1:  # If there are command-line arguments.
        print("Static interpreter mode.")
        with open(sys.argv[1], 'r') as file:  # Reads input from a file.
            contenido = file.read()
        for linea in contenido.strip().split('\n'):  # Parses each line from the file.
            parser.parse(linea)
    else:
        global flag_Interactivo
        flag_Interactivo = True  # Enables interactive mode.
        print("Interactive interpreter mode. Type 'exit' to exit.")
        while True:
            try:
                entrada = input('> ')  # Reads input from the user.
                if entrada.lower() == 'exit':  # Exits if the user types 'exit'.
                    break
                if entrada.strip():  # Ignores empty inputs.
                    resultado = parser.parse(entrada)
                    if resultado is not None:
                        print(f"Result: {resultado}")
            except EOFError:
                break
            except Exception as e:  # Catches and prints errors.
                print(f"Error: {e}")

# Entry point
if __name__ == "__main__":
    main()  # Runs the main function.