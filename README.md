# Drawable App

---

## 📋 Descrição do Sistema

O **Drawable App** é uma aplicação gráfica desenvolvida em Python utilizando a biblioteca Tkinter, destinada à criação e manipulação de desenhos vetoriais simples. O sistema permite ao usuário desenhar diversas formas geométricas (linhas, rabiscos, retângulos, ovais e etc), personalizar cores de borda e preenchimento, ajustar espessura de linhas e utilizar um sistema de desfazer/refazer. O projeto segue o padrão arquitetural **MVC (Model-View-Controller)**.

---

## 👨‍💻 Equipe

| Integrante      | GitHub          |
| --------------- | --------------- |
| Kayo Araujo     | @kayobass       |
| Matheuz Rozendo | @matheuzrozendo |

---

## 🔩 Classes Presentes

**15 classes**

| #   | Classe                | Arquivo                            |
| --- | --------------------- | ---------------------------------- |
| 1   | `Figura` (ABC)        | `src/models/figura.py`             |
| 2   | `Linha`               | `src/models/tracados.py`           |
| 3   | `Rabisco`             | `src/models/tracados.py`           |
| 4   | `Circulo`             | `src/models/ovais.py`              |
| 5   | `Oval`                | `src/models/ovais.py`              |
| 6   | `Retangulo`           | `src/models/retangulos.py`         |
| 7   | `Quadrado`            | `src/models/retangulos.py`         |
| 8   | `TrianguloEquilatero` | `src/models/poligonos.py`          |
| 9   | `TrianguloRetangulo`  | `src/models/poligonos.py`          |
| 10  | `Pentagono`           | `src/models/poligonos.py`          |
| 11  | `Hexagono`            | `src/models/poligonos.py`          |
| 12  | `Poligono`            | `src/models/poligonos.py`          |
| 13  | `Historico`           | `src/models/historico.py`          |
| 14  | `DrawableView`        | `src/views/view.py`                |
| 15  | `DrawableController`  | `src/controllers/controller.py`    |

---

## 🔎 Métodos por Classe

**50 métodos**

| Classe                | Métodos                                                                                                                          | Qtd |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------- | --- |
| `Figura`              | `__init__`, `desenhar`                                                                                                           | 2   |
| `Linha`               | `desenhar`                                                                                                                       | 1   |
| `Rabisco`             | `desenhar`                                                                                                                       | 1   |
| `Circulo`             | `transformar_em_circulo`, `desenhar`                                                                                             | 2   |
| `Oval`                | `desenhar`                                                                                                                       | 1   |
| `Retangulo`           | `desenhar`                                                                                                                       | 1   |
| `Quadrado`            | `retangulo_em_quadrado`, `desenhar`                                                                                              | 2   |
| `TrianguloEquilatero` | `desenhar`                                                                                                                       | 1   |
| `TrianguloRetangulo`  | `desenhar`                                                                                                                       | 1   |
| `Pentagono`           | `desenhar`                                                                                                                       | 1   |
| `Hexagono`            | `desenhar`                                                                                                                       | 1   |
| `Poligono`            | `adicionar_ponto`, `desenhar_pontos_do_poligono`, `desenhar`                                                                     | 3   |
| `Historico`           | `__init__`, `adicionar`, `desfazer`, `refazer`, `limpar`, `figuras`, `figuras_desfeitas`                                         | 7   |
| `DrawableView`        | `__init__`, `criar_widgets_selecao`, `criar_widgets_personalizacao`, `criar_area_desenho`, `mainloop`                            | 5   |
| `DrawableController`  | `__init__`, `figuras_disponiveis`, `ferramenta`, `espessura`, `configurar_comandos`, `configurar_eventos`, `atribuir_foco_canvas`, `escolher_cor_da_borda`, `escolher_cor_do_preenchimento`, `remover_preenchimento`, `opcao_mudou`, `iniciar_poligono`, `iniciar_figura`, `iniciar_figura_nova`, `atualizar_figura_nova`, `incluir_figura_nova`, `finalizar_poligono`, `desenhar_figuras`, `desenhar_figura_nova`, `incompleta`, `desfazer`, `refazer` | 21  |

---

## ⌨️ Atalhos

| Atalho                 | Ação                          |
| ---------------------- | ----------------------------- |
| Ctrl + Z               | Desfazer                      |
| Ctrl + Y               | Refazer                       |
| Botão direito do mouse | Finalizar polígono interativo |

---

### 📚 Pré-requisitos

- Python 3.x instalado
- Biblioteca Tkinter (incluída na instalação padrão do Python)

### 💻 Executar o Sistema

1. Clone o repositório:

```bash
git clone https://github.com/kayobass/drawable-app.git
```

2. Acesse a pasta do projeto:

```bash
cd drawable-app
```

3. Execute o programa:

```bash
python src/main.py
```

---

# 📈 Evolução do Projeto

## ✅ Etapa 1 — Implementada

- [x] Estudo de Git e GitHub
- [x] Estudo de Tkinter
- [x] Criação do repositório
- [x] Desenho de retângulos
- [x] Desenho de ovais
- [x] Desenho de círculos
- [x] Cor de borda
- [x] Cor de preenchimento

---

## ✅ Etapa 2 — Implementada

- [x] Refatoração para Programação Orientada a Objetos
- [x] Definir hierarquia de classes (Figura abstrata)
- [x] Adequar o programa para usar a hierarquia de Figuras
- [x] Adicionar desenho de polígonos (Triângulo, Triângulo Retângulo, Pentágono, Hexágono, Polígono interativo)
- [x] Separar código em módulos (cada figura em seu próprio arquivo)
- [x] Seleção de espessura da linha

---

## ✅ Etapa 3 — Implementada

Refatoração para o padrão **MVC (Model-View-Controller)**:

- [x] Definir as classes do modelo (Figuras, Desenho, ...)
- [x] Definir uma classe ou classes para a visão
- [x] Definir uma classe ou classes para o(s) controlador(es)

---

_Documentação elaborada para fins acadêmicos — Disciplina de Programação A_
