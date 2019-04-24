var express = require('express');
const mysql = require('mysql');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

const options = {
  user: 'admin',
  password: 'admin123',
  database: 'pubg_dw'
}

const connection = mysql.createConnection(options)

connection.connect(err => {
  if(err) {
    console.error('Error occured while connecting to DW')
    throw err
  }
})

connection.query('SELECT * FROM death_fact WHERE match_id_key = 1', (error, todos, field) => {
  if(error) {
    console.error('Error occured with query')
    throw err
  }
  console.log(todos[0].kill_count)
})

connection.end()

module.exports = router;
