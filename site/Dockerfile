FROM python:3.7

RUN mkdir -p /opt/services/thiccsite/src
WORKDIR /opt/services/thiccsite/src

#COPY Pipfile Pipfile.lock /opt/services/thiccsite/src/
COPY requirements.txt /opt/services/thiccsite/src/
#RUN pip install pipenv && pipenv install --system
RUN pip --use-deprecated=legacy-resolver install -r requirements.txt

COPY . /opt/services/thiccsite/src

EXPOSE 8000
#CMD ["gunicorn", "-b", ":8000", "thicc.wsgi:application"]
#CMD ["python", "manage.py", "runserver"]

