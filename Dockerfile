FROM python:3.9

COPY . .

RUN pip install -r requirements.txt
CMD ["python", "./main.py"]
