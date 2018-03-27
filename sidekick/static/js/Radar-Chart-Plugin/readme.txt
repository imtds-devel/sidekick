JQuery Radar Plus By Mehdi TAZI(http://www.tazimehdi.com)
is an improved version of JQueryRadarChart created by Ryan ALLRED

Additional Features:
---------------------

+fixed-max-value 	: 	Charts can take a fixed max value otherwise it will take the max value of chart.

+chartCanvasWrap 	: 	ChartCanvasWrap class allow us to define the order of insertion whittin a div.

+color 			:	Define a specific gradian color for the chart

+additionalLineDistance	:	allow the programmer to choose an additional distance for the labels from the center.

+add annimation delay	:	define the annimation fadding delay.otherwise 1s is the default value


Change:
-------

+Canvas now reside inside a Div

+Chart configuration  can now be define using the metadata attributs(data-[attr]) or using the javascript constructor.

+Chart Title is no more required : if not fill nothing will appear.(allow us to use title using html direcly)

+Size are now dynamic according to div.

+Reponsive chart : the chart can now go throught a div and be responsive.( tested using bootsrap...)

+The lines and labels position are based on max value and on a defined fixed distance(if exist)

+Large labels text are now visible(whittin the chart,if not use additionalLineDistance).

+All the Drawing are now into just 1 canvas , this option allow us to : 
	
	+Download the canvas png
	+Easy to manage nodes and the dom.
	+Less objects into the dom
	+Canvases annimation fadding are now based only on 1 and not many. if more effect needed use specific framework.
	

HOW TO :
--------

1-create a div with a class name "skillsPieChart".

2-put inside a div with a class name "chartCanvasWrap" according to the desired position where to show the chart.

3-Define data for skillsPieChart : either using the metadata attributs ( data-color , data-......) or using JavaScript.
	

Simple Example : See index.html	
--------------------------------

<div class="skillsPieChart" data-values='{"JAVA": 4.5,"C#": 3.0,"PHP":3.0,"HTML5":4.0,"CSS3":4.0}' 
	data-width="200" data-height="200" data-red="0" data-green="128" data-blue="255">
		<h2>MyChart</h2>
		<div class="chartCanvasWrap row"></div>
		<h5>some details .....</h5>
</div>
