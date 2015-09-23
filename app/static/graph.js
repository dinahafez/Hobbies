$(document).ready(function() {
	$(chart_id).highcharts({
		chart: chart,
		title: title,
		xAxis: xAxis,
		yAxis: yAxis,
		series: series,
 tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage}%</b>',
        percentageDecimals: 0
        },	
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            point: {
                events: {
                    click: function(event) {
                        var options = this.options;
                       
                        document.getElementById("myText").value = options.Tweetex;
                    }
                }
            },
            showInLegend: true,
            dataLabels: {
                enabled: true,
                color: '#000000',
                connectorColor: '#000000',

                formatter: function() {
                    return '<b>' + this.point.name + '</b>: ' + Math.round(this.percentage) + '%';
                }

            }
        }
    }
    
    }       
    );
});