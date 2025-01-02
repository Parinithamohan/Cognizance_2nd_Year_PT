from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Mock database (in-memory storage)
quotes_db = [
    {"id": 1, "quote": "The future belongs to those who believe in the beauty of their dreams.", "category": "Success"},
    {"id": 2, "quote": "Don't watch the clock; do what it does. Keep going.", "category": "Work"}
]

# Endpoint 1: Get All Quotes
@app.route('/quotes', methods=['GET'])
def get_quotes():
    return jsonify(quotes_db), 200

# Endpoint 2: Add a New Quote
@app.route('/quotes', methods=['POST'])
def add_quote():
    data = request.get_json()
    new_quote = {
        "id": len(quotes_db) + 1,
        "quote": data['quote'],
        "category": data['category']
    }
    quotes_db.append(new_quote)
    return jsonify(new_quote), 201

# Endpoint 3: Search Quotes by Keyword
@app.route('/quotes/search', methods=['GET'])
def search_quotes():
    keyword = request.args.get('keyword', '')
    filtered = [q for q in quotes_db if keyword.lower() in q['quote'].lower()]
    if not filtered:
        return jsonify({"error": "No quotes found matching the keyword."}), 404
    return jsonify(filtered), 200

# Endpoint 4: Get Quotes by Category
@app.route('/quotes/category/<string:category>', methods=['GET'])
def get_by_category(category):
    filtered = [q for q in quotes_db if q['category'].lower() == category.lower()]
    if not filtered:
        return jsonify({"error": f"No quotes found in category '{category}'."}), 404
    return jsonify(filtered), 200

# Endpoint 5: Random Quote
@app.route('/quotes/random', methods=['GET'])
def random_quote():
    if not quotes_db:
        return jsonify({"error": "No quotes available."}), 404
    return jsonify(random.choice(quotes_db)), 200

# Endpoint 6: Delete a Quote by ID
@app.route('/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    global quotes_db
    quotes_db = [q for q in quotes_db if q['id'] != quote_id]
    return jsonify({"message": "Quote deleted"}), 200

# Endpoint 7: API Documentation
@app.route('/', methods=['GET'])
def api_documentation():
    return jsonify({
        "endpoints": {
            "GET /quotes": "Fetch all quotes",
            "POST /quotes": "Add a new quote (Requires JSON with 'quote' and 'category')",
            "GET /quotes/search?keyword=<keyword>": "Search quotes by keyword",
            "GET /quotes/category/<category>": "Get quotes by category",
            "GET /quotes/random": "Fetch a random quote",
            "DELETE /quotes/<id>": "Delete a quote by ID"
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
