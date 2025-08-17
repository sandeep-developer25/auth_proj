FROM python:3.10-slim

WORKDIR /flaskapp

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# COPY . /flaskapp
# CMD ["python", "/flaskapp/app.py", "--reload"]

CMD ["python", "app.py", "--reload"]