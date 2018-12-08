queue()
  .defer(d3.json, "/get_data")
  .await(makeGraphs);
  
function makeGraphs(error, recipeData) {
  
}