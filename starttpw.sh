if [ $MODE == 'simple' ]
then
  flask run -h 0.0.0.0
else
  uwsgi uwsgiconf.ini
fi