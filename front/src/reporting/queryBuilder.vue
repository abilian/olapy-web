<template>

    <div class="page-wrapper">
        <div class="row page-titles">
            <div class="col-md-5 align-self-center">
            </div>
            <div class="col-md-7 align-self-center">
                <ol class="breadcrumb">
                </ol>
            </div>

        </div>


        <div class="panel panel-default">
            <div style="padding-left: 25px">
                <div class="row" style="height: 750px">
                    <div id="output" style="display: none;">{{DataFrameCsv}}</div>
                </div>
            </div>
        </div>

    </div>


</template>

<script>
export default {
  props: {
    DataFrameCsv: String,
  },
  mounted() {
    $(function() {
      if (window.location != window.parent.location)
        $("<a>", { target: "_blank", href: "" })
          .text("[Full Screen]")
          .prependTo($("body"));

      jQuery("#output")
        .pivotUI(jQuery.csv.toArrays($("#output").text()), {
          renderers: $.extend(
            jQuery.pivotUtilities.renderers,
            jQuery.pivotUtilities.c3_renderers,
            jQuery.pivotUtilities.d3_renderers,
            jQuery.pivotUtilities.export_renderers
          ),
          hiddenAttributes: [""],
        })
        .show();
    });
  },
};
</script>

<style scoped>
body {
  font-family: Verdana;
}

/*.node {*/
/*border: solid 1px white;*/
/*font: 10px sans-serif;*/
/*line-height: 12px;*/
/*overflow: hidden;*/
/*position: absolute;*/
/*text-indent: 2px;*/
/*}*/

/*.c3-line, .c3-focused {*/
/*stroke-width: 3px !important;*/
/*}*/

/*.c3-bar {*/
/*stroke: white !important;*/
/*stroke-width: 1;*/
/*}*/

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

/*.c3-circle {*/
/*opacity: 1 !important;*/
/*}*/
</style>
