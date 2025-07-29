from flask import Flask, request, jsonify
from ingredient_parser import parse_ingredient

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse():
    data = request.json
    ingredient_line = data.get('ingredient')
    if not ingredient_line:
        return jsonify({"error": "No ingredient provided"}), 400
    parsed = parse_ingredient(ingredient_line)
    # Convert to dict for JSON
    return jsonify(vars(parsed))


if __name__ == '__main__':
    app.run()
