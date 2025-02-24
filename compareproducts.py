from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database connection settings
DB_HOST = os.getenv("DB_HOST", "dpg-cuub8ntumphs73c9ig40-a")
DB_NAME = os.getenv("DB_NAME", "compareproducts")
DB_USER = os.getenv("DB_USER", "compareproducts_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "tumI2I6Cdo1r1AbxQzB0ptJBOqqV4abv")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/", methods=["POST"])
def product_comparison():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON body"}), 400
        
        category = data.get("category")
        min_price = data.get("min_price")
        max_price = data.get("max_price")

        if not category or min_price is None or max_price is None:
            return jsonify({"error": "Missing required fields: category, min_price, max_price"}), 400
        
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # SQL Query to fetch products within price range
        sql_query = """
        SELECT product_name, price, brand 
        FROM products 
        WHERE category = %s AND price BETWEEN %s AND %s
        ORDER BY price ASC;
        """
        cursor.execute(sql_query, (category, min_price, max_price))
        products = cursor.fetchall()

        cursor.close()
        conn.close()

        if not products:
            return jsonify({"message": "No products found for the given criteria"}), 404

        # Format response
        result = []
        for product in products:
            result.append({
                "product_name": product[0],
                "price": product[1],
                "brand": product[2]
            })

        return jsonify({"products": result}), 200

    except psycopg2.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
