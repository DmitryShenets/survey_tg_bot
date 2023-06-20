FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN python -m pip install --upgrade pip

WORKDIR /usr/src/app

COPY . .

RUN chmod +x entrypoint.sh
RUN chmod +x run.py

RUN python -m pip install --upgrade pip
RUN pip install -r requirements/requirements.txt

CMD ["sh", "entrypoint.sh"]