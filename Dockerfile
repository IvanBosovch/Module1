FROM python:3.11

ENV APP /Module1

WORKDIR $APP

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "group2/main.py"]

