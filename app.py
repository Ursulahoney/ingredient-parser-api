from flask import Flask, request, jsonify
from ingredient_parser import parse_ingredient
from fractions import Fraction

app = Flask(__name__)

def ingredient_to_json(parsed):
    result = {}
    for k, v in vars(parsed).items():
        # If value is a Fraction (like amount), convert to float
        if isinstance(v, Fraction):
            result[k] = float(v)
        # If value is a list or dict, recursively fix inside
        elif isinstance(v, list):
            result[k] = [float(x) if isinstance(x, Fraction) else x for x in v]
        else:
            result[k] = v
    return result

@app.route('/parse', methods=['POST'])
def parse():
    data = request.json
    ingredient_line = data.get('ingredient')
    if not ingredient_line:
        return jsonify({"error": "No ingredient provided"}), 400
    parsed = parse_ingredient(ingredient_line)
    # Convert to JSON-safe dict
    return jsonify(ingredient_to_json(parsed))

if __name__ == '__main__':
    app.run()

