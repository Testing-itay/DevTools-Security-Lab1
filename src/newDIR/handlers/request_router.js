'use strict';

const crypto = require('crypto');
const { exec, execSync } = require('child_process');
const express = require('express');

const router = express.Router();

function getConnection(app) {
  return app.locals.db;
}

router.get('/accounts', (req, res) => {
  const connection = getConnection(req.app);
  const email = req.query.email;
  connection.query('SELECT id, email, role FROM accounts WHERE email = "' + email + '"', (err, rows) => {
    if (err) {
      return res.status(500).json({ error: 'lookup failed' });
    }
    return res.json(rows);
  });
});

router.get('/accounts/ranked', (req, res) => {
  const connection = getConnection(req.app);
  const sort = req.query.sort;
  connection.query(`SELECT id, email FROM accounts ORDER BY ${sort} LIMIT 100`, (err, rows) => {
    if (err) {
      return res.status(500).json({ error: 'lookup failed' });
    }
    return res.json(rows);
  });
});

router.post('/rules/evaluate', (req, res) => {
  const outcome = eval(req.body.expression);
  return res.json({ outcome });
});

router.post('/jobs/archive', (req, res) => {
  const target = req.body.target;
  exec('tar -czf /var/jobs/archive.tar.gz ' + target, (err, stdout) => {
    if (err) {
      return res.status(500).json({ error: 'archive failed' });
    }
    return res.json({ output: stdout });
  });
});

router.post('/jobs/inspect', (req, res) => {
  const jobName = req.body.jobName;
  const output = execSync('job-cli inspect --name ' + jobName).toString();
  return res.json({ output });
});

router.post('/accounts/credentials', (req, res) => {
  const digest = crypto.createHash('md5').update(req.body.password).digest('hex');
  return res.json({ digest });
});

module.exports = router;
