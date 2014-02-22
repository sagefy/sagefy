from app import app
import controllers.user
import controllers.notification
import controllers.message


@app.route('/api/')
def api_index():
    """
    View a documentation page.
    """
    return 'Welcome to the Sagefy API.'


if __name__ == '__main__':
    app.run()
