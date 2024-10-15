document.getElementById('product-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('product-name').value;
    const quantity = document.getElementById('product-quantity').value;
    const price = document.getElementById('product-price').value;

    const response = await fetch('/add_product', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, quantity, price }),
    });

    if (response.ok) {
        alert('Product added successfully!');
        fetchProducts();  // Reload product list after adding
    } else {
        alert('Error adding product');
    }
});

// Fetch and display products
async function fetchProducts() {
    const response = await fetch('/products');
    const products = await response.json();

    const productList = document.getElementById('product-list');
    productList.innerHTML = '';  // Clear existing products

    products.forEach(product => {
        const li = document.createElement('li');
        li.textContent = `${product.name} - Quantity: ${product.quantity}, Price: ${product.price}`;
        productList.appendChild(li);
    });
}

// Initial load of products
fetchProducts();
