import os
from hypercorn.asyncio import serve
from hypercorn.config import Config as HypercornConfig
from EmployeeHealthMonitor.app import create_app

os.environ.setdefault('FLASK_ENV', 'production')
app = create_app()
