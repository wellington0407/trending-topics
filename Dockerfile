# Use uma imagem base do Python
FROM python:3.9

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requisitos para o contêiner
COPY requirements.txt .

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Adicione todo o conteúdo do diretório atual para o diretório de trabalho no contêiner
ADD . .

# Exponha a porta em que a aplicação está sendo executada
EXPOSE 8000

# Comando para iniciar a aplicação quando o contêiner for iniciado
CMD ["uvicorn", "trend_top:app", "--host", "0.0.0.0", "--port", "8000"]
