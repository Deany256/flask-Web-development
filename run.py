from app import create_app
from config import config
import os

# Determine the configuration to use
config_name = os.getenv('FLASK_CONFIG', 'default')

# Create the app instance with the selected configuration
app = create_app(config_class=config[config_name])

if __name__ == '__main__':
    app.run()