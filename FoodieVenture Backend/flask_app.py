from flaskApp import app
from flaskApp import manager

from flask_cors import CORS  

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# if __name__ == '__main__':
#     app.run(debug=True)

# for migrations
# python run.py db init
# python run.py migrate
# python run.py upgrade
# if __name__ == '__main__':
#     manager.run()
