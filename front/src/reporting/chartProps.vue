<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">

          <div class="modal-header">
            {{chartType}}
          </div>

          <div class="modal-body">
            <slot name="body">
              <label>
                <select v-model="selectedCube">
                  <option disabled value="">Choose</option>
                    <option v-for="cube in userCubes">
                      {{ cube }}
                    </option>
                </select>
              </label>
              <hr>
              <label>
                <select v-model="selectedColumn" v-show="allColumns.length > 0">
                  <option disabled value="">Choose</option>
                  <option v-for="dimension in allColumns">
                    {{ dimension }}
                  </option>
                </select>
              </label>
              <hr>
              <label>
                <select v-model="selectedMeasures" v-show="selectedCube !== ''">
                  <option disabled value="">Choose</option>
                  <option v-for="measure in allMeasures">
                    {{ measure }}
                  </option>
                </select>
              </label>
            </slot>
          </div>

          <div class="modal-footer">
            <slot name="footer">
              <!--<button class="modal-default-button" @click="$emit('SelectInputStatus', 'second')">-->
              <button class="modal-default-button" @click="validateChartProps()">
                Finish
              </button>
              <button class="modal-default-button" @click="$emit('showChartProps', false)">
                close
              </button>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import Plotly from "plotly.js";

export default {
  props: ["chartType", "currentChartDiv"],
  data: function() {
    return {
      selectedCube: "",
      userCubes: [],
      allColumns: [],
      selectedColumn: "",
      allMeasures: [],
      selectedMeasures: [],
      labels: [],
      values: [],
    };
  },
  methods: {
    genGraph(grapheType, chartData) {
      if (grapheType === "bar") {
        //todo replace with rest api
        let data = [
          {
            x: ["giraffes", "orangutans", "monkeys"],
            y: [20, 14, 23],
            type: "bar",
          },
        ];
        return {
          data: data,
        };
      } else if (grapheType === "pie") {
        let data = [
          {
            values: Object.values(chartData),
            labels: Object.keys(chartData),
            // values: [19, 26, 55],
            // labels: ["Residential", "Non-Residential", "Utility"],
            type: "pie",
          },
        ];

        // let layout = {
        //   height: 400,
        //   width: 500,
        // };
        return {
          data: data,
          // layout: layout,
        };
      }
    },
    validateChartProps() {
      if (this.selectedCube) {
        let data = {
          selectedCube: this.selectedCube,
          selectedColumn: this.selectedColumn,
          selectedMeasures: this.selectedMeasures,
        };
        this.$http.post("api/cubes/chart_columns", data).then(response => {
          let graph = this.genGraph(this.chartType, response.body);
          let ChartDiv = this.currentChartDiv;
          Plotly.newPlot(ChartDiv, graph.data, graph.layout).then(function() {
            let graphDiv = document.getElementById(ChartDiv);
            graphDiv.style.width = "95%";
            graphDiv.style.height = "95%";
            return Plotly.Plots.resize(graphDiv);
          });
        });
        this.$emit("selectedCube", this.selectedCube);
        this.$emit("showChartProps", false);
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
}

.modal-container {
  width: 70%;
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
