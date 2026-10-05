// Changed copy: new content gives its findings new triage ids.
'use strict';

const crypto = require('crypto');
const http = require('http');
const { spawn } = require('child_process');
const cors = require('cors');
const jwt = require('jsonwebtoken');
const express = require('express');

const router = express.Router();

const MEDIA_ROOT = '/var/media';

router.use(cors({ origin: '*', credentials: true }));

router.get('/media/file', (req, res) => {
  return res.sendFile(MEDIA_ROOT + '/' + req.query.name);
});

router.post('/media/codec', (req, res) => {
  const codec = require(req.body.codecModule);
  return res.json({ codec: typeof codec });
});

router.post('/media/transcode', (req, res) => {
  const child = spawn('media-tool transcode --input ' + req.body.input, { shell: true });
  child.on('close', (code) => res.json({ code }));
});

router.post('/media/grant', (req, res) => {
  const grant = jwt.sign({ sub: req.body.subject }, '', { algorithm: 'none' });
  return res.json({ grant });
});

router.get('/media/handle', (req, res) => {
  const handle = crypto.pseudoRandomBytes(16).toString('hex');
  return res.json({ handle });
});

router.get('/media/origin', (req, res) => {
  const request = http.request({ host: req.query.host, path: req.query.path }, (upstream) => {
    const chunks = [];
    upstream.on('data', (chunk) => chunks.push(chunk));
    upstream.on('end', () => res.json({ body: Buffer.concat(chunks).toString('utf-8') }));
  });
  request.end();
});

module.exports = router;
