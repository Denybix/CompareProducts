import psycopg2
import os
import traceback
from flask import Flask, request

app = Flask(__name__)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# HTML & CSS styles (unchanged from your code)
box_styles = """
<style>
    body { margin: 0; padding: 0; }
    .results { display: flex; flex-wrap: wrap; justify-content: space-around; list-style-type: none; margin:10px; padding: 0; }
    .productbox { border: 1px solid #000; padding: 10px; margin-bottom: 20px; width: 250px; border-radius: 8px; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2); transition: box-shadow 0.3s ease-in-out; box-sizing: border-box; }
    .productbox:hover { box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.6); background-color: rgb(234, 238, 174); }
    .productbox img { max-width: 100%; height: auto; border-radius: 5px; }
    .form-container { max-width: 500px; margin: 13px auto; padding: 20px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); }
    .compare-btn { background-color: #4caf50; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; }
    .compare-btn:hover { background-color: #45a049; }
</style>
"""

@app.route('/', methods=['GET', 'POST'])
def product_comparison():
    if request.method == 'POST':
        try:
            category = request.form['category']
            min_price = float(request.form['min_price'])
            max_price = float(request.form['max_price'])
            comparison_results = compare_products(category, min_price, max_price)
            return format_results(comparison_results)
        except Exception as e:
            print("Error:", e)
            traceback.print_exc()
            return "<h1>Internal Server Error</h1>", 500
    
    form = """
    <header><center><h1>Product Comparison Page</h1></center></header>
    <center>
    <div class="form-container">
        <form action="/" method="POST">
            <label for="category">Category:</label>
            <select id="category" name="category">
                <option value="Table">Table</option>
                <option value="Sofa">Sofa</option>
            </select><br><br>
            <label for="min_price">Minimum Price:</label>
            <input type="number" id="min_price" name="min_price" required><br><br>
            <label for="max_price">Maximum Price:</label>
            <input type="number" id="max_price" name="max_price" required><br><br>
            <button type="submit" class="compare-btn">Compare</button>
        </form>
    </div>
    </center>
    """
    return f"{box_styles} {form}"

def compare_products(category, min_price, max_price):
    try:
        cursor.execute(
            """
            SELECT p.productName, p.productRating, v.Types, v.Price, v.Color, i.productImage 
            FROM products p 
            JOIN variations v ON p.productId = v.ProductID 
            JOIN images i ON p.productId = i.ImageID 
            WHERE p.productcategory = %s AND v.Price BETWEEN %s AND %s
            """,
            (category, min_price, max_price)
        )
        products = cursor.fetchall()

        return [
            {"Name": prod[0], "Rating": prod[1], "Type": prod[2], "Price": prod[3], "Color": prod[4], "Image": prod[5]}
            for prod in products
        ]
    except Exception as e:
        print("Database error:", e)
        traceback.print_exc()
        return []

def format_results(results):
    if not results:
        return "<h1>No results found.</h1>"

    formatted_results = """
        <header><center><h1>Product Comparison Results</h1></center></header>
        <div class="results">
    """
    for product in results:
        formatted_results += f"""
        <div class="productbox">
            <img src="{product['Image']}" alt="{product['Name']}">
            <div class="product-details">
                <h2>{product['Name']}</h2>
                <p>Rating: {product['Rating']}</p>
                <p>Type: {product['Type']}</p>
                <p>Price: {product['Price']}</p>
                <p>Color: {product['Color']}</p>
            </div>
        </div>
        """
    formatted_results += "</div>"
    return f"{box_styles} {formatted_results}"

if __name__ == '__main__':
    app.run(debug=True)
