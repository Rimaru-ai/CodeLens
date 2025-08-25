from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Load SonarQube connection details from environment variables
SONAR_URL = os.getenv("SONAR_URL", "http://localhost:9000")
SONAR_TOKEN = os.getenv("SONAR_TOKEN", "")

def calculate_code_health(metrics):
    """Simple weighted KPI (0-100)"""
    bugs = int(metrics.get("bugs", 0))
    smells = int(metrics.get("code_smells", 0))
    coverage = float(metrics.get("coverage", 0))
    duplication = float(metrics.get("duplicated_lines_density", 0))

    score = 100
    score -= bugs * 2                # bugs hurt a lot
    score -= smells * 0.5            # smells have moderate impact
    score -= duplication             # duplication % reduces score
    score += coverage * 0.5          # coverage boosts score

    return max(0, min(score, 100))   # keep in 0-100 range

def generate_insights(metrics):
    """Generate human-readable improvement suggestions"""
    insights = []

    coverage = float(metrics.get("coverage", 0))
    bugs = int(metrics.get("bugs", 0))
    smells = int(metrics.get("code_smells", 0))
    duplication = float(metrics.get("duplicated_lines_density", 0))

    if coverage < 50:
        insights.append("Test coverage is low (<50%). Increase unit tests to reduce regression risk.")
    if bugs > 10:
        insights.append("High number of bugs detected. Prioritize fixing critical issues.")
    if smells > 50:
        insights.append("Code smells are high. Consider refactoring to improve maintainability.")
    if duplication > 10:
        insights.append("Code duplication exceeds 10%. Refactor common patterns into reusable functions.")

    if not insights:
        insights.append("Code quality looks good overall. Keep it up!")

    return insights

@app.route("/")
def home():
    return {"message": "SonarQube KPI App - Running"}

@app.route("/metrics/<project_key>")
def get_metrics(project_key):
    """Fetch metrics, compute KPI and insights"""
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

    # KPI + insights
    health_score = calculate_code_health(metrics)
    insights = generate_insights(metrics)

    return jsonify({
        "project": project_key,
        "metrics": metrics,
        "kpi": {"code_health": health_score},
        "insights": insights
    })

if __name__ == "__main__":
    app.run(debug=True)
