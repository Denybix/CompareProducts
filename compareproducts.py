import psycopg2
import os
from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")  # Render provides this

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def initialize_database():
    """Create database tables if they don't exist"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                productId SERIAL PRIMARY KEY,
                productName VARCHAR(255) NOT NULL,
                productCategory VARCHAR(255) NOT NULL,
                productRating DECIMAL(3,1) DEFAULT 0
            )
        ''')
        
        # Create variations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS variations (
                VariationID SERIAL PRIMARY KEY,
                ProductID INT REFERENCES products(productId),
                Types VARCHAR(255),
                Price DECIMAL(10,2),
                Color VARCHAR(50)
            )
        ''')
        
        # Create images table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                ImageID INT REFERENCES products(productId),
                productImage VARCHAR(255)
            )
        ''')
        
        # Insert sample data if tables are empty
        cursor.execute("SELECT COUNT(*) FROM products")
        if cursor.fetchone()[0] == 0:
            # Insert sample products
            cursor.execute('''
                INSERT INTO products (productName, productCategory, productRating)
                VALUES 
                ('Modern Dining Table', 'Table', 4.5),
                ('Coffee Table', 'Table', 4.2),
                ('Sectional Sofa', 'Sofa', 4.7),
                ('Convertible Sofa', 'Sofa', 4.0)
            ''')
            
            # Insert variations
            cursor.execute('''
                INSERT INTO variations (ProductID, Types, Price, Color)
                VALUES 
                (1, 'Dining', 499.99, 'Oak'),
                (1, 'Dining', 549.99, 'Walnut'),
                (2, 'Coffee', 199.99, 'Black'),
                (2, 'Coffee', 249.99, 'White'),
                (3, 'L-Shape', 899.99, 'Grey'),
                (3, 'L-Shape', 999.99, 'Blue'),
                (4, 'Sleeper', 699.99, 'Beige'),
                (4, 'Sleeper', 749.99, 'Brown')
            ''')
            
            # Insert images
            cursor.execute('''
                INSERT INTO images (ImageID, productImage)
                VALUES 
                (1, 'https://placehold.co/600x400?text=Dining+Table'),
                (2, 'https://placehold.co/600x400?text=Coffee+Table'),
                (3, 'https://placehold.co/600x400?text=Sectional+Sofa'),
                (4, 'https://placehold.co/600x400?text=Convertible+Sofa')
            ''')
        
        conn.commit()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

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
        
        .success-message {
            color: #4CAF50;
            background-color: #E8F5E9;
            padding: 10px;
            border-radius: 5px;
            margin: 20px 0;
            border: 1px solid #4CAF50;
        }
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
        <ul class="nav" id ="nav">
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

@app.route('/setup-database', methods=['GET'])
def setup_database():
    """Route to initialize database with tables and sample data"""
    try:
        initialize_database()
        success_message = """
        <div class="success-message">
            <h3>Success</h3>
            <p>Database initialized successfully with sample data!</p>
            <p><a href="/" style="color: #4CAF50; text-decoration: underline;">Return to Home</a></p>
        </div>
        """
        return f"{box_styles} {get_base_page()} {success_message}"
    except Exception as e:
        error_message = f"""
        <div class="error-message">
            <h3>Error</h3>
            <p>Could not initialize database: {str(e)}</p>
            <p><a href="/" style="color: #f44336; text-decoration: underline;">Return to Home</a></p>
        </div>
        """
        return f"{box_styles} {get_base_page()} {error_message}"

def compare_products(category, min_price, max_price):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql_query = (
            "SELECT p.productName, p.productRating, v.Types, v.Price, v.Color, i.productImage "
            "FROM products p "
            "JOIN variations v ON p.productId = v.ProductID "
            "JOIN images i ON p.productId = i.ImageID "
            "WHERE p.productcategory = %s AND v.Price BETWEEN %s AND %s"
        )
        cursor.execute(sql_query, (category, min_price, max_price))
        products = cursor.fetchall()

        # Create a list of dictionaries from the tuple results
        comparison_results = []
        for prod in products:
            comparison_results.append({
                "Name": prod[0],  # productName
                "Rating": prod[1], # productRating
                "Type": prod[2],   # Types
                "Price": prod[3],  # Price
                "Colour": prod[4], # Color
                "Image": prod[5]   # productImage
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
                <ul class="nav" id ="nav">
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
    
    js_script = """
    <script>
        function onClickMenu() {
            document.getElementById("menu").classList.toggle("icon");
            document.getElementById("nav").classList.toggle("change");
        }
    </script>
    """
    
    return f"{box_styles} {js_script} {formatted_results} {html_content}"

if __name__ == '__main__':
    # Initialize database on startup
    initialize_database()
    app.run(debug=True, host='0.0.0.0')
