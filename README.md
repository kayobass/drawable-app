# Drawable App

---

## 📋 Descrição do Sistema

O **Drawable App** é uma aplicação gráfica desenvolvida em Python utilizando a biblioteca Tkinter, destinada à criação e manipulação de desenhos vetoriais simples. O sistema permite ao usuário desenhar diversas formas geométricas (linhas, rabiscos, retângulos, ovais, polígonos), personalizar cores de borda e preenchimento, ajustar espessura de linhas, utilizar um sistema de desfazer/refazer, copiar/colar figuras e salvar/carregar desenhos em disco. O projeto segue os padrões arquiteturais **MVC (Model-View-Controller)** e **State**.

---

## 👨‍💻 Equipe

| Integrante      | GitHub          |
| --------------- | --------------- |
| Kayo Araujo     | @kayobass       |
| Matheuz Rozendo | @matheuzrozendo |

---

## 🔩 Classes Documentadas

**21 classes**

| #   | Classe                | Arquivo                          |
| --- | --------------------- | -------------------------------- |
| 1   | `Figura` (ABC)        | `src/models/figura.py`           |
| 2   | `Linha`               | `src/models/tracados.py`         |
| 3   | `Rabisco`             | `src/models/tracados.py`         |
| 4   | `Circulo`             | `src/models/ovais.py`            |
| 5   | `Oval`                | `src/models/ovais.py`            |
| 6   | `Retangulo`           | `src/models/retangulos.py`       |
| 7   | `Quadrado`            | `src/models/retangulos.py`       |
| 8   | `TrianguloEquilatero` | `src/models/poligonos.py`        |
| 9   | `TrianguloRetangulo`  | `src/models/poligonos.py`        |
| 10  | `Pentagono`           | `src/models/poligonos.py`        |
| 11  | `Hexagono`            | `src/models/poligonos.py`        |
| 12  | `Poligono`            | `src/models/poligonos.py`        |
| 13  | `Historico`           | `src/models/historico.py`        |
| 14  | `DrawableView`        | `src/views/view.py`              |
| 15  | `DrawableController`  | `src/controllers/controller.py`  |
| 16  | `EstadoFerramenta` (ABC) | `src/models/estados.py`       |
| 17  | `EstadoLinha`         | `src/models/estados.py`          |
| 18  | `EstadoRabisco`       | `src/models/estados.py`          |
| 19  | `EstadoFigura`        | `src/models/estados.py`          |
| 20  | `EstadoPoligono`      | `src/models/estados.py`          |
| 21  | `EstadoSelecao`       | `src/models/estados.py`          |

---

## 🔎 Métodos Documentados

**98 métodos**

| Classe                | Métodos                                                                                                           | Qtd |
| --------------------- | ----------------------------------------------------------------------------------------------------------------- | --- |
| `Figura`              | `__init__`, `__str__`, `__eq__`, `desenhar`                                                                       | 4   |
| `Linha`               | `desenhar`                                                                                                        | 1   |
| `Rabisco`             | `desenhar`                                                                                                        | 1   |
| `Circulo`             | `transformar_em_circulo`, `desenhar`                                                                              | 2   |
| `Oval`                | `desenhar`                                                                                                        | 1   |
| `Retangulo`           | `desenhar`                                                                                                        | 1   |
| `Quadrado`            | `retangulo_em_quadrado`, `desenhar`                                                                               | 2   |
| `TrianguloEquilatero` | `desenhar`                                                                                                        | 1   |
| `TrianguloRetangulo`  | `desenhar`                                                                                                        | 1   |
| `Pentagono`           | `desenhar`                                                                                                        | 1   |
| `Hexagono`            | `desenhar`                                                                                                        | 1   |
| `Poligono`            | `adicionar_ponto`, `desenhar_pontos_do_poligono`, `desenhar`                                                      | 3   |
| `Historico`           | `__init__`, `adicionar`, `inserir`, `desfazer`, `refazer`, `registrar_movimentacao`, `desfazer_movimentacao`, `refazer_movimentacao`, `limpar`, `figuras`, `figuras_desfeitas` | 11  |
| `DrawableView`        | `__init__`, `criar_widgets_selecao`, `criar_widgets_personalizacao`, `criar_area_desenho`, `mainloop`             | 5   |
| `DrawableController`  | `__init__`, `figuras_disponiveis`, `ferramenta`, `espessura`, `configurar_comandos`, `configurar_eventos`,        |     |
|                       | `atribuir_foco_canvas`, `escolher_cor_da_borda`, `escolher_cor_do_preenchimento`, `remover_preenchimento`,        |     |
|                       | `detecta_mudanca`, `alterar_espessura`, `verifica_historico`, `iniciar_figura_nova`,                              |     |
|                       | `atualizar_figura_nova`, `incluir_figura_nova`, `finalizar_poligono`, `desenhar_figuras`,                         |     |
|                       | `selecionar_figura`, `atualizar_indicadores`, `mover_figura_selecionada`, `desenhar_figura_nova`,                 |     |
|                       | `incompleta`, `desfazer`, `refazer`, `excluir_figura_selecionada`, `duplicar_figura`,                             |     |
|                       | `copiar_figura`, `colar_figura`, `mover_posicao_frente`, `mover_posicao_tras`,                                    |     |
|                       | `mover_posicao_topo`, `mover_posicao_fundo`, `cancelar_acao`, `esta_alterado`,                                   |     |
|                       | `salvar_desenho`, `carregar_desenho`, `fechar_app`                                                                | 38  |
| `EstadoFerramenta`    | `configurar_estado`, `iniciar_figura`, `atualizar_figura`, `incluir_figura`, `desfazer`, `refazer`                | 6   |
| `EstadoLinha`         | `configurar_estado`, `iniciar_figura`, `atualizar_figura`, `incluir_figura`, `desfazer`, `refazer`                | 6   |
| `EstadoRabisco`       | `configurar_estado`, `iniciar_figura`, `atualizar_figura`, `incluir_figura`, `desfazer`, `refazer`                | 6   |
| `EstadoFigura`        | `configurar_estado`, `iniciar_figura`, `atualizar_figura`, `incluir_figura`, `desfazer`, `refazer`                | 6   |
| `EstadoPoligono`      | `configurar_estado`, `iniciar_figura`, `atualizar_figura`, `incluir_figura`, `finalizar`, `desfazer`, `refazer`  | 7   |
| `EstadoSelecao`       | `configurar_estado`, `iniciar_figura`, `atualizar_figura`, `incluir_figura`, `desfazer`, `refazer`                | 6   |

