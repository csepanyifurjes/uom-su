import logging
import tutor

from flask import Flask, request, jsonify


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


@app.post("/tutor/evaluate")
def evaluate_learners_answer():
    if request.is_json:
        learners_answer = request.get_json()
        LOG.debug(learners_answer)
        question_id = learners_answer["id"]
        answer = learners_answer["answer"]
        client_info = request.headers.get("User-Agent")
        try:
            result = tutor.evaluate_learners_answer(question_id, answer, client_info)
        except ValueError as e:
            return jsonify(e.args[0])
        return jsonify({"result": result}), 200
    return {"error": "Request must be JSON"}, 415


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3030, debug=True)
