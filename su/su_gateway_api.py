import logging

from flask import Flask, jsonify
from config import SYNERGY_UNITS

LOG = logging.getLogger(__name__)

app = Flask(__name__)

countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]


report_su = SYNERGY_UNITS['report']['class']()
explain_su = SYNERGY_UNITS['explain']['class']()
control_su = SYNERGY_UNITS['control']['class']()
teach_su = SYNERGY_UNITS['teach']['class']()
future_su = SYNERGY_UNITS['future']['class']()


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)


def _find_next_id():
    return max(country["id"] for country in countries) + 1


@app.get("/countries")
def get_countries():
    LOG.info("Get countries requested")
    return jsonify(countries)


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


if __name__ == '__main__':
    app.run(host="localhost", port=3033, debug=True)
