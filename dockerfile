#imagen de Python
FROM python:3.10

#directorio de trabajo
WORKDIR /app

#archivos necesarios
COPY requirements.txt ./

#Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

#Copiamos el codigo fuente
COPY . .

#Puerto en el que se corre la API
EXPOSE 5000

#Ejecutar aplicacion
CMD ["python", "run.py"]