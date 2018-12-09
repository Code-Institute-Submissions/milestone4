queue()
  .defer(d3.json, "/get_data")
  .await(makeGraphs);
  
function makeGraphs(error, recipeData) {
  var ndx = crossfilter(recipeData);
  
  show_heat_rating(ndx);
  
  show_main_ingredients(ndx);
  
  show_cook_time(ndx);
  
  dc.renderAll();
  
}


function show_heat_rating(ndx) {
  var dim = ndx.dimension(dc.pluck('heat_rating'));
  var group = dim.group();
  
  dc.barChart("#heat_rating")
      .width(400)
      .height(300)
      .margins({top: 10, right: 50, bottom: 50, left: 50 })
      .dimension(dim)
      .group(group)
      .transitionDuration(500)
      .x(d3.scale.ordinal())
      .xUnits(dc.units.ordinal)
      .elasticY(true)
      .xAxisLabel("Heat Rating")
      .yAxis().ticks(10);
}


function show_main_ingredients(ndx) {
  var dim = ndx.dimension(dc.pluck('main_ingredient'));
  var group = dim.group();
  
  
  dc.pieChart("#main_ingredient")
      .height(330)
      .width(500)
      .radius(250)
      .transitionDuration(800)
      .dimension(dim)
      .group(group)
      .legend(dc.legend());
}



function show_cook_time(ndx) {
  var cook_dimension = ndx.dimension(function (d) {
    if (d.cook_time_hr >= 3)
      return "3hr +";
    else if ( d.cook_time_hr == 0)
      return "0-1hr";
    else if ( d.cook_time_hr == 1)
      return "1-2hr";
    else if ( d.cook_time_hr == 2)
      return "2-3hr";
    
  });
  var group = cook_dimension.group();
  
  console.log(group.all());
  
  dc.barChart("#cook_time")
      .width(500)
      .height(300)
      .margins({top: 10, right: 50, bottom: 50, left: 50 })
      .dimension(cook_dimension)
      .group(group)
      .transitionDuration(500)
      .x(d3.scale.ordinal())
      .xUnits(dc.units.ordinal)
      .elasticY(true)
      .xAxisLabel("Hours To Cook")
      .yAxis().ticks(10);
}