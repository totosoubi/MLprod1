# ML in Production - House Price Prediction

## Entrainer le modele

```bash
python3 train_model.py
```

Cette commande genere `regression.joblib`.

## Lancer l'application Streamlit

```bash
streamlit run model_app.py
```

## Lancer l'API FastAPI en local

```bash
uvicorn main:app --reload
```

Exemples de test:

```bash
wget -qO- "http://127.0.0.1:8000/predict?size=120&nb_rooms=3&garden=1"
python3 test_requests.py
```

Requete POST:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"size": 120, "nb_rooms": 3, "garden": 1}'
```

## Docker

```bash
docker build -t house-price-api .
docker run --rm -p 8000:8000 house-price-api
```

Puis tester:

```bash
wget -qO- "http://127.0.0.1:8000/predict?size=120&nb_rooms=3&garden=1"
```

## Deploiement sur la VM

Le projet est deploye dans `/home/ubuntu/ts` sur la VM `20.86.80.79`.
Le port `8002` est utilise car les ports `8000` et `8001` etaient deja occupes.

```bash
cd /home/ubuntu/ts
sudo docker build -t ts-house-price-api .
sudo docker run -d --restart unless-stopped \
  --name ts-house-price-api \
  -p 8002:8000 \
  ts-house-price-api
```

Verifier le conteneur:

```bash
sudo docker ps --filter name=ts-house-price-api
```

Tester l'API depuis une autre machine:

```bash
wget -qO- "http://20.86.80.79:8002/predict?size=120&nb_rooms=3&garden=1"
```

La documentation interactive FastAPI est disponible sur:

```text
http://20.86.80.79:8002/docs
```
