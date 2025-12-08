import express from "express";
import bodyParser from "body-parser";
import pg from "pg";
import bcrypt from "bcrypt";

const app = express();
const port = 3000;
const saltRounds = 10;

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
    console.log("User already exists.", user)
    return res.redirect("/")
  } else {
    bcrypt.hash(password, saltRounds, async (err, hash) => {
      if (err) {
        console.error("Error hashing password:", err);
        return res.redirect("/")
      } else {
        const newUserId = await addUser(email, hash)
        console.log("User successfully added.")
        return res.render("secrets.ejs");
      }
    })
  }
});

app.post("/login", async (req, res) => {
  const email = req.body.username
  const enteredPassword = req.body.password
  const user = await getUserByEmail(email)
  const userPassword = user[0].password
  if (user.length > 0){
    bcrypt.compare(enteredPassword, userPassword, (err, result) => {
      if (err) {
          console.error("Error comparing passwords:", err);
        } else {
          if (result) {
            return res.render("secrets.ejs");
          } else {
            return res.send("Incorrect Password");
          }
        }
    })
  } else {
    console.log("User not found.")
    return res.redirect("/")
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
