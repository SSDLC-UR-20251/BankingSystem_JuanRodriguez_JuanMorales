FROM python:3.11-alpine
WORKDIR /app
COPY . .
RUN pip install -r requiriments.txt
CMD ["python", "run.py"]
