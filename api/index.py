from app import create_app
import config
app = create_app(config, debug=True)  # TODO: Turn this off!
