from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

# Load SonarQube connection details from environment variables
SONAR_URL = os.getenv("SONAR_URL", "http://localhost:9000")
SONAR_TOKEN = os.getenv("SONAR_TOKEN", "")

@app.route("/")
def home():
    return {"message": "SonarQube KPI App - Running"}

@app.route("/metrics/<project_key>")
def get_metrics(project_key):
    """Fetch basic metrics from SonarQube for a given project"""
    url = f"{SONAR_URL}/api/measures/component"
    params = {
        "component": project_key,
        "metricKeys": "bugs,vulnerabilities,code_smells,coverage,duplicated_lines_density"
    }
    response = requests.get(url, auth=(SONAR_TOKEN, ""), params=params)

    if response.status_code != 200:
        return {"error": "Failed to fetch metrics", "details": response.text}, 500

    data = response.json()
    metrics = {m["metric"]: m["value"] for m in data["component"]["measures"]}
    return jsonify({"project": project_key, "metrics": metrics})

if __name__ == "__main__":
    app.run(debug=True)
