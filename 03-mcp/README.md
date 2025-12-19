## MCP homework — reproduction quick guide

But: ce README explique rapidement comment reproduire les trois questions du devoir (uv, FastMCP, et l'outil de scraping via r.jina.ai).

1) Préparer l'environnement (Windows / PowerShell)

 - Créer et activer un venv (optionnel mais recommandé) :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

 - Installer `uv` (gestionnaire de dépendances utilisé dans l'exo) :

```powershell
python -m pip install uv
```

 - Initialiser le projet et ajouter `fastmcp` :

```powershell
uv init
uv add fastmcp
```

2) Question 1 — trouver le hash dans `uv.lock`

 - Ouvrez `uv.lock` et cherchez la section `[[package]]` pour `name = "fastmcp"`.
 - Dans la sous-section `wheels` vous verrez des objets avec `hash = "sha256:..."`.
 - Copiez la première valeur `sha256:...` (entière, sans guillemets). Par exemple, dans cet exercice le premier hash trouvé pour la roue `fastmcp-2.14.1-py3-none-any.whl` est :

```
sha256:fb3e365cc1d52573ab89caeba9944dd4b056149097be169bce428e011f0a57e5
```

3) Question 2 — lancer le serveur FastMCP (starter code)

 - Le fichier `server.py` contient le code starter. Lancez-le :

```powershell
python server.py
```

 - Quand l'interface d'accueil apparaît, notez le transport indiqué (réponse attendue : `STDIO`, `HTTP`, `HTTPS` ou `SSE`).

4) Question 3 — Scrape Web Tool (Jina reader)

 - Jina reader renvoie la page en markdown si vous préfixez l'URL par `https://r.jina.ai/`.
 - Pour tester rapidement sans ajouter de code au dépôt, utilisez un one‑liner Python pour récupérer et compter les caractères :

```powershell
python -c "import requests; print(len(requests.get('https://r.jina.ai/https://github.com/alexeygrigorev/minsearch').text))"
```

 - Si vous préférez un petit script `scrape.py` (à créer localement) :

```python
import requests
url = 'https://r.jina.ai/https://github.com/alexeygrigorev/minsearch'
print(len(requests.get(url).text))
```

Remarques importantes
- Les variations de l'URL (ajout d'un slash final, usage de la page `raw` vs `blob` vs la page HTML du repo) changent le contenu renvoyé par r.jina.ai — donc la longueur peut varier.
- Les en‑têtes HTTP (User-Agent) peuvent parfois influencer le rendu, mais ce n'est pas systématique.
- Pour la question 3 du devoir, si votre run local ne retourne pas exactement `29184`, choisissez la valeur la plus proche parmi les options fournies — dans mes essais la valeur la plus proche était `29184`.

Si vous voulez, je peux ajouter un petit script `fetch_save.py` qui sauvegarde la sortie et la compare automatiquement à un fichier attendu. Voulez-vous que je l'ajoute dans le dépôt ?
