import requests
from flask import Flask, render_template, request

app = Flask(__name__)

url = "http://20.244.56.144/test/auth"
data ={
"companyName":"Affordmed",
"clientID":"1c4ccddf-f23d-42a3-977e-b515fc9275f8",
"clientSecret":"nloUudGxtSKwYgvw",
"ownerName":"Sai karthik pinisingi",
"ownerEmail":"spinisin@gitam.in",
"rollNo":"VU21CSEN0100398"}

response = requests.post(url,json=data)

response_json = response.json()
ACCESS_TOKEN = response_json.get('access_token')
BASE_URL = "http://20.244.56.144/test/companies/AMZ/categories/{categoryname}/products?top={top}&minPrice=1&maxPrice=10000"

categories = ["Phone", "Computer", "TV", "Earphone", "Tablet", "Charger", "Mouse", "Keypad", "Bluetooth", "Pendrive", "Remote", "Speaker", "Headset", "Laptop", "PC"]

def get_products(category, top):
    url = BASE_URL.format(categoryname=category, top=top)
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    try:
        return response.json()
    except ValueError:
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        category = request.form['category']
        top = int(request.form['top'])
        products = []

        if category in categories:
            try:
                data = get_products(category, top)
                # Assuming the response is a list of products
                if isinstance(data, list):
                    products = data[:top]
            except Exception as e:
                print(f"Error fetching data for {category}: {e}")

        return render_template('results.html', products=products, category=category)

    return render_template('index.html', categories=categories)

if __name__ == "__main__":
    app.run(debug=True)