---

## ⌨️ Atalhos

| Atalho                 | Ação                                |
| ---------------------- | ----------------------------------- |
| Ctrl + Z               | Desfazer                            |
| Ctrl + Y               | Refazer                             |
| Ctrl + D               | Duplicar figura selecionada         |
| Ctrl + C               | Copiar figura selecionada           |
| Ctrl + V               | Colar figura copiada                |
| Delete                 | Apagar figura selecionada           |
| Escape                 | Cancelar ação em andamento          |
| Seta →                 | Mover figura para frente            |
| Seta ←                 | Mover figura para trás              |
| Seta ↑                 | Mover figura para o topo            |
| Seta ↓                 | Mover figura para o fundo           |
| Botão direito do mouse | Finalizar polígono interativo       |

---

## 🏗️ Padrões de Projeto

### MVC (Model-View-Controller)

- **Model**: `Historico`, `Figura` e suas subclasses
- **View**: `DrawableView`
- **Controller**: `DrawableController`

### State

O padrão State é utilizado para encapsular o comportamento que varia de acordo com a ferramenta selecionada, eliminando condicionais no controlador:

| Estado           | Ferramentas                          |
| ---------------- | ------------------------------------ |
| `EstadoLinha`    | Linha                                |
| `EstadoRabisco`  | Rabisco                              |
| `EstadoFigura`   | Oval, Círculo, Retângulo, Quadrado, Triângulos, Pentágono, Hexágono |
| `EstadoPoligono` | Polígono interativo                  |
| `EstadoSelecao`  | Selecionar                           |

---

### 📚 Pré-requisitos

- Python 3.0 ou superior instalado
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

### 📖 Visualizar a Documentação

A documentação HTML gerada pelo Pydoc está disponível na pasta `docs/`.

1. Acesse a pasta de documentação:

```bash
cd docs
```

2. Abra o arquivo `main.html` no navegador:

```bash
# Windows
start main.html

# Linux
xdg-open main.html

# macOS
open main.html
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

- [x] Definir as classes do modelo (Figuras, Historico)
- [x] Definir uma classe para a visão (DrawableView)
- [x] Definir uma classe para o controlador (DrawableController)

---

## ✅ Etapa 4 — Implementada

Persistência e documentação do sistema:

- [x] Botões Salvar e Carregar na interface
- [x] Serialização de desenhos com Pickle (`.pkl`)
- [x] Verificação de alterações não salvas ao fechar
- [x] Atualização do título da janela com nome do arquivo
- [x] Docstrings padronizadas com tags `@author`, `@version`, `@param`, `@return`, `@throws`, `@see`, `@since`
- [x] Documentação HTML gerada via Pydoc

---

## ✅ Etapa 5 — Implementada

Refatoração para o padrão **State**:

- [x] Classes de estado abstrata (`EstadoFerramenta`) e concretas
- [x] Seleção de figura (clique no canvas)
- [x] Mover figura (arrastar com mouse)
- [x] Apagar figura selecionada (tecla Delete)
- [x] Mudar cores e espessura da figura selecionada
- [x] Passar uma posição para frente (seta →)
- [x] Passar uma posição para trás (seta ←)
- [x] Passar para o topo (seta ↑)
- [x] Passar para o fundo (seta ↓)
- [x] Copiar para buffer (Ctrl+C)
- [x] Colar do buffer (Ctrl+V)
- [x] Duplicar figura selecionada (Ctrl+D)
- [x] Cancelar ação com Escape
- [x] Desfazer/Refazer com suporte a movimentação de posições

---

_Documentação elaborada para fins acadêmicos — Disciplina de Programação A_
