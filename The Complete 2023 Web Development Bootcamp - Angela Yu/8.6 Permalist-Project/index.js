import express from "express";
import bodyParser from "body-parser";
import pg from "pg";

const app = express();
const port = 3000;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));

const db = new pg.Client({
  user: "postgres",
  host: "localhost",
  database: "permalist",
  password: "Woody25!",
  port: 5432,
});
db.connect();

let items = [];

async function getAllItems() {
  const result = await db.query("SELECT * FROM items")
  // result.rows.forEach(item => {
  //   items.push(item.text)
  // });
  return result.rows
}

async function addItem(title) {
  const result = await db.query("INSERT INTO items (title) VALUES ($1);", 
    [title]
  )
  console.log(result)
  return result.rows[0]
}

async function updateItem(id, title) {
  const result = await db.query("UPDATE items SET title = ($1) WHERE id = ($2)", 
    [title, id]
  )
  return result.rows
}

async function deleteItem(id) {
  const result = await db.query("DELETE FROM items WHERE id = ($1)", 
    [id]
  )
  return result.rows
}

app.get("/", async (req, res) => {
  const items = await getAllItems()
  console.log(items);
  
  res.render("index.ejs", {
    listTitle: "Today",
    listItems: items,
  });
});

app.post("/add", async (req, res) => {
  const title = req.body.newItem;
  // items.push({ title: item });
  const new_item = await addItem(title)
  items = getAllItems()
  res.redirect("/");
});

app.post("/edit", async (req, res) => {
  const item_id = req.body.updatedItemId;
  const title = req.body.updatedItemTitle;
  const result = await updateItem(item_id, title)
  items = getAllItems()
  res.redirect("/");
});

app.post("/delete", async (req, res) => {
  const item_id = req.body.deleteItemId;
  const result = await deleteItem(item_id)
  items = getAllItems()
  res.redirect("/");
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
