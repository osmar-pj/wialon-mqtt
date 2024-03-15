# Usamos una imagen base de Python
# FROM --platform=amd64  python:3.11.3-slim-buster
FROM  python:3.11.3-slim-buster

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos a la imagen
COPY requirements.txt .

# Instalar las dependencias especificadas en requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación a la imagen
COPY . .

# Exponer el puerto 5000
EXPOSE 5200

# Ejecutar el comando para iniciar la aplicación
CMD ["python3", "src/app.py"]