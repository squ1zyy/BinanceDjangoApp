FROM python

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r req.txt

RUN python main_app/manage.py migrate

CMD ["python", "main_app/manage.py", "runserver", "0.0.0.0:8000"]