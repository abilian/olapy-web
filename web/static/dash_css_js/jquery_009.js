/**
* Theme: Adminox Dashboard
* Author: Coderthemes
* Dashboard 2
*/


$(document).ready(function(){var e=function(){$("#dashboard-1").sparkline([20,40,30,10],{type:"pie",width:"80",height:"80",sliceColors:["#60befc","#6248ff","#e3b0db","#dbdbdb"]}),$("#dashboard-2").sparkline([25,35,21],{type:"pie",width:"80",height:"80",sliceColors:["#6ad9c3","#9aa1f2","#ebeff2"]}),$("#dashboard-3").sparkline([20,40,30],{type:"pie",width:"80",height:"80",sliceColors:["#c086f3","#65acff","#7ed321"]})}
e()
var i
$(window).resize(function(a){clearTimeout(i),i=setTimeout(function(){e()},300)})}),!function(e){"use strict"
var i=function(){}
i.prototype.createStackedChart=function(e,i,a,r,t,o){Morris.Bar({element:e,data:i,xkey:a,ykeys:r,stacked:!0,labels:t,hideHover:"auto",resize:!0,gridLineColor:"#eeeeee",barColors:o,barSizeRatio:.5})},i.prototype.createLineChart=function(e,i,a,r,t,o,s,c,n){Morris.Line({element:e,data:i,xkey:a,ykeys:r,labels:t,fillOpacity:o,pointFillColors:s,pointStrokeColors:c,behaveLikeLine:!0,gridLineColor:"#eef0f2",hideHover:"auto",lineWidth:"3px",pointSize:0,preUnits:"$",resize:!0,lineColors:n})},i.prototype.init=function(){var e=[{y:"2005",a:45,b:180,c:100},{y:"2006",a:75,b:65,c:80},{y:"2007",a:100,b:90,c:56},{y:"2008",a:75,b:65,c:89},{y:"2009",a:100,b:90,c:120},{y:"2010",a:75,b:65,c:110},{y:"2011",a:50,b:40,c:85},{y:"2012",a:75,b:65,c:52},{y:"2013",a:50,b:40,c:77},{y:"2014",a:75,b:65,c:90},{y:"2015",a:100,b:90,c:130},{y:"2016",a:80,b:65,c:95}]
this.createStackedChart("morris-bar-stacked",e,"y",["a","b","c"],["Series A","Series B","Series C"],["#6ad9c3","#9aa1f2","#ebeff2"])
var i=[{y:"2008",a:50,b:0},{y:"2009",a:75,b:50},{y:"2010",a:30,b:80},{y:"2011",a:50,b:50},{y:"2012",a:75,b:10},{y:"2013",a:50,b:40},{y:"2014",a:75,b:50},{y:"2015",a:100,b:70}]
this.createLineChart("morris-line-example",i,"y",["a","b"],["Series A","Series B"],["0.1"],["#ffffff"],["#999999"],["#5553ce ","#f06292"])},e.MorrisCharts=new i,e.MorrisCharts.Constructor=i}(window.jQuery),function(e){"use strict"
e.MorrisCharts.init()}(window.jQuery)
