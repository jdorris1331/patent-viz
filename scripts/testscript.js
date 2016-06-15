<script type="text/javascript">
  var nodes = new vis.DataSet([
    {id: 1, label: 'US7322199', title: 'Stirling cooler'},
    {id: 2, label: 'Node 2'},
    {id: 3, label: 'Node 3'},
    {id: 4, label: 'Node 4'},
    {id: 5, label: 'Node 5'} 
  ]);   

  // create an array with edges
  var edges = new vis.DataSet([
    {from: 1, to: 3, title: '1927'},
    {from: 1, to: 2, color:{color:'red'}},
    {from: 2, to: 4, color:'rgb(20,24,200)'},  
    {from: 2, to: 5}
  ]);   

  // create a network
  var container = document.getElementById('mynetwork');
  var data = { 
    nodes: nodes,
    edges: edges
  };    
  var options = {};
  var network = new vis.Network(container, data, options);
</script>
