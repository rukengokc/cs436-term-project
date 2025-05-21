// index.js
const functions = require('@google-cloud/functions-framework');
const admin     = require('firebase-admin');
const axios     = require('axios');

admin.initializeApp();

// Register an HTTP function called "onCreateTodo"
functions.http('onCreateTodo', async (req, res) => {
  try {
    const { id, task, done } = req.body || {};
    console.log('New TODO created:', id, task, done);

    // If you need to call an external webhook:
    // await axios.post(YOUR_WEBHOOK_URL, { text: `New todo: ${task}` });

    res.status(200).json({ ok: true, message: 'Function executed.' });
  } catch (e) {
    console.error(e);
    res.status(500).json({ ok: false, error: e.message });
  }
});

