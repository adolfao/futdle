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

## 📦 Como rodar o projeto localmente

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/futdle.git
   cd futdle
   ```

2. **Crie e ative o ambiente virtual:**

   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # No Windows
   # ou
   source venv/bin/activate  # No Linux/Mac
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados:**

   ```bash
   # Execute o script para popular a base de dados com times brasileiros
   python -m futdle.tests_db.tests
   ```

   **Scripts de teste disponíveis:**

   ```bash
   # Listar todos os times na base de dados
   python -m futdle.tests_db.test_nomes

   # Verificar anos de fundação dos times
   python -m futdle.tests_db.test_anos

   # Verificar cores dos times
   python -m futdle.tests_db.test_cores
   ```

5. **Execute a aplicação:**

   ```bash
   python -m flask --app futdle run --debug
   ```

6. **Acesse no navegador:**
   ```
   http://127.0.0.1:5000
   ```

### 🎮 Modos de Jogo Disponíveis

- **Modo Clássico** (`/classico`): Adivinhe o time baseado em cores, estado e ano de fundação
  - 🟢 Verde: acerto completo
  - 🟡 Amarelo: acerto parcial (cores)
  - 🔴 Vermelho: incorreto
  - ↑↓ Setas: indicam se o ano é maior ou menor

### 🗃️ Base de Dados

O projeto inclui 20 times brasileiros das principais séries:

- Atlético Mineiro, Bahia, Botafogo, Bragantino, Ceará
- Corinthians, Cruzeiro, Flamengo, Fluminense, Fortaleza
- Grêmio, Internacional, Juventude, Mirassol, Palmeiras
- Santos, Sport, São Paulo, Vasco da Gama, Vitória

---

> Este arquivo README foi gerado com auxílio do ChatGPT (OpenAI) em julho de 2025 para fins de documentação e organização do projeto Futdle.
