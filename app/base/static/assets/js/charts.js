/* eslint-disable object-curly-newline */

/* global Chart */

/**
 * --------------------------------------------------------------------------
 * CoreUI Boostrap Admin Template (v3.2.0): main.js
 * Licensed under MIT (https://coreui.io/license)
 * --------------------------------------------------------------------------
 */
window.chartColors = {
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
};

var COLORS = [
  '#4dc9f6',
  '#f67019',
  '#f53794',
  '#537bc4',
  '#acc236',
  '#166a8f',
  '#00a950',
  '#58595b',
  '#8549ba',
  '#b31340'
];

function getLineColor(ctx) {
  return COLORS[ctx.datasetIndex % COLORS.length];
}

var lineOptions = {
  responsive: true,
  legend: {
    position: 'right',
  },
  scales: {
    xAxes: [{
      type: 'linear',
      scaleLabel: {
        display: true,
        labelString: 'Achived Ops/sec'
      }
    }],
    yAxes: [{
      type: 'linear',
      scaleLabel: {
        display: true,
        labelString: 'Avg Latency (ms)'
      },
    }]
  }
};

var lineDataset = [];
$(document).ready(function(){
 $.ajax({
  url: "/nfs3",
  type: "get",
  data: {limit: '10', offset: '0'},
  success: function(response) {
    $.each(response, function(index, value) {
      var dataset = {label: value.legend, 
                     fill: false,
                     backgroundColor: getLineColor,
                     borderColor: getLineColor,
                     showLine: true,
                     data: []
                    };
      value.data.forEach((element, idx) => {
        dataset.data.push({x: value.labels[idx], y: element});
      });
      lineDataset.push(dataset);
    });
    // console.log(lineDataset);
    var lineChart = new Chart(document.getElementById('canvas-1'), {
      type: 'scatter',
      data: {
        datasets: lineDataset,
      },
      options: lineOptions
    }); // eslint-disable-next-line no-unused-vars
  },
 });
});



//# sourceMappingURL=charts.js.map