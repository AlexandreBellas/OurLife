// Plot do gráfico de pizza no d3.js

function pieGraphics(name){
  var svg_pie = d3.select(name),
      pie_width = +svg_pie.attr("width"),
      pie_height = +svg_pie.attr("height"),
      radius = Math.min(pie_width, pie_height) / 2,
      g = svg_pie.append("g").attr("transform", "translate(" + pie_width / 2 + "," + pie_height / 2 + ")");

  var color = d3.scaleOrdinal([
    "hsl(0, 50%, 10%)", 
    "hsl(0, 50%, 20%)", 
    "hsl(0, 50%, 30%)", 
    "hsl(0, 50%, 50%)", 
    "hsl(0, 50%, 70%)", 
    "hsl(0, 50%, 80%)", 
    "hsl(0, 50%, 90%)"
  ]);

  var pie = d3.pie()
      .sort(null)
      .value(function(d) { return d.population; });

  var path = d3.arc()
      .outerRadius(radius - 10)
      .innerRadius(0);

  var label = d3.arc()
      .outerRadius(radius - 40)
      .innerRadius(radius - 40);

  d3.csv("../data/pieData.csv", function(d) {
    d.population = +d.population;
    return d;
  }, function(error, data) {
    if (error) throw error;

    var arc = g.selectAll(".arc")
      .data(pie(data))
      .enter().append("g")
        .attr("class", "arc");

    arc.append("path")
        .attr("d", path)
        .attr("fill", function(d) { return color(d.data.age); });

    arc.append("text")
        .attr("transform", function(d) { return "translate(" + label.centroid(d) + ")"; })
        .attr("dy", "0.35em")
        .text(function(d) { return d.data.age; });
  });
}