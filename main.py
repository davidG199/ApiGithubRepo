from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.title = "Api Github Repo"
app.version = "0.0.1"

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["home"])
def root():
    return HTMLResponse("<h1>Api github repo</h1>")

@app.get("/repos")
async def get_github_repos():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.mercy-preview+json"
    } if GITHUB_TOKEN else {}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al consultar GitHub")

    repos = response.json()

    async def obtener_lenguajes(lenguajes_url):
        async with httpx.AsyncClient() as client:
            r = await client.get(lenguajes_url, headers=headers)
            if r.status_code == 200:
                return list(r.json().keys())
            return []

    tareas = [obtener_lenguajes(repo["languages_url"]) for repo in repos]
    lenguajes_repos = await asyncio.gather(*tareas)

    datos_repos = []
    for i, repo in enumerate(repos):
        datos_repos.append({
            "name": repo["name"],
            "html_url": repo["html_url"],
            "description": repo["description"],
            "languages": lenguajes_repos[i],
            "topics": repo.get("topics", []),
            "created_at": repo["created_at"],
            "homepage": repo["homepage"] if repo["homepage"] else None,
        })

    return datos_repos

@app.get("/actividad")
async def get_github_activity():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/events/public"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al consultar eventos")

    eventos = response.json()

    actividad = []
    for evento in eventos[:10]:  # los últimos 10 eventos
        actividad.append({
            "tipo": evento["type"],
            "repo": evento["repo"]["name"],
            "fecha": evento["created_at"],
        })

    return actividad



