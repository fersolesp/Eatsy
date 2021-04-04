% prepara el repositorio para su despliegue. 
release: python ./manage.py makemigrations && python manage.py migrate && python manage.py flush --noinput && python ./manage.py loaddata datosEjemplo.json
% especifica el comando para lanzar Eatsy
web: gunicorn Eatsy.wsgi --log-file -