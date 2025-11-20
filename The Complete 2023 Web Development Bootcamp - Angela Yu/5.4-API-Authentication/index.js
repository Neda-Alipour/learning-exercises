import express, { json } from "express";
import axios from "axios";

const app = express();
const port = 3000;
const API_URL = "https://secrets-api.appbrewery.com/";

//TODO 1: Fill in your values for the 3 types of auth.
const yourUsername = "Neda";
const yourPassword = "nedaneda12345";
const yourAPIKey = "45f5efe3-cc72-4058-b6f1-1d08135eb168";
const yourBearerToken = "1d81f7d2-e9f6-43da-9078-cd3398752e6c";
var page = 1

app.get("/", (req, res) => {
  res.render("index.ejs", { content: "API Response." });
});

app.get("/noAuth", async (req, res) => {
  //TODO 2: Use axios to hit up the /random endpoint
  //The data you get back should be sent to the ejs file as "content"
  //Hint: make sure you use JSON.stringify to turn the JS object from axios into a string.

  const response = await axios.get(API_URL + "random")
  const result = JSON.stringify(response.data)
  res.render("index.ejs", {
    content: result
  })

});

app.get("/basicAuth", async (req, res) => {
  //TODO 3: Write your code here to hit up the /all endpoint
  //Specify that you only want the secrets from page 2
  //HINT: This is how you can use axios to do basic auth:
  // https://stackoverflow.com/a/74632908

   const response = await axios.get(API_URL + `all?page=2`, {
      auth: {
        username: yourUsername,
        password: yourPassword,
      },
    });
    const result = JSON.stringify(response.data)
    res.render("index.ejs", {
      content: result
    })

});

app.get("/apiKey", async (req, res) => {
  //TODO 4: Write your code here to hit up the /filter endpoint
  //Filter for all secrets with an embarassment score of 5 or greater
  //HINT: You need to provide a query parameter of apiKey in the request.

  const response = await axios.get(API_URL + `filter?score=2&apiKey=${yourAPIKey}`);
  const result = JSON.stringify(response.data)
  res.render("index.ejs", {
    content: result
  })


});

app.get("/bearerToken", async (req, res) => {
  //TODO 5: Write your code here to hit up the /secrets/{id} endpoint
  //and get the secret with id of 42
  //HINT: This is how you can use axios to do bearer token auth:
  // https://stackoverflow.com/a/52645402
  /*
  axios.get(URL, {
    headers: { 
      Authorization: `Bearer <YOUR TOKEN HERE>` 
    },
  });
  */
  const response = await axios.get(API_URL + `secrets/1`, {
    headers: { 
      Authorization: `Bearer ${yourBearerToken}` 
    },
  });
  const result = JSON.stringify(response.data)
  res.render("index.ejs", {
    content: result
  })
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
