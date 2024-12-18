from admin.config import ADMIN_HOST, ADMIN_PORT, DEBUG

reload = DEBUG

# The address and port your Flask app will listen on
bind = f"{ADMIN_HOST}:{ADMIN_PORT}"

# Number of workers. Gunicorn recommends 2-4 workers per core
workers = 2

# The location of your Flask app
wsgi_app = "admin.app:app"

# Set logging - this example logs to a file
accesslog = "-"
errorlog = "-"

timeout = 120  # 默认是30秒
keepalive = 5

# 增加 worker 类型
worker_class = "sync"
