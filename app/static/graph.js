$(document).ready(function() {
	$(chart_id).highcharts({
	legend: {
            itemStyle: {
                color: '#000000',
                fontWeight: 'bold'
                "fontSize": "20px",
            }
        },
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
                       
                        //document.getElementById("myText").value = options.Tweetex;
                        if(options.Tweetex1 != undefined){
                        	document.getElementById("myText1").innerHTML = options.Tweetex1; 
                        }
                        if(options.Tweetex2 != undefined){
                        	document.getElementById("myText2").innerHTML = options.Tweetex2; 
                        }
                        if(options.Tweetex3 != undefined){
                        	document.getElementById("myText3").innerHTML = options.Tweetex3; 
                        }
                        if(options.Tweetex4 != undefined){
                        	document.getElementById("myText4").innerHTML = options.Tweetex4; 
                        }
                    
                        
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