# запуск миграций
PYTHONPATH=. alembic upgrade head

# запуск процессов
supervisord -c /etc/supervisor/conf.d/supervisord.conf
