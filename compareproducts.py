from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """ 
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Product Comparison</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }
            .results {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-around;
                list-style-type: none;
                margin: 10px;
                padding: 0;
            }
            .productbox {
                border: 1px solid #000;
                padding: 10px;
                margin-bottom: 20px;
                width: 250px;
                border-radius: 8px;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
                transition: box-shadow 0.3s ease-in-out;
                box-sizing: border-box;
                text-align: center;
                background-color: white;
            }
            .productbox:hover {
                box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.6);
                background-color: rgb(234, 238, 174);
            }
            .productbox img {
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
            .form-container {
                text-align: center;
                margin: 20px;
            }
            .comparison-form {
                display: inline-block;
                text-align: left;
                background: #f3f3f3;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            select, button {
                display: block;
                margin: 10px 0;
                padding: 10px;
                width: 100%;
            }
            .compare-btn {
                background-color: #28a745;
                color: white;
                border: none;
                cursor: pointer;
                font-size: 16px;
            }
            .compare-btn:hover {
                background-color: #218838;
            }
        </style>
    </head>
    <body>

        <header>
            <h1>Product Comparison</h1>
        </header>

        <div class="form-container">
            <form class="comparison-form">
                <label for="product1">Select Product 1:</label>
                <select id="product1">
                    <option value="Product A">Product A</option>
                    <option value="Product B">Product B</option>
                    <option value="Product C">Product C</option>
                </select>

                <label for="product2">Select Product 2:</label>
                <select id="product2">
                    <option value="Product A">Product A</option>
                    <option value="Product B">Product B</option>
                    <option value="Product C">Product C</option>
                </select>

                <button type="button" class="compare-btn" onclick="compareProducts()">Compare</button>
            </form>
        </div>

        <ul class="results" id="product-list">
            <!-- Products will be added here dynamically -->
        </ul>

        <script>
            // Product data
            const products = [
                { name: "Product A", price: "$100", img: "https://via.placeholder.com/150" },
                { name: "Product B", price: "$150", img: "https://via.placeholder.com/150" },
                { name: "Product C", price: "$200", img: "https://via.placeholder.com/150" }
            ];

            function displayProducts() {
                const productList = document.getElementById("product-list");
                productList.innerHTML = ""; // Clear before adding
                products.forEach(product => {
                    let li = document.createElement("li");
                    li.className = "productbox";
                    li.innerHTML = `
                        <img src="${product.img}" alt="${product.name}">
                        <h3>${product.name}</h3>
                        <p>Price: ${product.price}</p>
                    `;
                    productList.appendChild(li);
                });
            }

            function compareProducts() {
                let product1 = document.getElementById("product1").value;
                let product2 = document.getElementById("product2").value;
                if (product1 === product2) {
                    alert("Please select two different products to compare.");
                } else {
                    alert(`Comparing ${product1} and ${product2}`);
                }
            }

            window.onload = displayProducts;
        </script>

    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
