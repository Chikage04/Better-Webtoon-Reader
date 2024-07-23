from flask import Flask, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # Permet toutes les origines

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        result = subprocess.run(['python3', './imgur.py'], capture_output=True, text=True, check=True)
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            'error': str(e),
            'stderr': e.stderr,
            'stdout': e.stdout
        }), 500

if __name__ == '__main__':
    # Le serveur WSGI prendra en charge l'exécution en production
    app.run()
