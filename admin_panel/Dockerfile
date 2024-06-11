FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

CMD ["sh", "-c", "python admin_panel/manage.py migrate && python admin_panel/manage.py runserver 0.0.0.0:8000"]