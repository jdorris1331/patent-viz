  var data = JSON.parse(data_json);
  var container = document.getElementById('mynetwork');
  var options = {};
  var network = new vis.Network(container, data, options);
