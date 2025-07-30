from flask import Flask, request, jsonify
from ingredient_parser import parse_ingredient
from fractions import Fraction

app = Flask(__name__)

def convert(obj):
    """
    Recursively convert all Fraction objects to float in any data structure.
    """
    if isinstance(obj, dict):
        return {k: convert(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert(i) for i in obj]
    elif isinstance(obj, Fraction):
        return float(obj)
    else:
        return obj

@app.route('/parse', methods=['POST'])
def parse():
    data = request.json
    ingredient_line = data.get('ingredient')
    if not ingredient_line:
        return jsonify({"error": "No ingredient provided"}), 400
    parsed = parse_ingredient(ingredient_line)
    parsed_dict = vars(parsed)
    clean_dict = convert(parsed_dict)
    return jsonify(clean_dict)
