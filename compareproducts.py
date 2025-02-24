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

        .form-container {
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
    </style>
</head>
<body>

    <header>
        <h1>Product Comparison</h1>
    </header>

    <nav id="navigation">
        <div id="menu" onclick="toggleMenu()">
            <div class="bar"></div>
            <div class="bar"></div>
            <div class="bar"></div>
        </div>
        <ul class="nav" id="nav-links">
            <li><a href="#">Home</a></li>
            <li><a href="#">Products</a></li>
            <li><a href="#">Compare</a></li>
            <li><a href="#">Contact</a></li>
        </ul>
    </nav>

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
        function toggleMenu() {
            var navLinks = document.getElementById("nav-links");
            navLinks.classList.toggle("change");
        }

        // Product data
        const products = [
            { name: "Product A", price: "$100", img: "https://via.placeholder.com/150" },
            { name: "Product B", price: "$150", img: "https://via.placeholder.com/150" },
            { name: "Product C", price: "$200", img: "https://via.placeholder.com/150" }
        ];

        // Display products dynamically
        function displayProducts() {
            const productList = document.getElementById("product-list");
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

        // Load products on page load
        window.onload = displayProducts;
    </script>

</body>
</html>
