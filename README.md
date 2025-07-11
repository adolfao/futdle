# futdle

# 🟢 Projeto Futdle — Escopo Geral

## 🎯 Objetivo
Criar um jogo estilo Loodle onde o jogador precisa adivinhar um **time de futebol brasileiro** com base em dicas visuais e textuais.

## 🧱 Tecnologias Utilizadas
- **Back-end**: Flask (Python)
- **Front-end**: HTML + Bootstrap (provavelmente)
- **Banco de Dados**: PostgreSQL (provavelmente)
- **APIs externas**: indefinido
- **Deploy**: será feito no final

## 🧩 Modos de Jogo

### 🔹 Clássico
- Jogador digita o nome de um time.
- Retorno com as dicas comparadas ao time correto com cores:
  - 🟢 Verde: acerto completo
  - 🟡 Amarelo: parcialmente correto
  - 🔴 Vermelho: incorreto

#### 🗂️ Dados exibidos inicialmente:
- Nome
- Estado
- Cores
- Ano de fundação (com seta ↑ ou ↓)

#### 💡 Dicas adicionais (podem aparecer conforme a dificuldade ou tentativas):
- Participação em competição continental, mundial ou Série A
- Títulos estaduais
- Mascote
- Apelido
- Sigla do time
- Número de letras do nome

- Dificuldade ajustável:
  - Muda o tipo/quantidade de dicas
  - Permite restringir os times por série (A, B, C, D)
  - Modo padrão: séries A, B e C
- Cada página de modo terá explicação inicial
- Ajuda extra pode aparecer após X tentativas erradas
- O jogador pode jogar os desafios dos dias anteriores
- Os times mudam diariamente

### 🔹 Hino
- Jogador adivinha o time com base em:
  - Trecho do hino (curto ou progressivamente maior)
  - Dicas secundárias (como no modo Clássico)

### 🔹 Escudo
- Escudo inicial:
  - Extremamente borrado ou com zoom-in excessivo
  - Preto e branco, rotacionado
- Conforme o jogador erra:
  - Escudo gira na posição correta
  - Ganha cor
  - Imagem é desembaçada
- Pode ser dividido em dois modos: "Borrado" e "Zoom"

### 🔹 Mascote
- Funciona como o escudo
- Começa borrado ou cortado
- Inicialmente restrito aos mascotes dos times da Série A

## 🌱 Ideias Futuras
- Modo Geografia (mapa/localização)
- Modo Uniforme (partes do uniforme)
- Modo Anagrama (nome embaralhado)
- Modo Linha do Tempo (eventos históricos)
- Modo Reverso (ver o que não bate com o time correto)
- Modo com jogadores

## 🧠 Estratégia de Desenvolvimento
- Sem foco em design nem segurança inicialmente
- Linguagem e estrutura simples para facilitar o desenvolvimento solo
- Complexidade controlada para garantir avanço constante
- Deploy será visto apenas ao final do projeto

## 🗂️ Página Inicial
- Imagem de fundo: visão da grama e arquibancadas de um estádio
- Logo do Futdle centralizada
- Botões para os modos de jogo

---
