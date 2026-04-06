#!/bin/bash
celery -A FormulaSeasonTracker worker --loglevel=info --detach --pidfile=/tmp/celery.pid --logfile=/tmp/celery.log
gunicorn --bind=0.0.0.0:8000 --timeout 600 FormulaSeasonTracker.wsgi