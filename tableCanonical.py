import tkinter as tk
from tkinter import ttk
import parsetab

def print_action_goto_table():
    # Obtener las tablas de acciones y goto generadas por PLY
    action_table = parsetab._lr_action
    goto_table = parsetab._lr_goto
    
    # Identificar todos los terminales y no terminales en la tabla para hacer el encabezado
    terminals = set()
    nonterminals = set()

    for actions in action_table.values():
        terminals.update(actions.keys())
    for gotos in goto_table.values():
        nonterminals.update(gotos.keys())

    terminals = sorted(terminals)
    nonterminals = sorted(nonterminals)

    # Crear la ventana de Tkinter
    root = tk.Tk()
    root.title("Tabla de Análisis Sintáctico")

    # Crear un marco para la tabla
    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)

    # Crear el Treeview para mostrar la tabla
    columns = ["State"] + terminals + nonterminals
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    
    # Definir las columnas y sus encabezados
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    # Obtener el número de estados en la tabla
    num_states = max(max(action_table.keys()), max(goto_table.keys()))

    # Agregar filas a la tabla
    for state in range(num_states + 1):
        row = [str(state)]
        
        # Agregar acciones de la tabla de acciones (shift, reduce, accept)
        for terminal in terminals:
            action = action_table.get(state, {}).get(terminal, "")
            
            # Verifica el tipo de 'action' para asegurarse de que sea un entero
            if isinstance(action, int):
                if action > 0:
                    row.append(f"S{action}")   # Shift
                elif action < 0:
                    row.append(f"r{-action}")  # Reduce
                elif action == 0:
                    row.append("acc")          # Accept
            else:
                row.append(str(action) if action else "")

        # Agregar transiciones de la tabla goto
        for nonterminal in nonterminals:
            next_state = goto_table.get(state, {}).get(nonterminal, "")
            row.append(str(next_state) if next_state else "")

        # Agregar la fila al Treeview
        tree.insert("", "end", values=row)

    # Agregar el Treeview a la interfaz
    tree.pack(fill="both", expand=True)

    # Iniciar el bucle principal de Tkinter
    root.mainloop()

def print_productions():
    print("\n=== Producciones ===")
    productions = parsetab._lr_productions  # Lista de producciones
    for i, prod in enumerate(productions):
        print(f"{i}: {prod}")

def main():
    print("=== Imprimiendo la Tabla de Análisis ===")
    print_productions()     # Lista de producciones
    print_action_goto_table()  # Tabla combinada de Action y Goto

if __name__ == "__main__":
    main()