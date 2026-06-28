from figura import Figura

class Poligono(Figura):  
    def adicionar_ponto(self, x, y):
        self.values.append((x, y))
    
    def desenhar_pontos_do_poligono(self, canvas):
        # Desenha as bolinhas nos vértices temporários
        for x, y in self.values:
            canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=self.cor_borda)
            
        if len(self.values) >= 2:
            for i in range(len(self.values) - 1):
                x_inicial, y_inicial = self.values[i]
                x_final, y_final = self.values[i + 1]
                canvas.create_line(x_inicial, y_inicial, x_final, y_final, fill=self.cor_borda, width=self.espessura, dash=(4, 2))
            
            # Liga o ponto atual de volta ao primeiro ponto com uma linha pontilhada guia
            x_prim, y_prim = self.values[0]
            x_ult, y_ult = self.values[-1]
            canvas.create_line(x_ult, y_ult, x_prim, y_prim, fill=self.cor_borda, width=self.espessura, dash=(2, 4))
 
    def desenhar(self, canvas):
        pontos = self.values

        if len(pontos) < 3:
            return None

        return canvas.create_polygon(
            pontos,
            outline=self.cor_borda, 
            fill=self.cor_preenchimento, 
            width=self.espessura
        )