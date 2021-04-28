const express = require("express");
const bodyParser = require("body-parser");
const path = require("path")
const app = express();

app.set("views",path.join(__dirname,"/views"))
app.set("view engine","ejs")

app.use(express.static("public"))
app.use(express.json())

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

const PORT = process.env.PORT || 3000;

app.use("/api",require("./routes/routes"))

app.listen(PORT,()=>{
    console.log("server is up")

});