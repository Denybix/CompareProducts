import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Database connection setup
def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname="your_db_name",
            user="your_db_user",
            password="your_db_password",
            host="your_db_host",
            port="your_db_port"
        )
        return connection
    except Exception as e:
        print("Database connection error:", e)
        return None

# Establish connection and cursor
connection = get_db_connection()
cursor = connection.cursor() if connection else None

@app.route("/", methods=["POST"])
def product_comparison():
    try:
        data = request.get_json()
        category = data.get("category")
        min_price = data.get("min_price")
        max_price = data.get("max_price")

        if not all([category, min_price, max_price]):
            return jsonify({"error": "Missing required parameters"}), 400

        products = compare_products(category, min_price, max_price)
        return jsonify({"products": products})

    except Exception as e:
        print("Error in request processing:", e)
        return jsonify({"error": "Internal server error"}), 500

def compare_products(category, min_price, max_price):
    print(f"Category: {category}, Min Price: {min_price}, Max Price: {max_price}")  # Debugging

    sql_query = """
        SELECT p.productName, p.productRating, v.Types, v.Price, v.Color, i.productImage
        FROM products p
        JOIN variations v ON p.productId = v.ProductID
        JOIN images i ON p.productId = i.ImageID
        WHERE p.productcategory = %s AND v.Price BETWEEN %s AND %s
    """

    try:
        if connection.closed:
            print("Reconnecting to database...")
            reconnect_db()

        connection.rollback()  # Reset transaction state
        cursor.execute(sql_query, (category, min_price, max_price))
        products = cursor.fetchall()
        print("Query executed successfully. Fetched products:", products)  # Debugging
    except Exception as e:
        print("Database query failed:", e)
        connection.rollback()  # Ensure rollback on failure
        return []

    return products

# Function to reconnect to DB if needed
def reconnect_db():
    global connection, cursor
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
    else:
        print("Failed to reconnect to the database.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
