# ML in Production — Prédiction du prix des maisons

Mini-projet : entraînement d'une régression linéaire, interface Streamlit,
API FastAPI et déploiement avec Docker.

Dépôt à remettre : https://github.com/totosoubi/MLprod1

## Installation et entraînement

Depuis la racine du dépôt, avec Python 3.12 ou ultérieur :

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python train_model.py
```

L'entraînement utilise `houses.csv` et génère `regression.joblib` à côté du
script. Réentraîner le modèle après une mise à jour de scikit-learn.

Les entrées sont `size` (surface positive ou nulle), `nb_rooms` (nombre entier
positif ou nul de chambres) et `garden` (0 sans jardin, 1 avec jardin).

## Streamlit

```bash
streamlit run model_app.py
```

Ouvrir http://localhost:8501, remplir les trois champs puis cliquer sur
**Prédire**. Le résultat apparaît avec `st.metric` et `st.write`.

## Niveau 0 — API locale

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Dans un autre terminal avec l'environnement virtuel activé :

```bash
python test_requests.py
```

Ce script envoie une requête GET et une requête POST, vérifie leurs statuts
HTTP et compare leurs prédictions.

Test GET dans le navigateur :
http://127.0.0.1:8000/predict?size=120&nb_rooms=3&garden=1

Test POST avec curl :

```bash
curl --fail-with-body -X POST http://127.0.0.1:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"size":120,"nb_rooms":3,"garden":1}'
```

Réponse : `{"y_pred": <prix prédit>}`. Les données invalides ou manquantes
retournent HTTP 422. L'étape initiale du TP renvoyant la constante 2 est
remplacée par la prédiction du modèle dans la version finale.

Avec les données fournies, l'exemple ci-dessus retourne environ
`{"y_pred": 289962.4945993448}`.

Pour un client graphique, ouvrir http://127.0.0.1:8000/docs et utiliser
**Try it out** sur POST `/predict`, ou envoyer le même JSON avec Postman ou
Insomnia.

## Tests automatisés

```bash
python -m pip install -r requirements-dev.txt
python -m unittest -v test_app
```

Ces tests vérifient que GET et POST renvoient le résultat du modèle, que les
entrées invalides sont rejetées et que le formulaire Streamlit affiche la
prédiction après soumission.

## Niveau 0.5 — API sur la machine distante

L'adresse utilisée précédemment pour le TP est `20.86.80.79`, avec le dossier
`/home/ubuntu/ts`. Confirmer cette adresse auprès du formateur si la VM a changé.

```bash
ssh ubuntu@20.86.80.79 'mkdir -p /home/ubuntu/ts'
scp main.py train_model.py houses.csv requirements.txt ubuntu@20.86.80.79:/home/ubuntu/ts/
ssh ubuntu@20.86.80.79
cd /home/ubuntu/ts
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python train_model.py
uvicorn main:app --host 0.0.0.0 --port 8002
```

Le port 8002 permet d'éviter les ports 8000 et 8001 utilisés précédemment.
Le port choisi doit être accessible dans les règles réseau de la VM.

Depuis votre machine, puis depuis celle d'un collègue :

```bash
python test_requests.py --url http://20.86.80.79:8002
```

Arrêter ce serveur avec Ctrl+C avant d'utiliser le même port avec Docker.

## Niveau 1 — Docker local

Démarrer Docker Desktop ou le moteur Docker, puis :

```bash
docker build -t house-price-api .
docker run -d --name house-price-api -p 8000:8000 house-price-api
python test_requests.py
```

L'image entraîne le modèle pendant sa construction. Le serveur écoute sur
`0.0.0.0:8000` dans le conteneur et `-p` publie ce port sur la machine hôte.

```bash
docker logs house-price-api
docker stop house-price-api
docker rm house-price-api
```

## Niveau 2 — Docker sur la VM

Après avoir arrêté le serveur du niveau 0.5, copier les fichiers de construction :

```bash
scp Dockerfile .dockerignore main.py train_model.py houses.csv requirements.txt \
  ubuntu@20.86.80.79:/home/ubuntu/ts/
ssh ubuntu@20.86.80.79
cd /home/ubuntu/ts
sudo docker build -t ts-house-price-api .
sudo docker run -d --restart unless-stopped \
  --name ts-house-price-api -p 8002:8000 ts-house-price-api
sudo docker ps --filter name=ts-house-price-api
sudo docker logs ts-house-price-api
```

Si un ancien conteneur du projet porte déjà ce nom, l'arrêter et le supprimer
avant de lancer sa nouvelle version :

```bash
sudo docker stop ts-house-price-api
sudo docker rm ts-house-price-api
```

Depuis votre machine puis celle d'un collègue, vérifier :

```bash
python test_requests.py --url http://20.86.80.79:8002
```

Documentation distante : http://20.86.80.79:8002/docs

## Validation effectuée le 21 octobre 2026

- Modèle réentraîné avec les dépendances fixées dans `requirements.txt`.
- Quatre tests automatisés réussis : prédictions GET/POST, valeurs invalides,
  champs manquants et soumission du formulaire Streamlit.
- Requêtes HTTP GET et POST réussies sur le serveur local.
- Image Docker construite et conteneur testé via un port publié : prédictions
  GET/POST réussies, `/docs` en HTTP 200, valeurs invalides en HTTP 422.
- Connexions SSH et HTTP à la VM `20.86.80.79` expirées : le déploiement
  distant reste à revalider dès que la VM est accessible.
- L'accès depuis la machine d'un collègue reste à confirmer pour valider
  entièrement le TP.
