% prepara el repositorio para su despliegue. 
release: sh -c 'python manage.py migrate'
% especifica el comando para lanzar Eatsy
web: sh -c 'gunicorn Eatsy.wsgi --log-file -'