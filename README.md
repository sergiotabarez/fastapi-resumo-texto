
# 🧠 API de Resumo de Textos com LLM (distilBART)

Este projeto é uma API REST desenvolvida com **FastAPI** que utiliza um modelo pré-treinado da Hugging Face, o `distilbart-cnn-12-6`, para gerar **resumos automáticos de textos**.

O código foi desenvolvido no **Google Colab** e empacotado em container com **Docker Desktop no Windows**, facilitando a execução local ou futura publicação em ambientes de produção.

---

## 🚀 Tecnologias Utilizadas

- Python 3.10+
- FastAPI
- PyTorch
- Hugging Face Transformers
- Docker (build local com Docker Desktop)

---

## 📦 Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
```

---

### 2. Build da imagem Docker

```bash
docker build -t resumo-api .
```

---

### 3. Execução do container

```bash
docker run -p 8000:8000 resumo-api
```

---

## 📌 Endpoints Disponíveis

### `GET /`
Verifica se a API está ativa.
**Resposta esperada:**
```json
{ "message": "Bem-vindo à API de Resumo de Textos com LLM!" }
```

---

### `POST /summarize/`
Gera o resumo de um texto fornecido.

**Payload de entrada:**
```json
{
  "text": "Seu texto longo aqui..."
}
```

**Resposta de saída:**
```json
{
  "summary": "Resumo gerado...",
  "original_length": 1234,
  "summary_length": 234,
  "compression_ratio": 81.04
}
```

---

## 👤 Autor

**Sergio Tabarez**  
🔗 [LinkedIn](https://linkedin.com/in/sergiotabarez)  
💻 [GitHub](https://github.com/sergiotabarez)

---

## 🏗️ Observações

- O modelo utilizado (`distilbart-cnn-12-6`) é carregado diretamente do repositório Hugging Face.
- Projeto idealizado como parte de um portfólio técnico com foco em **LLMs aplicados a NLP**.
