from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database connection settings
DB_HOST = os.getenv("DB_HOST", "dpg-cuub8ntumphs73c9ig40-a")
DB_NAME = os.getenv("DB_NAME", "compareproducts")
DB_USER = os.getenv("DB_USER", "compareproducts_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "tumI2I6Cdo1r1AbxQzB0ptJBOqqV4abv")

# Function to establish a database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except psycopg2.Error as e:
        print("Database connection error:", e)
        return None

@app.route("/", methods=["GET", "POST"])
def product_comparison():
    if request.method == "GET":
        return jsonify({"message": "Send a POST request with JSON data to compare products."})

    try:
        # Ensure request has JSON data
        if not request.is_json:
            return jsonify({"error": "Invalid JSON request"}), 400
        
        data = request.get_json()
        category = data.get("category")
        min_price = data.get("min_price")
        max_price = data.get("max_price")

        if not category or min_price is None or max_price is None:
            return jsonify({"error": "Missing required parameters"}), 400

        # Connect to the database
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = conn.cursor()

        # Query to fetch products based on category and price range
        sql_query = """
        SELECT * FROM products 
        WHERE category = %s AND price BETWEEN %s AND %s
        ORDER BY price ASC;
        """

        cursor.execute(sql_query, (category, min_price, max_price))
        products = cursor.fetchall()

        conn.commit()  # Ensure transactions are properly committed

        cursor.close()
        conn.close()

        # Convert data to JSON response
        product_list = []
        for product in products:
            product_list.append({
                "id": product[0],
                "name": product[1],
                "category": product[2],
                "price": product[3]
            })

        return jsonify({"products": product_list})

    except psycopg2.Error as db_error:
        return jsonify({"error": f"Database query error: {str(db_error)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
