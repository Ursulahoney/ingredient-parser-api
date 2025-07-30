from flask import Flask, request, jsonify
from ingredient_parser import parse_ingredient
from fractions import Fraction

app = Flask(__name__)

def clean_for_json(obj):
    """
    Recursively convert all Fractions in any nested structure to float.
    Also calls vars() if needed on objects.
    """
    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(i) for i in obj]
    elif isinstance(obj, Fraction):
        return float(obj)
    elif hasattr(obj, "__dict__"):
        return clean_for_json(vars(obj))
    else:
        return obj

@app.route('/parse', methods=['POST'])
def parse():
    data = request.json
    ingredient_line = data.get('ingredient')
    if not ingredient_line:
        return jsonify({"error": "No ingredient provided"}), 400
    parsed = parse_ingredient(ingredient_line)
    result = clean_for_json(parsed)
    return jsonify(result)

if __name__ == "__main__":
    app.run()
