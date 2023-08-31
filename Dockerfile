# start from an official image
FROM python:3.9-slim

# arbitrary location choice: you can change the directory
RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

# install our dependencies
# we use --system flag because we don't need an extra virtualenv
COPY requirements.txt /opt/services/djangoapp/src/
RUN pip install -r requirements.txt
RUN pip install gunicorn
# copy our project code
COPY frontend/thinking /opt/services/djangoapp/src
COPY  poe /opt/services/djangoapp/src/poe
COPY  poe/constants.py /opt/services/djangoapp/src/
RUN python manage.py collectstatic --no-input -v 2

# expose the port 8000
EXPOSE 80
ENV PYTHONUNBUFFERED=1

# define the default command to run when starting the container
CMD ["gunicorn", "--chdir", "thinking", "--bind", ":80", "thinking.wsgi:application"]