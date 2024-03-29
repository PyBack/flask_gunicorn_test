import os
import site
import traceback

from logging.config import dictConfig

from flask import Flask, jsonify
from flask import Blueprint
from flask_cors import CORS
# from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy

# from dotenv import load_dotenv

src_path = os.path.dirname(__file__)
pjt_home_path = os.path.join(src_path, os.pardir)
pjt_home_path = os.path.abspath(pjt_home_path)
site.addsitedir(pjt_home_path)

from views import controller as ctrl

# Flask 환경 변수
FLASK_ENV = 'development'
FLASK_RUN_PORT = 5500
FLASK_DEBUG = True

# Flask root logger config
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '%(asctime)s [%(levelname)s] %(filename)s %(lineno)d: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

# instantiate the app
app = Flask(__name__)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# app.register_blueprint(get_bp_v1())
app.register_blueprint(ctrl.blueprint)
ctrl.create_equity_namespace()


@app.route('/', methods=['GET'])
def health_check():
    app.logger.info('flaskapi good')
    return jsonify('flaskapi good')


@app.route('/traceback-test', methods=['GET'])
def traceback_test_router():
    msg = 'ok'
    try:
        int('k')
    except:
        msg = traceback.format_exc()
        app.logger.error(msg)
    return jsonify(error=msg), 500


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=os.environ.get('FLASK_RUN_PORT'), debug=os.environ.get('FLASK_DEBUG'))
    app.run(host='0.0.0.0', port=FLASK_RUN_PORT, debug=FLASK_DEBUG)