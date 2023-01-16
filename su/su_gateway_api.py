import logging

from config import SYNERGY_UNITS
from flask import Flask, jsonify, send_file, request
from io import BytesIO

LOG = logging.getLogger(__name__)

app = Flask(__name__)


report_su = SYNERGY_UNITS['report']['class']()
explain_su = SYNERGY_UNITS['explain']['class']()
control_su = SYNERGY_UNITS['control']['class']()
teach_su = SYNERGY_UNITS['teach']['class']()
future_su = SYNERGY_UNITS['future']['class']()


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)


@app.get("/sugw/health")
def get_health():
    LOG.info("Health check requested")
    health_report = [
        {'report': report_su.get_health(),
         'explain': explain_su.get_health(),
         'control': control_su.get_health(),
         'teach': teach_su.get_health(),
         'future': future_su.get_health()
         }
    ]
    return jsonify(health_report)


@app.get("/")
def get_root():
    LOG.info("Root call, redirecting...")
    return app.redirect("/sugw/health")


@app.route("/sugw/<external_id>/explain.png")
def get_explanation(external_id):
    LOG.info("Getting an explaining image for the request: " + str(external_id))
    try:
        result = explain_su.get_explanation(external_id)
    except ValueError as e:
        return jsonify(e.args[0])
    return _nocache(_img_response(result))


@app.route("/sugw/<external_id>/teach.png")
def get_teaching_information(external_id):
    LOG.info("Getting a teaching image for the request: " + str(external_id))
    try:
        result = teach_su.get_teaching_information(external_id)
    except ValueError as e:
        return jsonify(e.args[0])
    return _nocache(_img_response(result))


@app.get("/sugw/report")
def get_report():
    LOG.info("Getting statistical information from DB.")
    try:
        result = report_su.get_stat()
    except ValueError as e:
        return jsonify(e.args[0]), 204
    return jsonify(result), 200


@app.put("/sugw/control/<grade_group>")
def control(grade_group):
    LOG.info("Switching the grading behaviour of the system to: " + grade_group)
    result = control_su.update_grade_group(grade_group)
    return jsonify(result), 200


def _img_response(plt_wc):
    """Convert a matplotlib word-cloud into a png image"""
    img_bytes = BytesIO()
    plt_wc.savefig(img_bytes)
    img_bytes.seek(0)
    return send_file(img_bytes, mimetype='image/png')


def _nocache(response):
    """Add Cache-Control headers to disable caching a response"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response


if __name__ == '__main__':
    app.run(host="localhost", port=3033, debug=True)
