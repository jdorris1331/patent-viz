var express = require('express');
var app = express();

function pad (str, max) {
  str = str.toString();
  return str.length < max ? pad("0" + str, max) : str;
}

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
  patent_num = 0;
  if(/^\d+$/.test(req.query.patent_num) == true ) {
    patent_num = pad(req.query.patent_num,8);
    console.log(patent_num);
  }
  else if(/^[0-9]{8}/.test(req.query.patent_num) == true ) {
    patent_num = req.query.patent_num;
  }
  if( patent_num != 0 ) {
  connection.query('SELECT count(1) FROM patent_info WHERE ID = ? ', [patent_num], function(err, rows, fields) {
    if (err) throw err;
    if(rows[0]['count(1)']==1) {
      //connection.query('SELECT inventor FROM patent_info WHERE ID = ? ', [patent_num], function(err, rows, fields) {
      connection.query('SELECT patent_info.title, patent_info.inventor, patent_info.ref, patent_data.abstract, patent_data.claims FROM patent_info INNER JOIN patent_data ON patent_info.ID=patent_data.ID WHERE patent_info.ID=? ', [patent_num], function(err, rows, fields) {
        if (err) {
          throw err;
        }
        else {
          var ref = JSON.parse(rows[0].ref);
          var nodes = [];
          nodes.push({id: 1, label: patent_num});
          var edges = [];
          for (i = 0; i < ref.length; i++) {
            //console.log(ref[i]);
            nodes.push({id: i+2, label: ref[i]});
            edges.push({from: i+2, to: 1});
          } 
          /*var nodes = [
            {id: 1, label: 'US7322199', title: 'Stirling cooler'},
            {id: 2, label: 'Node 2'},
            {id: 3, label: 'Node 3'},
            {id: 4, label: 'Node 4'},
            {id: 5, label: 'Node 5'} 
          ];   
      
          var edges = [
            {from: 1, to: 3, title: '1927'},
            {from: 1, to: 2, color:{color:'red'}},
            {from: 2, to: 4, color:'rgb(20,24,200)'},  
            {from: 2, to: 5}
          ];*/ 
      //var data_json = JSON.stringify(data);
          res.render('show_patent',{ title: rows[0].title, id: patent_num, author: rows[0].inventor, abstract: rows[0].abstract, claims: rows[0].claims, nodes: nodes, edges: edges });
        }
      });
    }
    else {
      res.render('patent_search');
    }
  });
  }
  else { 
    //match title against ...
    res.render('patent_search');
  }
});

app.use(express.static('public'));
app.use('/scripts', express.static(__dirname + "/node_modules/vis/dist/"));

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});

