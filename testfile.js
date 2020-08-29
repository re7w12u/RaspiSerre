#!/usr/nin/env node

var express = require("express");
var app = express();
app.use(express.json()); // use to parse post json requests

var fs = require('fs');
var path = require('path');

app.use(express.static('public'));


console.log(path.join(__dirname, '/output/output.txt'));
var result = fs.readFileSync(path.join(__dirname, '/output/output.txt'), {encoding : 'utf8'}); 
var result = result.split('\r\n');
console.log(result);

result = result.slice(result.length - 5).reverse();
console.log(result);


app.get("/", (req, res) => {
    res.sendFile(__dirname + "/pages/index.html");
});

var server = app.listen(8081, () => {
    var host = server.address().address;
    var port = server.address().port;
    console.log("app listening @ http http://%s:%s", host, port);
});
