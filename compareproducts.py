import os
import psycopg2
import traceback
from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to get a new database connection
def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def compare_products(category, min_price, max_price):
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
        
        cursor.close()
        conn.close()

        # Construct result as a list of dictionaries
        comparison_results = [
            {
                "Name": prod[0],    # productName
                "Rating": prod[1],  # productRating
                "Type": prod[2],    # Types
                "Price": prod[3],   # Price
                "Colour": prod[4],  # Color
                "Image": prod[5],   # productImage
            }
            for prod in products
        ]
        
        return comparison_results
    
    except Exception as e:
        print("Error occurred:", str(e))
        traceback.print_exc()
        return []

@app.route("/compare", methods=["POST"])
def compare():
    data = request.json
    category = data.get("category")
    min_price = data.get("min_price")
    max_price = data.get("max_price")
    
    if not category or min_price is None or max_price is None:
        return jsonify({"error": "Missing required parameters"}), 400
    
    try:
        result = compare_products(category, min_price, max_price)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
