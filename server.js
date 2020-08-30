#!/usr/nin/env node

//var express = require("express");
import express from 'express';
import routers from './routers.mjs';
import { URL } from 'url';
import pkg from 'onoff';
import dPkg from 'deferred';
import * as fs from 'fs';
import favicon from 'serve-favicon';
import path from 'path';
import { spawn } from 'child_process';


const adminKeys = { login: "julien", password: "julien" };
var app = express();
app.use(express.json()); // use to parse post json requests
app.use('/api', routers);

//const url = require('url');
const host = new URL('https://***************.fr/');
const { Gpio } = pkg;
//const { deferred } = dPkg;
const __dirname = path.resolve();

var log = [];
var currentPosition = "";
var extend = new Gpio(10, 'out');
var retract = new Gpio(25, 'out');
const parameterFilePath = path.join(__dirname, 'parameters', 'param.json');
var params = JSON.parse(fs.readFileSync(parameterFilePath, { encoding: 'utf8' }));

app.use(express.static('public'));
app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));

fs.readFile(path.join(__dirname, params.PositionFile), 'utf8', (err, data) => {
    currentPosition = data;
});

function requireLogin(req, res, next) {    
    if (Object.keys(req.query).length == 0 && req.query.username == null && req.query.password == null) {        
        res.redirect("/login");
    }

    if (req.query.username === adminKeys.login && req.query.password == adminKeys.password) {
        next();        
    }
    else {
        res.status(401).send();
    }
}


/* ------------ PAGES -----------------*/

app.get("/", (req, res) => {
    res.sendFile(__dirname + "/pages/index.html");
});

app.get("/param", requireLogin, (req, res) => {
    res.sendFile(__dirname + "/pages/admin/param.html");
});

app.get("/menu", (req, res) => {
    res.sendFile(__dirname + "/pages/menu.html");
});

app.get("/login", (req, res) => {
    res.sendFile(__dirname + "/pages/login.html");
});

var server = app.listen(8081, () => {
    var host = server.address().address;
    var port = server.address().port;
    console.log("app listening @ http http://%s:%s", host, port);
});
