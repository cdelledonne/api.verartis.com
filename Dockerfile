FROM python:3.10

WORKDIR /api.verartis.com

COPY ./requirements.txt /api.verartis.com/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api.verartis.com/requirements.txt

COPY ./app /api.verartis.com/app

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
