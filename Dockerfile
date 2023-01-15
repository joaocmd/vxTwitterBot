FROM python:3.9

COPY main.py config.json requirements.txt ./

RUN pip install -r requirements.txt
CMD ["python", "./main.py"]
