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
    
            .form-container 
            {
                max-width: 500px;
                margin: 13px auto;
                padding: 20px;
                background-color: #f9f9f9;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            }
    
            .comparison-form label {
                display: block;
                margin-bottom: 8px;
            }
    
            .comparison-form select,
            .comparison-form input[type="number"] {
                width: 100%;
                padding: 8px;
                margin-bottom: 15px;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
            }
    
            .compare-btn {
                background-color: #4caf50;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
    
            .compare-btn:hover {
                background-color: #45a049;
            }
    
            .error-message {
                color: #f44336;
                background-color: #ffebee;
                padding: 10px;
                border-radius: 5px;
                margin: 20px 0;
                border: 1px solid #f44336;
            }
            
            .debug-info {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 15px;
                margin: 20px 0;
                font-family: monospace;
                white-space: pre-wrap;
            }
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
            <li><a href="http://scrapcraftedfinds.infinityfreeapp.com/project.php">Home</a></li>
            <li><a href="http://scrapcraftedfinds.infinityfreeapp.com/services.php">Services</a></li>
            <li><a href="http://scrapcraftedfinds.infinityfreeapp.com/aboutus.php">About Us</a></li>
            <li><a href="http://scrapcraftedfinds.infinityfreeapp.com/contactus.php">Contact Us</a></li>
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
        SELECT p.productname, p.productrating, v.types, v.price, v.color, i.productimage
        FROM _products p
        JOIN _variations v ON p.productid = v.productid
        JOIN _images i ON p.productid = i.imageid
        WHERE p.productcategory = %s AND v.price BETWEEN %s AND %s
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
            <li><a href="http://scrapcraftedfinds.infinityfreeapp.com/project.php">Home</a></li>
            <li><a href="http://scrapcraftedfinds.infinityfreeapp.com/services.php">Services</a></li>
            <li><a href="http://scrapcraftedfinds.infinityfreeapp.com/aboutus.php">About Us</a></li>
            <li><a href="http://scrapcraftedfinds.infinityfreeapp.com/contactus.php">Contact Us</a></li>
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
        js_script = """
        <script>
            function onClickMenu() {
                document.getElementById("menu").classList.toggle("icon");
                document.getElementById("nav").classList.toggle("change");
            }
        </script>
        """
        html_content += productbox
    html_content += '</div>'

    return f"{box_styles} {formatted_results} {html_content} {js_script}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
