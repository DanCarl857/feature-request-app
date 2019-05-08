'use strict';

const express = require('express');
const PORT = process.env.PORT || 8080;
const HOST = process.env.HOST || '0.0.0.0';
const app = express();

app.use(express.static(__dirname + '/dist'));
app.use(express.static(__dirname + '/node_modules'));
app.get('/', (req, res) => {
  res.sendfile(__dirname + '/index.html');
});

app.listen(PORT, HOST, function () {
    console.log(`[SERVER]: Running on http://${HOST}:${PORT}`);
});