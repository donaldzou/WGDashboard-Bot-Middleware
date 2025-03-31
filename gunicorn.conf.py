from datetime import datetime

date = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
pidfile = './gunicorn.pid'
wsgi_app = "main:app"
bind = "0.0.0.0:80"
workers = 2
accesslog = f"./log/access_{date}.log"
log_level = "debug"
capture_output = True
errorlog = f"./log/error_{date}.log"
# daemon = True