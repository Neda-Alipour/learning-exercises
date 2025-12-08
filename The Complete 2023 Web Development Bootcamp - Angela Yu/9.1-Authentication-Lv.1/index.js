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
  database: "secrets",
  password: "Woody25!",
  port: 5432,
});
db.connect();

async function getUserByEmail(email) {
  const result = await db.query("SELECT * FROM users WHERE email = ($1);", [email])
  return result.rows
}

async function addUser(email, password) {
  const result = await db.query("INSERT INTO users (email, password) VALUES ($1, $2) RETURNING id;", 
    [email, password]
  )
  return result.rows[0]
}

app.get("/", (req, res) => {
  res.render("home.ejs");
});

app.get("/login", (req, res) => {
  res.render("login.ejs");
});

app.get("/register", (req, res) => {
  res.render("register.ejs");
});

app.post("/register", async (req, res) => {
  const email = req.body.username
  const password = req.body.password
  const user = await getUserByEmail(email)
  if (user.length > 0){
    console.log("User is already exists.")
  } else {
    const newUserId = await addUser(email, password)
    console.log("User successfully added.")
    return res.render("secrets.ejs");
  }
  res.redirect("/")
});

app.post("/login", async (req, res) => {
  const email = req.body.username
  const password = req.body.password
  const user = await getUserByEmail(email)
  if (user.length > 0){
    if (user[0].password === password){
      console.log("User found.")
      return res.render("secrets.ejs");
    } else {
      console.log("Incorrect password.")
    }
  } else {
    console.log("User not found.")
  }
  return res.redirect("/")
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
