% prepara el repositorio para su despliegue. 
release: python manage.py migrate
% especifica el comando para lanzar Eatsy
web: gunicorn Eatsy.wsgi --log-file -