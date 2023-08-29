import express from "express";
import { createClient } from "redis";
import { promisify } from 'util';

const app = express();
const port = 1245;

const client = createClient({ url: `redis://127.0.0.1:6379` });
client.on('connect', () => console.log('Redis client connected to the server'));
client.on('error', err => console.log(`Redis client not connected to the server: ${err.message}`));
const getAsync = promisify(client.get).bind(client);


const listProducts = [
  {
    itemId: 1,
    itemName: 'Suitcase 250',
    price: 50,
    stock: 4,
  },
  {
    itemId: 2,
    itemName: 'Suitcase 450',
    price: 100,
    stock: 10
  },
  {
    itemId: 3,
    itemName: 'Suitcase 650',
    price: 350,
    stock: 2
  },
  {
    itemId: 4,
    itemName: 'Suitcase 1050',
    price: 550,
    stock: 5
  },
]

function getItemById(id) {
  return listProducts.filter((item) => id === item.itemId)[0];
}

function reserveStockById(itemId, stock) {
  client.set(itemId, JSON.stringify(stock));
}

async function getCurrentReservedStockById(itemId) {
  return await getAsync(itemId);
}

app.get('/list_products', (req, res) => {
  const products = addInitialAvailableQuantityField(listProducts)
  res.json(products);
});

app.get('/list_products/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const item = await getCurrentReservedStockById(itemId);
  if (item) {
    const product = addCurrentQuantityField([JSON.parse(item)])[0];
    res.json(product);
  } else {
    res.statusCode = 404;
    res.json({ "status": "Product not found" });
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const item = await getCurrentReservedStockById(itemId);
  if (item) {
    const product = JSON.parse(item);
    if (product.stock > 0) {
      reserveStockById(itemId, product);
      res.json({ "status": "Reservation confirmed", "itemId": itemId })
    } else {
      res.json({ "status": "Not enough stock available", "itemId": itemId });
    }
  } else {
    res.statusCode = 404;
    res.json({ "status": "Product not found" });
  }
});

app.listen(port);


//UTILITY FUNCTIONS 
function addInitialAvailableQuantityField(products) {
  return products.map((product) => {
    const newProductObject = product;
    newProductObject.initialAvailableQuantity = newProductObject.stock;
    delete newProductObject.stock;
    return newProductObject;
  });
}

function addCurrentQuantityField(products) {
  return products.map((product) => {
    const newProductObject = product;
    newProductObject.initialAvailableQuantity = newProductObject.stock;
    newProductObject.currentQuantity = newProductObject.initialAvailableQuantity;
    delete newProductObject.stock;
    return newProductObject;
  });
}