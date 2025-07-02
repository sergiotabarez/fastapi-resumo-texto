# Use uma imagem base Python otimizada para slim builds
FROM python:3.11-slim-buster

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo requirements.txt para o container
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o container
COPY main.py .

# Expõe a porta que o Uvicorn estará escutando
EXPOSE 8000

# Comando para rodar a aplicação quando o container iniciar
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]