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

db.connect()

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));

app.get("/", async (req, res) => {
  const result = await db.query("SELECT country_code FROM visited_countries")
  let visited_countries = []
  result.rows.forEach((item)=>{
    visited_countries.push(item.country_code)
  })
  res.render("index.ejs", { countries: visited_countries, total: visited_countries.length })
});

app.post("/add", async (req, res)=>{
  let country = req.body.country
  country = country.charAt(0).toUpperCase() + country.slice(1)
  const country_code = await db.query("SELECT country_code FROM countries WHERE country_name=$1", [country])

  if (country_code.rows.length !== 0) {
    const result = await db.query("INSERT INTO visited_countries (country_code) VALUES ($1)", [country_code.rows[0].country_code])
    // console.log(result.rows)
  } else {
    console.log("Not a valid country name.")
  }
  res.redirect("/")

})

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
