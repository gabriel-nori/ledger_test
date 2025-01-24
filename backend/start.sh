python3 -m pip install -r requirements.txt
python3 manage.py collectstatic
python3 -m uvicorn config.asgi:application --host 0.0.0.0 --port 8000