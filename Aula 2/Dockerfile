# Usando uma imagem base do Python
FROM python:3.10-slim

# Definindo o diretório de trabalho dentro do container
WORKDIR /app

# Copiando o arquivo Python para o diretório de trabalho no container
COPY gigastore.py .
# COPY ./app .

# Comando para executar o script Python
CMD ["python", "gigastore.py"]