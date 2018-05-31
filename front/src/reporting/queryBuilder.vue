<template>

    <div class="page-wrapper">
        <div id="pivotOptions" class="row page-titles">
            <div class="col-md-5 align-self-center">
                <select id="cube_selector" class="form-control" v-model="selectedCube">
                    <option disabled value="">Cube</option>
                    <option v-for="cube in userCubes">
                        {{ cube }}
                    </option>
                </select>
            </div>
            <div v-if="selectedCube" class="col-md-7 align-self-center">
                <ol class="breadcrumb">
                    <label>
                        <input type="text" v-model="pivottableName" class="form-control input-rounded"
                               placeholder="Pivottable Title">
                    </label>

                    <button type="button" class="btn btn-success m-b-10 m-l-5" @click="savePivottable">Save</button>
                </ol>
            </div>


        </div>


        <div class="panel panel-default">

            <div style="padding-left: 25px">
                <div class="row" style="margin-right: 25px">
                    <div id="output" style="overflow: auto; display: none;">{{df}}</div>
                </div>
            </div>
        </div>

    </div>


</template>

<script>
export default {
  props: {
    DataFrameCsv: String,
    selectedPivotTable: Object,
  },
  data: function() {
    return {
      pivottableName: null,
      selectedCube: "",
      userCubes: [],
      df: this.DataFrameCsv,
    };
  },
  computed: {
    rows() {
      if (this.selectedPivotTable) {
        return this.selectedPivotTable.rows;
      } else {
        return [];
      }
    },
    columns() {
      if (this.selectedPivotTable) {
        return this.selectedPivotTable.columns;
      } else {
        return [];
      }
    },
  },
  methods: {
    getUserCubes() {
      let userCubes = [];
      this.$http
        .get("api/cubes")
        .then(response => {
          return response.json();
        })
        .then(data => {
          for (let key in data) {
            userCubes.push(data[key]);
          }
        });
      return userCubes;
    },
    render_pivottable() {
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

      // $(function() {
      //   if (window.location != window.parent.location)
      //     $("<a>", { target: "_blank", href: "" })
      //       .text("[Full Screen]")
      //       //   add this when using vue-router
      //       .prependTo($("#pivotOptions"));
      // .prependTo($("body"));

      jQuery("#output")
        .pivotUI(jQuery.csv.toArrays(this.df), {
          renderers: $.extend(
            jQuery.pivotUtilities.renderers,
            jQuery.pivotUtilities.c3_renderers,
            jQuery.pivotUtilities.d3_renderers,
            jQuery.pivotUtilities.export_renderers
          ),
          hiddenAttributes: [""],
          cols: this.columns,
          rows: this.rows,
          // vals: ["montant"],
          // aggregatorName: "Sum",
          // rendererName: "Heatmap",
        })
        .show();
    },
    getPivottableContent() {
      let pvtDivs = {
        pvtRows: null,
        pvtCols: null,
      };
      for (let pvtDiv in pvtDivs) {
        let divContent = [];
        let div = document.getElementsByClassName(pvtDiv);
        for (let i = 0; i < div[0].children.length; i++) {
          divContent.push(div[0].children[i].children[0].firstChild.data);
        }
        pvtDivs[pvtDiv] = divContent;
      }
      return pvtDivs;
    },
    savePivottable() {
      if (this.pivottableName) {
        let pivottableContent = this.getPivottableContent();
        pivottableContent["pivottableName"] = this.pivottableName;
        pivottableContent["cubeName"] = this.selectedCube;
        this.$http.post("api/pivottable/save", pivottableContent);

        this.$notify({
          group: "user",
          title: "Successfully Saved",
          type: "success",
        });
        this.$emit("refreshPivotTables", true);
      } else {
        this.$notify({
          group: "user",
          title: "Missing pivottable title",
          type: "error",
        });
      }
    },
  },
  watch: {
    selectedCube: function(cube) {
      this.$http
        .get("api/query_builder/" + cube)
        .then(response => {
          return response.json();
        })
        .then(data => {
          this.df = data;
          this.render_pivottable();
        });
    },
    selectedPivotTable: function(pivotTable) {
      if (pivotTable.cube_name && pivotTable.name) {
        this.pivottableName = pivotTable.name;
        this.selectedCube = pivotTable.cube_name;
      } else {
        this.df = "";
        this.render_pivottable();
      }
    },
  },
  created() {
    this.userCubes = this.getUserCubes();

    if (this.selectedPivotTable) {
      this.selectedCube = this.selectedPivotTable.cube_name;
      this.pivottableName = this.selectedPivotTable.name;
    }
  },
};
</script>

<style scoped>
#cube_selector {
  width: 42%;
}
</style>
