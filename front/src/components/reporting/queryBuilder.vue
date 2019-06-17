<template>
  <div class="page-wrapper">
    <div id="pivotOptions" class="row page-titles">
      <div class="col-md-5 align-self-center">
        <select id="cube_selector" class="form-control" v-model="selectedCube">
          <option disabled value="">Cube</option>
          <option v-for="(cube, index) in userCubes" :key="cube + index">
            {{ cube }}</option
          >
        </select>
      </div>
      <div v-if="selectedCube" class="col-md-7 align-self-center">
        <ol class="breadcrumb">
          <label>
            <input
              type="text"
              v-model="pivottableName"
              class="form-control input-rounded"
              placeholder="Pivottable Title"
            />
          </label>

          <button
            type="button"
            class="btn btn-success m-b-10 m-l-5"
            @click="savePivottable"
          >
            <span
              v-if="selectedPivotTable.cube_name && selectedPivotTable.name"
            >
              Update
            </span>
            <span v-else> Save </span>
          </button>

          <button
            v-if="selectedPivotTable.cube_name && selectedPivotTable.name"
            type="button"
            class="btn btn-danger m-b-10 m-l-5"
            @click="deletePivottable"
          >
            Delete
          </button>
        </ol>
      </div>
    </div>

    <div class="panel panel-default">
      <div style="padding-left: 25px">
        <div class="row" style="margin-right: 25px">
          <div
            v-if="selectedCube"
            id="output"
            style="overflow: auto; display: none;"
          >
            {{ DataFrameCsv }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
const $ = require("jquery");
require("jquery-ui-bundle");
require("pivottable");
require("pivottable/dist/c3_renderers");
require("pivottable/dist/d3_renderers");
require("pivottable/dist/export_renderers");
// UNCOMMENT IF YOU WANT TO USE PLOTLY CHARTS
// require('pivottable/dist/plotly-latest.min.js');
// require('pivottable/dist/plotly_renderers.min.js');

export default {
  props: {
    selectedPivotTable: Object,
  },

  data: function() {
    return {
      pivottableName: null,
      selectedCube: "",
      userCubes: [],
      DataFrameCsv: null,
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
      const userCubes = [];
      axios
        .get("api/cubes")
        .then(response => {
          return response.data;
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

      //    renderers: $.extend(
      //       jQuery.pivotUtilities.renderers,
      //       jQuery.pivotUtilities.c3_renderers,
      //       jQuery.pivotUtilities.d3_renderers,
      //       jQuery.pivotUtilities.export_renderers
      //     ),
      $("#output")
        .pivotUI(this.DataFrameCsv, {
          renderers: $.extend(
            $.pivotUtilities.renderers,
            $.pivotUtilities.c3_renderers,
            $.pivotUtilities.d3_renderers,
            $.pivotUtilities.export_renderers
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
      const pvtDivs = {
        pvtRows: null,
        pvtCols: null,
      };
      for (let pvtDiv in pvtDivs) {
        const divContent = [];
        const div = document.getElementsByClassName(pvtDiv);
        for (let i = 0; i < div[0].children.length; i++) {
          divContent.push(div[0].children[i].children[0].firstChild.data);
        }
        pvtDivs[pvtDiv] = divContent;
      }
      return pvtDivs;
    },

    savePivottable() {
      if (this.pivottableName) {
        const pivottableContent = this.getPivottableContent();
        pivottableContent["pivottableName"] = this.pivottableName;
        pivottableContent["cubeName"] = this.selectedCube;
        axios.post("/api/pivottable/save", pivottableContent);

        this.$notify({
          group: "user",
          title: "Successfully Saved",
          type: "success",
        });
        this.$emit("addPivotTableName", this.pivottableName);
      } else {
        this.$notify({
          group: "user",
          title: "Missing pivottable title",
          type: "error",
        });
      }
    },

    deletePivottable() {
      const vue = this;
      this.$dlg.alert(
        "Are you sure to delete " + vue.pivottableName + " ?",
        function() {
          if (vue.pivottableName) {
            const data = {
              pivottableName: vue.pivottableName,
            };
            axios.post("/api/pivottable/delete", data);

            vue.$notify({
              group: "user",
              title: "Successfully Deleted",
              type: "success",
            });

            vue.$emit("removePivotTableName", vue.pivottableName);
            vue.$emit("reportingInterface", "main");
          } else {
            vue.$notify({
              group: "user",
              title: "Missing dashboard title",
              type: "error",
            });
          }
        },
        {
          messageType: "confirm",
          language: "en",
        }
      );
    },
  },

  watch: {
    selectedCube(cube) {
      if (cube) {
        axios
          .get("api/query_builder/" + cube)
          .then(response => {
            return response.data;
          })
          .then(data => {
            this.DataFrameCsv = data;
            this.render_pivottable();
          });
      }
    },
    selectedPivotTable(pivotTable) {
      if (pivotTable.cube_name && pivotTable.name) {
        this.selectedCube = pivotTable.cube_name;
        this.pivottableName = pivotTable.name;
      } else {
        $("#output").empty();
        this.selectedCube = "";
        this.pivottableName = "";
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

<style lang="scss" scoped>
@import "~pivottable/dist/pivot.css";
@import "~c3/c3.min.css";
#cube_selector {
  width: 42%;
}
</style>
