@echo off
if not exist shopping (
    python -m venv shopping
)
call shopping\Scripts\activate
pip install -r requirements.txt
flask db init
flask db migrate
flask db upgrade
flask run