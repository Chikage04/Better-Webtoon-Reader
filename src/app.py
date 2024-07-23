from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        result = subprocess.run(['python3', './teste.py'], capture_output=True, text=True, check=True)
        return jsonify({'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
