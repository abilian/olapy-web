<template>

    <div class="page-wrapper">
        <div id="pivotOptions" class="row page-titles">
            <div class="col-md-5 align-self-center">
            </div>
            <div class="col-md-7 align-self-center">
                <ol class="breadcrumb">
                </ol>
            </div>

        </div>


        <div class="panel panel-default">

            <div style="padding-left: 25px">
                <div class="row" style="margin-right: 25px">
                    <div id="output" style="overflow: auto; display: none;">{{DataFrameCsv}}</div>
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
    // RENDER PLOTLY CHARTS
    // $(function(){
    //
    //     var renderers = $.extend(jQuery.pivotUtilities.renderers,
    //         jQuery.pivotUtilities.plotly_renderers);
    //
    //         jQuery("#output").pivotUI(jQuery.csv.toArrays($("#output").text()), {
    //             renderers: renderers,
    //             hiddenAttributes: [""],
    //         })
    //           .show();
    //  });

    $(function() {
      if (window.location != window.parent.location)
        $("<a>", { target: "_blank", href: "" })
          .text("[Full Screen]")
          //   add this when using vue-router
          .prependTo($("#pivotOptions"));
      // .prependTo($("body"));

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

</style>
