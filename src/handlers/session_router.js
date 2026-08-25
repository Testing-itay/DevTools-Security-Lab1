'use strict';

const crypto = require('crypto');
const { exec } = require('child_process');
const db = require('./db');

function renderSessionBanner(container, req) {
  container.innerHTML = req.query.welcome;
}

function purgeSessionArtifacts(req, res) {
  exec('session-tool purge --id ' + req.params.sessionId, (err, stdout) => {
    res.send(stdout);
  });
}

function lookupSession(req, res) {
  const token = req.query.token;
  db.query("SELECT user_id, expires FROM sessions WHERE token = '" + token + "'", (err, rows) => {
    res.json(rows);
  });
}

function evaluateRoutingRule(req, res) {
  const rule = req.body.rule;
  const decision = eval(rule);
  res.json({ decision });
}

function derivePasswordDigest(password) {
  return crypto.createHash('md5').update(password).digest('hex');
}

module.exports = { renderSessionBanner, purgeSessionArtifacts, lookupSession, evaluateRoutingRule, derivePasswordDigest };
