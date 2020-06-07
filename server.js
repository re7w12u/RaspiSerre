#!/usr/nin/env node

var express = require("express");
var app = express();

var fs = require('fs');
var currentPosition = "";
fs.readFile(__dirname + "/position.txt", 'utf8', (err, data) => {
    currentPosition = data;
});

var log = [];
fs.readFile(__dirname + "/log.txt", 'utf8', (err, data) => {
    log = data.split('\n');
});

var Gpio = require("onoff").Gpio;
var extend = new Gpio(10, 'out');
var retract = new Gpio(25, 'out');

app.use(express.static('public'));

app.get("/", (req, res) => {
    res.sendFile(__dirname + "/index.html");
});

app.get("/log/:lines", (req, res) => {
    var lines = req.params.lines;
    var result = [];
    if (lines != undefined) {
        result = log.slice(log.length - lines);
    } else {
        result = log;
    }

    res.setHeader('Content-Type', 'application/json');
    res.send(JSON.stringify({ log: result }));
});

app.get("/position", (req, res) => {
    console.log("current position = " + currentPosition);
    res.setHeader('Content-Type', 'application/json');
    res.send(JSON.stringify({ currentPosition: currentPosition }));
});

app.get("/move/:gpio_id/:duration", (req, res) => {

    var gpio_id = req.params.gpio_id;
    var duration = req.params.duration;
    console.log("gpio 10 status = %s || gpio 25 status = %s", extend.readSync(), retract.readSync());
    console.log("switching gpio %s for %d milliseconds", gpio_id, duration);

    // open gpio port
    if (gpio_id == 10) {
        extend.writeSync(1);
        setTimeout(() => { extend.writeSync(0); }, duration);
    } else {
        retract.writeSync(1);
        setTimeout(() => { retract.writeSync(0); }, duration);
    }

    // save current position
    currentPosition = gpio_id == 10 ? 0 : 100;
    console.log("saving current position : " + currentPosition);
    fs.writeFile(__dirname + "/position.txt", currentPosition, 'utf8', (err) => {
        console.error("something bad just happened while trying to save position in position.txt");
        console.error(err);
    });

    // append to log
    var today = new Date();
    fs.appendFile(__dirname + "/log.txt", `${today.toLocaleString('fr-Fr')} -- switching gpio ${gpio_id} for ${duration} milliseconds`)

    res.send("Ok - operation completed");
});

var server = app.listen(8081, () => {
    var host = server.address().address;
    var port = server.address().port;
    console.log("app listening @ http http://%s:%s", host, port);
});
