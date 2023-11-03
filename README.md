
# Health-Service

## Database
Make an env file in root directory containing a connector string like: 
```
DB_CONN = "sqlite:///./service.db"
```

## Docker
Creating docker container and running the app:
```
docker build -t healthservice .
docker run -p 8443:8443 healthservice
```

## Development

Windows Powershell:

```sh
python -m venv .venv
.venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -e .
```

### Start Microservice

```
uvicorn app.server:app --reload
```





