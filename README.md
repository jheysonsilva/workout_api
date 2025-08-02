# Workout API - Backend em Python com FastAPI

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.95-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 🚀 Sobre o Projeto

Workout API é um projeto desenvolvido durante o curso de Backend com Python da [Digital Innovation One (DIO)](https://digitalinnovation.one) com patrocínio do Santander.  
Essa API gerencia informações de atletas, categorias e centros de treinamento, trazendo funcionalidades robustas para filtros avançados, paginação e tratamento de erros personalizado.  

Este projeto é uma porta de entrada para o mercado de trabalho na área de desenvolvimento backend, demonstrando habilidades práticas em Python, FastAPI, SQLAlchemy e boas práticas de API REST.

---

## 💡 Funcionalidades

- **Endpoints com Query Parameters** para filtrar recursos, ex:  
  - Atleta por `nome` e `cpf`  
- **Resposta customizada** nos endpoints GET, incluindo dados relacionados de `categoria` e `centro_treinamento` para atletas.  
- **Tratamento de exceções** para integridade de dados, utilizando `sqlalchemy.exc.IntegrityError` com retorno personalizado:  
  - Exemplo: `"Já existe um atleta cadastrado com o cpf: x"`  
  - Status HTTP: `303 See Other`  
- **Paginação** implementada com a biblioteca [fastapi-pagination](https://github.com/uriyyo/fastapi-pagination), suportando parâmetros `limit` e `offset` para resultados paginados em listagens.

---

## 🛠 Tecnologias Utilizadas

- Python 3.11  
- FastAPI  
- SQLAlchemy (ORM)  
- PostgreSQL (ou outro banco configurável)  
- fastapi-pagination  
- Pydantic (para schemas e validação)  
- Uvicorn (servidor ASGI)  

---

## 📁 Estrutura do Projeto

```

workoutapi/
├── workout\_api/
│   ├── atleta/
│   ├── categorias/
│   ├── centro\_treinamento/
│   ├── configs/
│   ├── contrib/
│   ├── main.py
│   └── ...
├── tests/
├── README.md
└── requirements.txt

````

---

## 🔧 Como Rodar Localmente

1. Clone o repositório:  
```bash
git clone https://github.com/jheysonsilva/workout_api.git
cd workout_api
````

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate   # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure seu banco de dados e variáveis de ambiente (ex: `.env`).

5. Execute a aplicação:

```bash
uvicorn workout_api.main:app --reload
```

6. Acesse a documentação interativa no navegador:

```
http://127.0.0.1:8000/docs
```

---

## 🙏 Agradecimentos

Este projeto foi desenvolvido durante o curso **Backend com Python** da [Digital Innovation One (DIO)](https://digitalinnovation.one), oferecido pelo **Santander**.
Sou grato(a) por todo conhecimento compartilhado, que ampliou meus horizontes e me permitiu construir esta API com qualidade e profissionalismo.

---

## 📬 Contato

Sinta-se à vontade para conectar comigo no LinkedIn:
Jheyson Silva https://www.linkedin.com/in/jheyson-silva-siqueira

Quer que eu gere o arquivo `README.md` para você baixar?
```
