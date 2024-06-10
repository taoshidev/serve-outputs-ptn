FROM python:3.10-bookworm

COPY . /app
WORKDIR /app

EXPOSE 48888
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "serve.py"]

