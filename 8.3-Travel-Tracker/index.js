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

async function showVisitedCountries() {
  const result = await db.query("SELECT country_code FROM visited_countries")

  let visited_countries = []

  result.rows.forEach((item)=>{
    visited_countries.push(item.country_code)
  })

  return visited_countries
} 

app.get("/", async (req, res) => {
  // important async await
  const visited_countries = await showVisitedCountries()
  res.render("index.ejs", { 
    countries: visited_countries, 
    total: visited_countries.length 
  })
});


app.post("/add", async (req, res)=>{
  var country = req.body.country

  // Make sure the country name has first uppercase letter
  country = country.charAt(0).toUpperCase() + country.slice(1)

  const result = await db.query(
    "SELECT country_code FROM countries WHERE country_name = ($1)", 
    [country]
  );

  const country_code = result.rows.length !== 0 ? result.rows[0].country_code : null
  
  if (!country_code) {
    const error = "Country does not exists. Try again."

    const visited_countries = await showVisitedCountries()

    return res.render("index.ejs", { 
      countries: visited_countries, 
      total: visited_countries.length,
      error: error 
    })
  }

  // Check if the country is already in visited_country table
  const visited = await db.query(
    "SELECT country_code FROM visited_countries WHERE country_code = $1", [country_code]
  );

  if (visited.rows.length !== 0) {
    const error = "Country has already been added. Try again."

    const visited_countries = await showVisitedCountries()

    return res.render("index.ejs", { 
      countries: visited_countries, 
      total: visited_countries.length,
      error: error 
    })
  }

  await db.query(
    "INSERT INTO visited_countries (country_code) VALUES ($1)", 
    [country_code]
  );
  res.redirect("/")
})

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
