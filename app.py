from flask import Flask, jsonify
import logging
from logging.handlers import RotatingFileHandler
from code_file import generate_analytics_proposals, generate_dashboard_metrics
import config

app = Flask(__name__)

# Configure logging
handler = RotatingFileHandler(
    'logs/app.log', maxBytes=10000, backupCount=3)
error_handler = RotatingFileHandler(
    'logs/error.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
error_handler.setLevel(logging.ERROR)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
error_handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.addHandler(error_handler)
app.logger.setLevel(logging.INFO)

@app.route('/analytics/proposals', methods=['GET'])
def get_analytics_proposals():
    """Endpoint to retrieve analytics proposals"""
    try:
        proposals = generate_analytics_proposals()
        app.logger.info('Successfully generated analytics proposals')
        return jsonify({"analytics_proposals": proposals})
    except Exception as e:
        app.logger.error(f"Error generating proposals: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/dashboard/metrics', methods=['GET'])
def get_dashboard_metrics():
    """Endpoint to retrieve dashboard metrics"""
    try:
        metrics = generate_dashboard_metrics()
        app.logger.info('Successfully generated dashboard metrics')
        return jsonify({"dashboard_metrics": metrics})
    except Exception as e:
        app.logger.error(f"Error generating metrics: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT, debug=config.DEBUG)