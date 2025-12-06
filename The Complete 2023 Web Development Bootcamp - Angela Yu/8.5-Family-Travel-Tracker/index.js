import express from "express";
import bodyParser from "body-parser";
import pg from "pg";

const app = express();
const port = 3000;

const db = new pg.Client({
  user: "postgres",
  host: "localhost",
  database: "world",
  password: "Woody25!",
  port: 5432,
});
db.connect();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));

let currentUserId = 1;

let color = "teal";

let user_visited_countries = [];

async function checkVisisted(user_id) {
  const result = await db.query(`SELECT visited_countries.country_code FROM users JOIN visited_countries ON users.id = visited_countries.user_id WHERE users.id = ${user_id}`);
  let countries = [];
  result.rows.forEach((country) => {
    countries.push(country.country_code);
  });
  return countries;
}

async function getAllUsers() {
  const result = await db.query(`SELECT * FROM users`)
  return result.rows
}

async function getUser(user_id) {
  const result = await db.query(`SELECT * FROM users WHERE id = ${user_id}`)
  return result.rows[0]
}

app.get("/", async (req, res) => {
  user_visited_countries = await checkVisisted(currentUserId);

  const users = await getAllUsers();

  const user = await getUser(currentUserId)

  res.render("index.ejs", {
    countries: user_visited_countries,
    total: user_visited_countries.length,
    users: users,
    color: user.color,
  });
});

app.post("/add", async (req, res) => {
  const input = req.body["country"];
  console.log(input);

  try {
    const result = await db.query(
      "SELECT country_code FROM countries WHERE LOWER(country_name) LIKE '%' || $1 || '%';",
      [input.toLowerCase()]
    );

    const data = result.rows[0];
    console.log(data);
    const countryCode = data.country_code;
    try {
      console.log(currentUserId);
      
      await db.query(
        "INSERT INTO visited_countries (country_code, user_id) VALUES ($1, $2)",
        [countryCode, currentUserId]
      );
      res.redirect("/");
    } catch (err) {
      console.log(err);
    }
  } catch (err) {
    console.log(err);
  }
});

app.post("/user", async (req, res) => {
  if (req.body.add === "new") return res.render("new.ejs")
  currentUserId = req.body.user
  res.redirect("/")
});

app.post("/new", async (req, res) => {
  const name = req.body.name
  const color = req.body.color
  const result = await db.query(
    "INSERT INTO users (name, color) VALUES ($1, $2) RETURNING id;",
    [name, color]
  );
  currentUserId = result.rows[0].id
  res.redirect("/")
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
