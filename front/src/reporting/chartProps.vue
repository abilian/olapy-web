<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-header">
            <input
              class="form-control"
              placeholder="Chart Title"
              type="text"
              v-model="chartTitle"
            />
          </div>

          <div class="modal-body">
            <slot name="body">
              <select class="form-control" v-model="selectedCube">
                <option disabled value="">Cube</option>
                <option v-for="cube in userCubes"> {{ cube }} </option>
              </select>

              <div v-show="allColumns.length > 0">
                <hr />
                <select class="form-control" v-model="selectedColumn">
                  <option disabled value="">Dimension</option>
                  <option v-for="dimension in allColumns">
                    {{ dimension }}
                  </option>
                </select>
              </div>

              <div v-show="selectedCube !== ''">
                <hr />
                <select class="form-control" v-model="selectedMeasures">
                  <option disabled value="">Measure</option>
                  <option v-for="measure in allMeasures">
                    {{ measure }}
                  </option>
                </select>
              </div>
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <!--
                <button class="modal-default-button" @click="$emit('SelectInputStatus', 'second')">
              -->
              <button
                class="btn btn-default pull-left"
                @click="$emit('showChartProps', false);"
              >
                Cancel
              </button>

              <button class="btn btn-primary" @click="validateChartProps();">
                Finish
              </button>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import Plotly from "plotly.js/dist/plotly-basic.min.js";

export default {
  props: {
    chartType: String,
    currentChartDiv: String,
  },
  data: function() {
    return {
      selectedCube: "",
      userCubes: [],
      allColumns: [],
      selectedColumn: "",
      allMeasures: [],
      selectedMeasures: [],
      chartTitle: "",
    };
  },
  methods: {
    genGraph(graphType, chartData) {
      let data;
      if (["bar", "scatter"].includes(graphType)) {
        data = [
          {
            y: Object.values(chartData),
            x: Object.keys(chartData),
            type: graphType,
          },
        ];
      } else if (graphType === "pie") {
        data = [
          {
            values: Object.values(chartData),
            labels: Object.keys(chartData),
            type: graphType,
          },
        ];
      }
      let layout = {
        title: this.chartTitle,
        // height: 400,
        // width: 500,
      };
      return {
        data: data,
        layout: layout,
      };
    },
    validateChartProps() {
      if (this.selectedCube) {
        let data = {
          selectedCube: this.selectedCube,
          selectedColumn: this.selectedColumn,
          selectedMeasures: this.selectedMeasures,
        };
        if (this.chartTitle === "") {
          this.chartTitle =
            data.selectedMeasures +
            " of " +
            data.selectedColumn +
            " from " +
            data.selectedCube;
        }
        this.$http
          .post("api/cubes/chart_columns", data)
          .then(response => {
            return response.json();
          })
          .then(data => {
            let graph = this.genGraph(this.chartType, data);
            this.$emit("chartData", graph);
            let ChartDiv = this.currentChartDiv;
            Plotly.newPlot(ChartDiv, graph.data, graph.layout).then(function() {
              let graphDiv = document.getElementById(ChartDiv);
              graphDiv.style.width = "95%";
              graphDiv.style.height = "95%";
              return Plotly.Plots.resize(graphDiv);
            });
            this.$emit("showChartProps", false);
          });
        this.$emit("selectedCube", this.selectedCube);
      }
    },
  },
  watch: {
    selectedCube: function(selectedCube) {
      this.$http
        .get("api/cubes/" + selectedCube + "/columns")
        .then(response => {
          return response.json();
        })
        .then(data => {
          for (let key in data) {
            this.allColumns.push(data[key]);
          }
        });

      this.$http
        .get("api/cubes/" + selectedCube + "/facts")
        .then(response => {
          return response.json();
        })
        .then(data => {
          this.allMeasures = data["measures"];
        });
    },
  },
  created() {
    this.$http
      .get("api/cubes")
      .then(response => {
        return response.json();
      })
      .then(data => {
        for (let key in data) {
          this.userCubes.push(data[key]);
        }
      });
  },
};
</script>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
  overflow: auto;
}

.modal-container {
  width: 25%;
  height: 50%;
  margin: 0px auto;
  padding: 20px 30px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.modal-header h3 {
  margin-top: 0;
  color: #42b983;
}

.modal-body {
  margin: 20px 0;
}

.modal-default-button {
  float: right;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>
