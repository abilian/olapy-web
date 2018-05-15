<template>
    <div class="panel panel-default">
        <div class="panel-heading">
            <i class="fa fa-wrench fa-fw"></i> Query Builder
        </div>
        <div style="padding-left: 15px">
            <div class="row" style="height: 750px">
                <div id="output" style="display: none;"> ,Month,City,Sub_Category,average_sales_M,Average Spent By Person,Year,Quarter,Company,Category,Continent,Country
0,Novemver 2015,Madrid,jackets,110,84,2015,Q4 2015,zara,Clothing/accessories,Europe,Spain
1,Novemver 2014,Madrid,jackets,90,72,2014,Q4 2014,zara,Clothing/accessories,Europe,Spain
2,Novemver 2015,Paris,jackets,300,100,2015,Q4 2015,zara,Clothing/accessories,Europe,France
3,Novemver 2014,Paris,jackets,200,95,2014,Q4 2014,zara,Clothing/accessories,Europe,France
4,Novemver 2015,Paris,Playstation,400,300,2015,Q4 2015,Amazon,Game,Europe,France
5,Novemver 2015,Paris,Playstation,400,300,2015,Q4 2015,Amazon,Game,Europe,France
6,Novemver 2015,Paris,Playstation,400,300,2015,Q4 2015,Amazon,Game,Europe,France
7,Novemver 2015,Paris,Playstation,400,300,2015,Q4 2015,Amazon,Game,Europe,France
8,Novemver 2014,Paris,Playstation,450,200,2014,Q4 2014,Amazon,Game,Europe,France
9,Novemver 2015,Paris,Kids_game,200,100,2015,Q4 2015,Toys R Us,Game,Europe,France
10,Novemver 2014,Paris,Kids_game,240,80,2014,Q4 2014,Toys R Us,Game,Europe,France
11,Novemver 2015,Barcelona,shirts,190,141,2015,Q4 2015,h&m,Clothing/accessories,Europe,Spain
12,Novemver 2014,Barcelona,shirts,140,105,2014,Q4 2014,h&m,Clothing/accessories,Europe,Spain
13,Novemver 2015,Lausanne,Washer,220,231,2015,Q4 2015,Amazon,Household items,Europe,Switzerland
14,Novemver 2015,Lausanne,Washer,90,265,2015,Q4 2015,Amazon,Household items,Europe,Switzerland
15,Novemver 2014,Lausanne,Washer,200,175,2014,Q4 2014,Amazon,Household items,Europe,Switzerland
16,Novemver 2014,Lausanne,Washer,100,245,2014,Q4 2014,Amazon,Household items,Europe,Switzerland
17,Novemver 2015,Lausanne,TV,120,365,2015,Q4 2015,Amazon,Tech/electronics,Europe,Switzerland
18,Novemver 2014,Lausanne,TV,120,235,2014,Q4 2014,Amazon,Tech/electronics,Europe,Switzerland
19,Novemver 2015,New York,TV,512,403,2015,Q4 2015,Amazon,Tech/electronics,America,United States
20,Novemver 2014,New York,TV,500,303,2014,Q4 2014,Amazon,Tech/electronics,America,United States
21,Novemver 2015,New York,Iphone,799,380,2015,Q4 2015,Apple,Tech/electronics,America,United States
22,Novemver 2014,New York,Iphone,509,420,2014,Q4 2014,Apple,Tech/electronics,America,United States
23,Novemver 2015,New York,Kids_game,432,153,2015,Q4 2015,Toys R Us,Game,America,United States
24,Novemver 2014,New York,Kids_game,332,103,2014,Q4 2014,Toys R Us,Game,America,United States
25,Novemver 2015,Zurich,Other,164,500,2015,Q4 2015,Walmart,Other,Europe,Switzerland
26,Novemver 2014,Zurich,Other,130,440,2014,Q4 2014,Walmart,Other,Europe,Switzerland
27,Novemver 2015,Geneva,Fridge,128,230,2015,Q4 2015,Amazon,Household items,Europe,Switzerland
28,Novemver 2014,Geneva,Fridge,111,220,2014,Q4 2014,Amazon,Household items,Europe,Switzerland
29,Novemver 2015,Los Angeles,Playstation,422,250,2015,Q4 2015,Amazon,Game,America,United States
30,Novemver 2014,Los Angeles,Playstation,466,231,2014,Q4 2014,Amazon,Game,America,United States  </div>
            </div>
        </div>
    </div>
</template>

<script>
  export default {
    name: "queryBuilder",
    mounted() {

      $(function () {
        if (window.location != window.parent.location)
          $("<a>", {target: "_blank", href: ""})
            .text("[Full Screen]").prependTo($("body"));

        jQuery("#output").pivotUI(
          jQuery.csv.toArrays($("#output").text()),
          {
            renderers: $.extend(
              jQuery.pivotUtilities.renderers,
              jQuery.pivotUtilities.c3_renderers,
              jQuery.pivotUtilities.d3_renderers,
              jQuery.pivotUtilities.export_renderers
            ),
            hiddenAttributes: [""]
          }
        ).show();
      });


    }
  }
</script>

<style scoped>
    body {
        font-family: Verdana;
    }

    .node {
        border: solid 1px white;
        font: 10px sans-serif;
        line-height: 12px;
        overflow: hidden;
        position: absolute;
        text-indent: 2px;
    }

    .c3-line, .c3-focused {
        stroke-width: 3px !important;
    }

    .c3-bar {
        stroke: white !important;
        stroke-width: 1;
    }

    .c3 text {
        font-size: 12px;
        color: grey;
    }

    .tick line {
        stroke: white;
    }

    .c3-axis path {
        stroke: grey;
    }

    .c3-circle {
        opacity: 1 !important;
    }
</style>