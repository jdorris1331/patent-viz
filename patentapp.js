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

  connection.query('SELECT count(1) FROM patent_test WHERE ID = ? ', [req.query.patent_num], function(err, rows, fields) {
    if (err) throw err;
    if(rows[0]['count(1)']==1) {
      //connection.query('SELECT inventor FROM patent_info WHERE ID = ? ', [req.query.patent_num], function(err, rows, fields) {
      connection.query('SELECT patent_test.inventor, patent_data_test.abstract, patent_data_test.claims FROM patent_test INNER JOIN patent_data_test ON patent_test.ID=patent_data_test.ID WHERE patent_test.ID=? ', [req.query.patent_num], function(err, rows, fields) {
        if (err) {
          throw err;
        }
        else {
          res.render('show_patent',{ title: req.query.patent_num, author: rows[0].inventor, abstract: rows[0].abstract, claims: rows[0].claims });
        }
      });
    }
    else {
      res.render('patent_search');
    }
  });
});

app.use(express.static('public'));
app.use('/scripts', express.static(__dirname + "/node_modules/vis/dist/"));

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});

