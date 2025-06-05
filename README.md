Este proyecto funciona como una aplicacion centrada en Programacion Funcional y Reactiva que se divide en tres modulos

Antes de pasar al despliegue de cada uno es necesario tener un .env en la raiz del proyecto con las siguientes variables definidas

DB_HOST
POSTGRES_PORT
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
JWT_SECRET_KEY

1. Base de datos
Esta se despliega en el proyecto a traves de docker usando el .yml de la raiz del proyecto, los valores del .env y el archivo .sql
para crear el modelo de datos.

2. Back-end
Es necesario tener instaladas las dependencias definidas en el requirements.txt en el entorno de ejecucion de Python
Una vez hecho esto desde la carpeta back-end se despliega este modulo con el siguiente comando

  uvicorn main:app --reload

3. Front-end
Para instalar las dependencias se utilza el siguiente comando desde la carpeta front

  npm install

Una vez hecho esto, el proyecto se despliega en esa misma carpeta usando

  npm run start
