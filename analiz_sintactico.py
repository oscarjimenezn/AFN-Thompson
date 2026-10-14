from analiz_lexico import AnalizLexico

class AnalizSintactico:
    def __init__(self, analizador_lexico):
        self.lexico = analizador_lexico
        self.token_actual = -1

    def iniciar_sintactico(self):
        # Leemos el primer token
        self.token_actual = self.lexico.yylex()
        
        # Llamamos al símbolo inicial de la gramática: E()
        if self.E() and self.token_actual == AnalizLexico.FIN:
            print("¡Análisis sintáctico exitoso! La cadena es válida.")
            return True
        else:
            print("Error sintáctico: La cadena no es válida.")
            return False

    # E -> T E'
    def E(self):
        if self.T():
            if self.Ep():
                return True
        return False

    # E' -> + T E' | - T E' | ε
    def Ep(self):
        # Token 10 = Suma (+), Token 20 = Resta (-) según tu prueba anterior
        if self.token_actual == 10 or self.token_actual == 20:
            self.token_actual = self.lexico.yylex() # Consumir operador
            if self.T():
                if self.Ep():
                    return True
                return False
            return False
        # Producción vacía (ε)
        return True

    # T -> F T'
    def T(self):
        if self.F():
            if self.Tp():
                return True
        return False

    # T' -> * F T' | / F T' | ε
    def Tp(self):
        # Token 30 = Multiplicación (*), Token 40 = División (/) por ejemplo
        if self.token_actual == 30 or self.token_actual == 40:
            self.token_actual = self.lexico.yylex() # Consumir operador
            if self.F():
                if self.Tp():
                    return True
                return False
            return False
        # Producción vacía (ε)
        return True

    # F -> ( E ) | num
    def F(self):
        # Token 70 = Número / ID según tus pruebas anteriores
        if self.token_actual == 70:
            self.token_actual = self.lexico.yylex() # Consumir número
            return True
        
        # Si manejas paréntesis: Token 50 = '(', Token 60 = ')'
        elif self.token_actual == 50:
            self.token_actual = self.lexico.yylex() # Consumir '('
            if self.E():
                if self.token_actual == 60:
                    self.token_actual = self.lexico.yylex() # Consumir ')'
                    return True
                else:
                    print("Error: Se esperaba ')'")
                    return False
            return False
        
        print(f"Error sintáctico en lexema: '{self.lexico.estado.lexema}'")
        return False
