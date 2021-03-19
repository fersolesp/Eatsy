% prepara el repositorio para su despliegue. 
release: sh -c 'cd Eatsy && python manage.py migrate'
% especifica el comando para lanzar Eatsy
web: sh -c 'cd Eatsy && gunicorn Eatsy.wsgi --log-file -'