import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Endpoint to get the access token
AUTH_URL = "http://20.244.56.144/test/auth"
DATA = {
    "companyName": "Affordmed",
    "clientID": "1c4ccddf-f23d-42a3-977e-b515fc9275f8",
    "clientSecret": "nloUudGxtSKwYgvw",
    "ownerName": "Sai karthik pinisingi",
    "ownerEmail": "spinisin@gitam.in",
    "rollNo": "VU21CSEN0100398"
}

def get_access_token():
    response = requests.post(AUTH_URL, json=DATA)
    response_json = response.json()
    return response_json.get('access_token')

ACCESS_TOKEN = get_access_token()

BASE_URL = "http://20.244.56.144/test/companies/{company}/categories/{category}/products?top={top}&minPrice={minPrice}&maxPrice={maxPrice}"

# Endpoint to get products for a specific company and category
@app.route('/products', methods=['GET'])
def get_products():
    company = request.args.get('company')
    category = request.args.get('category')
    top = request.args.get('top', 10)  # default to 10 if not provided
    min_price = request.args.get('minPrice', 1)
    max_price = request.args.get('maxPrice', 10000)

    url = BASE_URL.format(company=company, category=category, top=top, minPrice=min_price, maxPrice=max_price)
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to retrieve products"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
