# 🧳 Travel Board — Backend

Backend da aplicação **Travel Board**, desenvolvido com **Python e Flask** como parte do MVP da Sprint de Desenvolvimento Full Stack Básico da Pós-Graduação em Engenharia de Software da PUC-Rio.

---

## ✨ Descrição

A API do Travel Board é responsável pelo gerenciamento dos destinos de viagem, permitindo operações completas de CRUD, filtros e controle de estado.

A aplicação segue o padrão REST e foi estruturada para manter separação de responsabilidades entre camadas.

---

## 🚀 Tecnologias Utilizadas

- Python 3
- Flask
- Flask-CORS
- SQLAlchemy
- SQLite
- Flasgger (Swagger / OpenAPI)

---

## 📁 Estrutura do Projeto

```text
backend/
├── app/
│   ├── routes/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   └── db/
├── run.py
├── requirements.txt
└── README.md
```

---

## 🧠 Arquitetura

A aplicação foi estruturada em camadas:

### Routes
Recebem requisições HTTP e retornam respostas.

### Services
Aplicam regras de negócio e validações.

### Repositories
Responsáveis pela persistência no banco de dados.

### Models
Representam as entidades do domínio.

---

## 📦 Entidade Principal

### Destination

Campos:

- id
- name
- country
- city
- category
- planned_date
- estimated_budget
- status
- notes
- is_favorite
- created_at

---

## 🔁 Rotas da API

### CRUD

- `GET /destinations`
- `GET /destinations/<id>`
- `POST /destinations`
- `PUT /destinations/<id>`
- `DELETE /destinations/<id>`

### Extras

- `PUT /destinations/<id>/favorite`
- `GET /destinations?status=&category=&search=&page=&per_page=`

---

## 🔎 Filtros

A API permite:

- filtro por status
- filtro por categoria
- busca textual (nome e cidade)
- paginação

Exemplo:

```text
GET /destinations?status=planned&category=city&search=montreal&page=1&per_page=6
```

---

## 📚 Documentação (Swagger)

A API possui documentação interativa com Swagger, incluindo:

- descrição das rotas
- parâmetros
- exemplos de request/response
- códigos de status

---

## ▶️ Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/travel-board-backend.git
```

### 2. Acesse a pasta

```bash
cd travel-board-backend
```

### 3. Crie e ative o ambiente virtual

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Execute a aplicação

```bash
python run.py
```

A API estará disponível em:

```text
http://127.0.0.1:5001
```
E a Documentação Swagger da API estará disponível em:

```text
http://127.0.0.1:5001/apidocs/
```

---

## 🗃️ Banco de Dados

- SQLite
- Persistência via SQLAlchemy
- Paginação nativa

---

## 🧠 Regras de Negócio

- Campos obrigatórios:
  - name
  - country
  - city
  - category
  - status

- Status permitidos:
  - idea
  - planned
  - booked
  - visited

- Categorias permitidas:
  - beach
  - city
  - mountain
  - cultural
  - adventure

- Validação de:
  - datas
  - orçamento
  - tipos de dados

---

## ✅ Requisitos Atendidos

- API REST com Flask
- mínimo de 4 rotas
- uso de método POST
- persistência com SQLite
- documentação Swagger
- organização em camadas
- separação de projetos frontend/backend

---

## 💡 Melhorias Futuras

- autenticação de usuários
- múltiplas tabelas (trips)
- dashboard de métricas
- integração com APIs externas
- histórico de alterações

---

## 👩‍💻 Autora

Pamela Fabia Iglesias de Godoy  
Projeto acadêmico — MVP 1  
Pós-Graduação em Engenharia de Software — PUC-Rio
