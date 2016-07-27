var express = require('express');
var app = express();

function pad (str, max) {
  str = str.toString();
  return str.length < max ? pad("0" + str, max) : str;
}

/*var edges = [];

function push_edge(val) {
  edges.push(val);
  console.log(edges);
}*/


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
  connection.query('SELECT count(1) FROM patent_info WHERE ID = ? ', [patent_num], function(err_x, rows_x, fields_x) {
    if (err_x) throw err_x;
    if(rows_x[0]['count(1)']==1) {
      connection.query('SELECT patent_info.title, patent_info.inventor, patent_info.ref, patent_info.ref_by, patent_info.topics, patent_data.abstract, patent_data.claims FROM patent_info INNER JOIN patent_data ON patent_info.ID=patent_data.ID WHERE patent_info.ID=? ', [patent_num], function(err_y, rows_y, fields_y) {
        if (err_y) {
          throw err_y;
        }
        else {
          var ref = JSON.parse(rows_y[0].ref);
          var ref_by = JSON.parse(rows_y[0].ref_by);
          
          var topics = JSON.parse(rows_y[0].topics);
          if (topics == null){
            topics = [0];
          }

          var nodes = [];
          nodes.push({id: 1, label: patent_num});
          edges = [];
          for (i = 0; i < ref.length; i++) {
            //console.log(ref[i]);
            nodes.push({id: i+2, label: ref[i], group: 0});
            edges.push({from: i+2, to: 1, arrows: 'from'});
            //console.log(nodes);
          }
          if (ref_by != null) {
          for (i = 0; i < ref_by.length; i++) {
            nodes.push({id: i+ref.length+2, label: ref_by[i], color: 'red', group: 1});
            edges.push({from: i+ref.length+2, to: 1, arrows: 'to'});
          }
          }
        
            
            /*if(/^\d+$/.test(ref[i]) == true ) {
              temp_patent_num = pad(ref[i],8);
              console.log(temp_patent_num);
            connection.query('SELECT count(1) FROM patent_info WHERE ID = ? ', [temp_patent_num], function(err_z, rows_z, fields_z) {
              if (err_z) throw err_z;
              if(rows_z[0]['count(1)']==1) {
                console.log(temp_patent_num);
                connection.query('SELECT topics FROM patent_info WHERE ID=? ', [temp_patent_num], function(err_zz, rows_zz, fields_zz) {
                  if (err_zz) throw err_zz;
                  else {
                    console.log(temp_patent_num);
                    var inner_topics = JSON.parse(rows_zz[0].topics);
                    console.log(inner_topics);
                    if (inner_topics == null){
                      innner_topics = [0];
                      edges.push({from: i+2, to: 1});
                    }
                    else {
                      console.log(topics);
                      var intersection = topics.filter(function(n) {
                        return inner_topics.indexOf(n) != -1;
                      });   
                      var edge_name;
                      if (intersection.length > 0) {
                        edge_name = intersection.join();
                      }
                      else {
                        edge_name = "None";
                      }
                      console.log(edge_name);
                      push_edge({from: i+2, to: 1});//, label: edge_name});
                    }
                  }
                });
              }
              else{
                push_edge({from: i+2, to: 1});
              }
            });
            }
            else{
              push_edge({from: i+2, to: 1});
            }
    
          }  */
      
          res.render('show_patent',{ title: rows_y[0].title, id: patent_num, author: rows_y[0].inventor, abstract: rows_y[0].abstract, claims: rows_y[0].claims, nodes: nodes, edges: edges, topics: topics });
        }
      });
    }
    else {
      res.render('patent_search');
    }
  });
  }
  else { 
    //query for lower case word in patent_index and pass json data to results making links to IDs
    connection.query('SELECT count(1) FROM patent_index WHERE word = ? ', [req.query.patent_num], function(err_x, rows_x, fields_x) {
      if (err_x) throw err_x;
      if(rows_x[0]['count(1)']==1) {
      connection.query('SELECT IDs FROM patent_index WHERE word=? ', [req.query.patent_num], function(err, rows, fields) {
        //need to check if word exists
        if (err) {
          throw err;
        }
        else {
          var IDs = JSON.parse(rows[0].IDs);

          //pass rows instead
          res.render('results', { IDs: IDs  });
        }
      });
      }
      else {
        res.render('patent_search');
      }
    });
  }
});

app.use(express.static('public'));
app.use('/scripts', express.static(__dirname + "/node_modules/vis/dist/"));

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});

