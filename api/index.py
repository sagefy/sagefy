from app import create_app
import config
app = create_app(config)
app.debug = True  # TODO: disable in production
