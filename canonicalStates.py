import parsetab

def extract_transitions_and_actions():
    transitions = []

    # Obtener las tablas de acciones (action) y transiciones (goto)
    action_table = parsetab._lr_action
    goto_table = parsetab._lr_goto

    # Extraer las acciones (SHIFT, REDUCE, ACCEPT)
    for state, actions in action_table.items():
        for symbol, action in actions.items():
            if isinstance(action, int):  # SHIFT o REDUCE
                if action > 0:  # SHIFT
                    transitions.append({
                        "from": state,
                        "symbol": symbol,
                        "to": action
                    })
                elif action < 0:  # REDUCE
                    transitions.append({
                        "from": state,
                        "symbol": symbol,
                        "to": f"Reduce using Rule {-action}"
                    })
                elif action == 0:  # ACCEPT
                    transitions.append({
                        "from": state,
                        "symbol": symbol,
                        "to": "Accept"
                    })

    # Extraer las transiciones GOTO
    for state, gotos in goto_table.items():
        for symbol, target in gotos.items():
            transitions.append({
                "from": state,
                "symbol": symbol,
                "to": target
            })

    return transitions

def print_transitions_and_actions():
    # Extraer transiciones y acciones
    transitions = extract_transitions_and_actions()

    # Imprimir en el formato solicitado
    print("=== Transiciones y Acciones ===")
    for transition in transitions:
        print(transition)

def main():
    print("=== Imprimiendo la Tabla de Análisis ===")
    print_transitions_and_actions()  # Transiciones y acciones en el formato solicitado

if __name__ == "__main__":
    main()
