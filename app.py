def unsafe_apply_function():
    # Vulnerabilidad: uso de 'apply' (deprecado en Python 3, peligroso si se imita el comportamiento)
    def multiply(x, y):
        return x * y

    args = (5, 6)
    result = apply(multiply, args)  # <-- Vulnerabilidad detectada por CodeQL
    print("Resultado:", result)

def break_in_finally():
    try:
        print("Intentando hacer algo riesgoso...")
        1 / 0  # Forzamos un error
    finally:
        print("En finally...")
        break  # <-- Vulnerabilidad: break dentro de finally (SyntaxError pero aún analizable por CodeQL)

if __name__ == "__main__":
    unsafe_apply_function()
    break_in_finally()
