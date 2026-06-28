# Drawable App

Aplicação gráfica desenvolvida em Python utilizando a biblioteca Tkinter para criação e manipulação de desenhos vetoriais simples, inspirada em ferramentas como Google Drawings, Paint e LibreOffice Draw.

Este projeto foi desenvolvido como atividade da disciplina de Programação A da UFS.

---

## 📋 Objetivo do Projeto

O objetivo é desenvolver uma ferramenta de desenho com interface gráfica capaz de permitir ao usuário criar e manipular formas geométricas, aplicando conceitos de:

- Programação Orientada a Objetos
- Interfaces Gráficas com Tkinter
- Padrões de Projeto
- Arquitetura de Software
- Controle de Versão com Git e GitHub
- Desenvolvimento Colaborativo

O projeto será evoluído gradualmente ao longo das etapas da disciplina.

---

# 🚀 Tecnologias Utilizadas

- Python
- Tkinter
- Git
- GitHub

---

# 📌 Funcionalidades Implementadas

### Funcionalidades disponíveis

- Desenho de linhas
- Desenho livre (rabisco)
- Desenho de retângulos
- Desenho de ovais
- Desenho de círculos
- Desenho de quadrados
- Desenho de triângulos equiláteros
- Desenho de triângulos retângulos
- Desenho de pentágonos
- Desenho de hexágonos
- Desenho de polígonos interativos (3 a 12 lados)
- Escolha de cor da borda
- Escolha de cor de preenchimento
- Opção de remover preenchimento
- Seleção de espessura da linha (1 a 10)
- Visualização em tempo real da figura durante o desenho
- Visualização de vértices e guias ao desenhar polígonos interativos
- Sistema de desfazer (Ctrl + Z)
- Sistema de refazer (Ctrl + Y)

### Ferramentas de desenho

| Ferramenta | Descrição |
|------------|------------|
| Linha | Cria linhas retas |
| Rabisco | Desenho livre acompanhando o movimento do mouse |
| Retângulo | Cria retângulos |
| Quadrado | Cria quadrados proporcionais |
| Oval | Cria elipses |
| Círculo | Cria círculos proporcionais |
| Triângulo | Cria triângulos equiláteros |
| Triângulo Retângulo | Cria triângulos retângulos |
| Pentágono | Cria pentágonos regulares |
| Hexágono | Cria hexágonos regulares |
| Polígono | Cria polígonos interativos com número de lados configurável (3–12) |

---

# 🖥️ Como Executar

## Clone o repositório

```bash
git clone https://github.com/kayobass/drawable-app
```

## Acesse a pasta

```bash
cd drawable-app
```

## Execute o programa

```bash
python main.py
```

---

# 🎨 Interface

A aplicação possui:

- Menu de seleção da ferramenta de desenho
- Seletor de número de lados para polígonos interativos
- Seleção de cor da borda com indicador visual
- Seleção de cor do preenchimento com indicador visual
- Opção de remover preenchimento
- Seletor de espessura da linha
- Área de desenho baseada no widget Canvas do Tkinter (600×600)

---

# ⌨️ Atalhos

| Atalho | Ação |
|---------|--------|
| Ctrl + Z | Desfazer |
| Ctrl + Y | Refazer |
| Botão direito do mouse | Finalizar polígono interativo |

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

## 🔄 Etapa 3 — Em desenvolvimento

Refatoração para o padrão **MVC (Model-View-Controller)**:

- [ ] Definir as classes do modelo (Figuras, Desenho, ...)
- [ ] Definir uma classe ou classes para a visão
- [ ] Definir uma classe ou classes para o(s) controlador(es)

### Estrutura de pastas recomendada

```
drawable-app/
├── .git/
├── .gitignore
├── src/
│   └── drawable_app/
│       ├── main.py
│       ├── modelo/
│       │   └── ...
│       ├── visao/
│       │   └── ...
│       └── controlador/
│           └── ...
```

---

## 🔄 Etapa 4 — Em desenvolvimento

Funcionalidades serão adicionadas conforme os requisitos da disciplina.

- [ ] A definir

---

# 👨‍💻 Equipe

| Integrante      | GitHub |
|-----------------|----|
| Kayo Araujo     | @kayobass |
| Matheuz Rozendo | @matheuzrozendo  |

---

# 📄 Licença

Projeto desenvolvido exclusivamente para fins acadêmicos.