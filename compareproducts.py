import psycopg2
import os
from flask import Flask, request

app = Flask(__name__)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")  # Render provides this

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

box_styles = """
<style>
/* Your CSS styles here */
</style>
"""

@app.route('/', methods=['GET', 'POST'])
def product_comparison():
    if request.method == 'POST':
        try:
            category = request.form['category']
            min_price = float(request.form['min_price']) if request.form['min_price'] else 0
            max_price = float(request.form['max_price']) if request.form['max_price'] else 1000
            comparison_results = compare_products(category, min_price, max_price)
            return format_results(comparison_results)
        except Exception as e:
            error_message = f"""
            <div class="error-message">
                <h3>Error</h3>
                <p>{str(e)}</p>
            </div>
            """
            return f"{box_styles} {get_base_page()} {error_message}"

    return f"{box_styles} {get_base_page()}"

def get_base_page():
    """Return the base page HTML with navigation and form"""
    header = """
    <header>
        <center>
            <h1>Product Comparison Page</h1>
        </center>
    </header>
    """
    navigation = """
    <div id="navigation">
        <div id="menu" onclick="onClickMenu()">
            <div id="bar1" class="bar"></div>
            <div id="bar2" class="bar"></div>
            <div id="bar3" class="bar"></div>
        </div>
        <ul class="nav" id="nav">
            <li><a href="/">Home</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#">About Us</a></li>
            <li><a href="#">Contact Us</a></li>
        </ul>
    </div>
    """
    form = """
    <center>
        <div class="form-container">
            <form action="/" method="POST" class="comparison-form">
                <label for="category">Category:</label>
                <select id="category" name="category">
                    <option value="Table">Table</option>
                    <option value="Sofa">Sofa</option>
                </select><br><br>
                <label for="min_price">Minimum Price:</label>
                <input type="number" id="min_price" name="min_price" value="0"><br><br>
                <label for="max_price">Maximum Price:</label>
                <input type="number" id="max_price" name="max_price" value="1000"><br><br>
                <button type="submit" class="compare-btn">Compare</button>
            </form>
        </div>
    </center>
    """
    js_script = """
    <script>
    function onClickMenu() {
        document.getElementById("menu").classList.toggle("icon");
        document.getElementById("nav").classList.toggle("change");
    }
    </script>
    """
    return f"{header} {navigation} {form} {js_script}"

def compare_products(category, min_price, max_price):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql_query = """
        SELECT p."productName", p."productRating", v."Types", v."Price", v."Color", i."productImage"
        FROM "products" p
        JOIN "variations" v ON p."productId" = v."ProductID"
        JOIN "images" i ON p."productId" = i."ImageID"
        WHERE p."productcategory" = %s AND v."Price" BETWEEN %s AND %s
        """
        
        cursor.execute(sql_query, (category, min_price, max_price))
        products = cursor.fetchall()

        comparison_results = []
        for prod in products:
            comparison_results.append({
                "Name": prod[0],
                "Rating": prod[1],
                "Type": prod[2],
                "Price": prod[3],
                "Colour": prod[4],
                "Image": prod[5]
            })

        return comparison_results
    except Exception as e:
        print(f"Database error: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def format_results(results):
    if not results:
        no_results = """
        <div class="error-message">
            <h3>No Results Found</h3>
            <p>No products match your criteria. Please try different filter settings.</p>
            <p>Try checking the <a href="/debug" style="color: blue; text-decoration: underline;">debug page</a> to see what's in your database.</p>
        </div>
        """
        return f"{box_styles} {get_base_page()} {no_results}"

    formatted_results = """
    <header>
        <center>
            <h1>Product Comparison Results</h1>
        </center>
    </header>
    <div id="navigation">
        <div id="menu" onclick="onClickMenu()">
            <div id="bar1" class="bar"></div>
            <div id="bar2" class="bar"></div>
            <div id="bar3" class="bar"></div>
        </div>
        <ul class="nav" id="nav">
            <li><a href="/">Home</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#">About Us</a></li>
            <li><a href="#">Contact Us</a></li>
        </ul>
    </div>
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
                <p>Price: ${product['Price']}</p>
                <p>Colour: {product['Colour']}</p>
            </div>
        </div>
        """
        html_content += productbox
    html_content += '</div>'

    return f"{box_styles} {formatted_results} {html_content}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
