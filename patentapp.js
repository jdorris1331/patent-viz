var express = require('express');
var app = express();

var mysql      = require('mysql');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'joe',
  password : 'password',
  database : 'patents'
});


connection.connect();


app.set('views', './views');
app.set('view engine', 'pug');

app.get('/', function (req, res) {
  res.render('patent_search');
});

app.get('/search', function (req, res) {

  //connection.connect();
  connection.query('SELECT inventor FROM patent_info WHERE ID = ? ', [req.query.patent_num], function(err, rows, fields) {
    if (err) throw err;
    res.render('show_patent',{ title: req.query.patent_num, author: rows[0].inventor});
  });
  //connection.end();
});

app.use(express.static('public'));
app.use('/scripts', express.static(__dirname + "/node_modules/vis/dist/"));

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});

