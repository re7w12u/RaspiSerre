import express from 'express';
import * as fs from 'fs';
import path from 'path';
import Deferred from 'deferred';
import { ChildProcess, spawn } from 'child_process';
import pkg from 'onoff';
const { Gpio } = pkg;

const routers = express.Router();
const __dirname = path.resolve();
var log = [];
const parameterFilePath = path.join(__dirname, 'parameters', 'param.json');
var params = JSON.parse(fs.readFileSync(parameterFilePath, { encoding: 'utf8' }));

function GetAM2302Data() {
    var am2302 = {
        'LastMeasureTime': "",
        'temperature': "",
        'humidity': ""
    };

    var d = Deferred();
    fs.readFile(path.join(__dirname, params.TemperatureDataFile), 'utf8', (err, data) => {
        var lines = data.split('\r\n').filter((e) => e != '');
        var lastline = lines.slice(-1)[0];
        var measure = lastline.split(',');
        am2302.LastMeasureTime = measure[0] + " - " + measure[1];
        am2302.temperature = measure[3];
        am2302.humidity = measure[2];
        d.resolve(am2302);
    });

    return d.promise;
}

// send parameters
routers.get("/params", (req, res) => {
    console.log(parameterFilePath);
    if (fs.existsSync(parameterFilePath))
        res.send(fs.readFileSync(parameterFilePath, { encoding: 'utf8' }));
    else
        res.status(503).send("ERROR 500 - Could not load param file");
});

// save parameters
routers.post("/params", (req, res) => {
    const data = fs.readFileSync(parameterFilePath, { encoding: 'utf8' });
    console.log(data);
    const json = JSON.parse(data);
    console.log(json);
    json.TemperatureTreshold = req.body.tempTreshold;
    json.Close.duration = req.body.closingTime;
    json.Open.duration = req.body.openingTime;

    fs.writeFileSync(parameterFilePath, JSON.stringify(json), { encoding: "utf8", flag: "w", mode: 0o666 });
});

// returns ouput log data
routers.get("/log/:lines", (req, res) => {
    var lines = req.params.lines;
    var result = [];

    log = fs.readFileSync(path.join(__dirname, params.OutputFilePath), { encoding: 'utf8' }).split('\r\n');

    if (lines != undefined) {
        result = log.slice(log.length - lines).reverse();
    } else {
        result = log;
    }

    res.setHeader('Content-Type', 'application/json');
    res.send(JSON.stringify({ log: result }));
});

// return temperature and humidity live data
routers.get("/am2302", (req, res) => {
    GetAM2302Data().then((data) => {
        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify({ temperature: data.temperature, humidity: data.humidity, time: data.LastMeasureTime }));
    });

});

// return number indicating if greenhouse is opened or closed
routers.get("/position", (req, res) => {
    var data = fs.readFileSync(path.join(__dirname, params.PositionFile), { encoding: 'utf8' });
    res.setHeader('Content-Type', 'application/json');
    res.send(JSON.stringify({ currentPosition: data }));
});

// debug to open or close greenhouse door
routers.get("/debug/:gpio_id/:duration", (req, res) => {
    var gpio_id = req.params.gpio_id;
    var duration = req.params.duration;
  
    var g = new Gpio(gpio_id, 'out');
    g.writeSync(1);
    setTimeout(() => { g.writeSync(0); }, duration);

    res.send("GPIO=" + gpio_id + " - Duration=" + duration);
});

routers.get("/move/:action", (req, res) => {
    var action = req.params.action;
    var process = spawn('python3', [params.LAManagerFile, action]);
    res.send("Ok - operation completed");
});

export default routers;