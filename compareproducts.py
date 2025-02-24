import psycopg2
import os
from flask import Flask, request

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")  # Render provides this
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

box_styles = """
<style>
        body
        {
            margin: 0;
            padding: 0;
        }
        
        .results 
        {
            display: flex;
            flex-wrap: wrap; 
            justify-content: space-around; 
            list-style-type: none;
            margin:10px; 
            padding: 0;
        }

        .productbox 
        {
            border: 1px solid #000;
            padding: 10px;
            margin-bottom: 20px;
            width: 250px;
            border-radius: 8px;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
            transition: box-shadow 0.3s ease-in-out;
            box-sizing: border-box;
        }

        .productbox:hover 
        {
            box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.6);
            background-color: rgb(234, 238, 174);
        }

        .productbox img 
        {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
        }

        header {
            background-color: #f55c47;
            color: white;
            text-align: center;
            padding: 20px 0;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.9);
        }
        h1 {
            margin: 0;
        }
        #navigation {
            background-color: #80a3d1;
            padding: 10px;
            overflow: hidden;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.9);
        }
        #menu {
            display: block;
            cursor: pointer;
            float: left;
        }
        .bar {
            width: 25px;
            height: 3px;
            background-color: white;
            margin: 4px 0;
            transition: 0.4s;
        }
        .icon .bar:nth-child(1) {
            transform: rotate(-45deg) translate(-5px, 6px);
        }
        .icon .bar:nth-child(2) {
            opacity: 0;
        }
        .icon .bar:nth-child(3) {
            transform: rotate(45deg) translate(-5px, -6px);
        }
        .nav {
            list-style-type: none;
            margin: 0;
            padding: 0;
            overflow: hidden;
            transition: max-height 0.2s ease-out;
            max-height: 0;
            float: left;
        }
        .nav li {
            float: left;
        }
        .nav li a {
            display: block;
            color: white;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
            transition: background-color 0.3s;
        }
        .nav li a:hover {
            background-color: #0056b3;
        }
        .change {
            max-height: 200px;
        }

        a {
            text-decoration: none; 
            color: inherit; 
        }
        </style>
"""

@app.route('/', methods=['GET', 'POST'])
def product_comparison():
    if request.method == 'POST':
        category = request.form['category']
        min_price = float(request.form['min_price'])
        max_price = float(request.form['max_price'])
        comparison_results = compare_products(category, min_price, max_price)
        return format_results(comparison_results)

    form = """
    <header>
        <center>
            <h1>Product Comparison Page</h1>
        </center>
    </header>
    <center>
     <form action="/" method="POST">
        <label for="category">Category:</label>
        <select id="category" name="category">
            <option value="Table">Table</option>
            <option value="Sofa">Sofa</option>
        </select><br><br>
        
        <label for="min_price">Minimum Price:</label>
        <input type="number" id="min_price" name="min_price"><br><br>
        
        <label for="max_price">Maximum Price:</label>
        <input type="number" id="max_price" name="max_price"><br><br>
        
        <button type="submit">Compare</button>
    </form>
    </center>
    """
    return f"{box_styles} {form}"

def compare_products(category, min_price, max_price):
    sql_query = """
        SELECT p.productName, p.productRating, v.Types, v.Price, v.Color, i.productImage 
        FROM products p 
        JOIN variations v ON p.productId = v.ProductID 
        JOIN images i ON p.productId = i.ImageID 
        WHERE p.productcategory = %s AND v.Price BETWEEN %s AND %s
    """
    cursor.execute(sql_query, (category, min_price, max_price))
    products = cursor.fetchall()

    if not products:
        return []

    comparison_results = []
    for prod in products:
        comparison_results.append({
            "Name": prod[0],
            "Rating": prod[1],
            "Type": prod[2],
            "Price": prod[3],
            "Colour": prod[4],
            "Image": prod[5],
        })

    return comparison_results

def format_results(results):
    if not results:
        return "<h1>No results found.</h1>"

    formatted_results = """
        <header>
            <center>
                <h1>Product Comparison Results</h1>
            </center>
        </header>
    """
    html_content = '<div class="results">'
    for product in results:
        productbox = f"""
        <div class="productbox">
            <img src="{product['Image']}" alt="{product['Name']}">
            <div class="product-details">
                <h2>{product['Name']}</h2>
                <p>Rating: {product['Rating']}</p>
                <p>Type: {product['Type']}</p>
                <p>Price: {product['Price']}</p>
                <p>Colour:{product['Colour']}</p>
            </div>
        </div>
        """
        html_content += productbox
    html_content += '</div>'
    
    return f"{box_styles} {formatted_results} {html_content}"

if __name__ == '__main__':
    app.run(debug=True)
