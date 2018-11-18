from flask import Flask, render_template
import sys

app = Flask(__name__, template_folder='templates')

app.secret_key = '*****^&&#^@&@&@12348akubingung&&&&**&&&&@@@@' # secret key

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from post import post as post_blueprint
app.register_blueprint(post_blueprint)

if __name__ == '__main__':
	app.run(debug=True)