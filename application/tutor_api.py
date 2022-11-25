import logging
import tutor

from flask import Flask, jsonify


LOG = logging.getLogger(__name__)

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)


@app.get("/tutor/health")
def get_health():
    LOG.info("Health check of tutor has been requested")
    return jsonify("UP")


@app.get("/")
def get_root():
    LOG.info("Root call, redirecting...")
    return app.redirect("/tutor/health")


@app.get("/tutor/questions")
def get_questions():
    LOG.info("Available questions have been requested...")
    return jsonify(tutor.get_questions())


if __name__ == '__main__':
    app.run(host="localhost", port=3030, debug=True)
