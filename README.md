# ApiGithubRepo

Esta api fue creada para obtener la informacion de todos los repositorios de un usuario de
github y tambien la actividad de un usuario en su cuenta de github

## uso

Clonar este repositorio 

```
git clone https://github.com/davidG199/ApiGithubRepo.git
```

Crear el entorno virtual para python

```
py -m venv venv
```

activa el entorno virtual

```
venv/Scripts/activate
```

instala las dependencias

```
pip install -r requirements.txt
```

## en el archivo .env.example esta el ejemplo para escribir las variables de entorno para su usuario y su token

inicia la api

```
uvicorn main:app --reload
```



