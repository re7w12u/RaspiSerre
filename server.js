#!/usr/nin/env node

var express = require("express");
var app = express();
app.use(express.json()); // use to parse post json requests

var Gpio = require("onoff").Gpio;
var deferred =  require('deferred');
var fs = require('fs');
var favicon = require('serve-favicon');
var path = require('path');

var log = [];
var currentPosition = "";
var extend = new Gpio(10, 'out');
var retract = new Gpio(25, 'out');

app.use(express.static('public'));
app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));

fs.readFile(__dirname + "/position.txt", 'utf8', (err, data) => {
    currentPosition = data;
});

fs.readFile(__dirname + "/log.txt", 'utf8', (err, data) => {
    log = data.split('\r\n');
});

function GetAM2302Data(){
    var am2302 = {
        'LastMeasureTime':"",
        'temperature':"",
        'humidity':""
    };

    var d = new deferred();
    fs.readFile(__dirname + "/am2302.csv", 'utf8', (err, data) =>{        
        lines = data.split('\r\n').filter((e) => e != '');             
        lastline = lines.slice(-1)[0];        
        measure = lastline.split(',');        
        am2302.LastMeasureTime = measure[0] + " - " + measure[1];
        am2302.temperature = measure[3];
        am2302.humidity = measure[2];        
        d.resolve(am2302);
    });

    return d.promise;
}

app.get("/", (req, res) => {
    res.sendFile(__dirname + "/index.html");
});

app.get("/admin", (req, res) => {
    res.sendFile(__dirname + "/admin/param.html");
});

app.post("/admin/params", (req, res)=>{
    json = JSON.parse(fs.readFileSync(__dirname + "/param.json", {encoding : 'utf8'}));

    json.TemperatureTreshold = req.body.tempTreshold;
    json.Close.duration = req.body.closingTime;
    json.Open.duration = req.body.openingTime;

    fs.writeFileSync(__dirname + '/param.json', JSON.stringify(json), { encoding: "utf8", flag: "w", mode: 0o666 });    
});

app.get("/admin/params", (req,res)=>{        
    if (fs.existsSync(__dirname + "/param.json"))
        res.send(fs.readFileSync(__dirname + "/param.json", {encoding : 'utf8'}));   
    else 
        res.status(503).send("ERROR 500 - Could not load param file");
});

app.get("/log/:lines", (req, res) => {
    var lines = req.params.lines;
    var result = [];
    
    if (lines != undefined) {
        result = log.slice(log.length - lines).reverse();
    } else {
        result = log;
    }

    res.setHeader('Content-Type', 'application/json');
    res.send(JSON.stringify({ log: result }));
});

app.get("/am2302", (req, res) => {
    GetAM2302Data().then((data) =>{
        res.setHeader('Content-Type', 'application/json');        
        res.send(JSON.stringify({ temperature: data.temperature, humidity : data.humidity, time : data.LastMeasureTime }));
    });
    
});

app.get("/position", (req, res) => {    
    res.setHeader('Content-Type', 'application/json');
    res.send(JSON.stringify({ currentPosition: currentPosition }));
});

app.get("/debug/:gpio_id/:duration", (req, res) => {
   var gpio_id = req.params.gpio_id;
    var duration = req.params.duration;
    console.log("coucou");
    if (gpio_id == 10) {         
         extend.writeSync(1);
         setTimeout(() => { extend.writeSync(0); }, duration);
     } else {
         retract.writeSync(1);
         setTimeout(() => { retract.writeSync(0); }, duration);
     }
});

app.get("/move/:action", (req, res) => {
    //var gpio_id = req.params.gpio_id;
    //var duration = req.params.duration;
    var action = req.params.action;
    console.log("gpio 10 status = %s || gpio 25 status = %s", extend.readSync(), retract.readSync());
    //console.log("switching gpio %s for %d milliseconds", gpio_id, duration);
    
    // open gpio port
    //if (gpio_id == 10) {         
    //     extend.writeSync(1);
    //     setTimeout(() => { extend.writeSync(0); }, duration);
    // } else {
    //     retract.writeSync(1);
    //     setTimeout(() => { retract.writeSync(0); }, duration);
    // }

    var spawn = require("child_process").spawn;
    var process = spawn('python3', ['./LAManager.py', action]);
    //process.stdout.on('data', function(data){ res.send(data.toString())});


    // save current position
    //currentPosition = gpio_id == 10 ? 0 : 100;
    //console.log("saving current position : " + currentPosition);
    // fs.writeFile(__dirname + "/position.txt", currentPosition, 'utf8', (err) => {
    //     console.error("something bad just happened while trying to save position in position.txt");
    //     console.error(err);
    // });

    // append to log
    // var today = new Date();
    // fs.appendFile(__dirname + "/log.txt", `${today.toLocaleString('fr-Fr')} -- switching gpio ${gpio_id} for ${duration} milliseconds`)

    res.send("Ok - operation completed");
});

var server = app.listen(8081, () => {
    var host = server.address().address;
    var port = server.address().port;
    console.log("app listening @ http http://%s:%s", host, port);
});
