<template>
    <div class="page-wrapper">
        <div class="row page-titles">
            <div class="col-md-5 align-self-center"></div>
            <div class="col-md-7 align-self-center">
                <ol class="breadcrumb">
                    <label>
                        <input
                                type="text"
                                v-model="dashboardName"
                                class="form-control input-rounded"
                                placeholder="Dashboard Title"
                        />
                    </label>

                    <button
                            type="button"
                            class="btn btn-success m-b-10 m-l-5"
                            @click="saveDashboard"
                    >
                        Save
                    </button>

                    <button @click="drawChart()"> Draw</button>
                </ol>
            </div>
        </div>

        chartData => {{chartData}}
        <br>
        {{chartData.length}}
        <br>

        laster : {{chartData[chartData.length - 1 ]}}
        <br>
        <chart-props
                :currentChartDiv="currentChartDiv"
                :chartType="draggedChart"
                v-if="showChartProps === true"
                @chartData="chartData.push($event)"
                @selectedCube="selectedCube = $event"
                @showChartProps="showChartProps = $event"
        />

        <draggable
                @change="addChart"
                id="divDash"
                v-model="usedCharts"
                class="dashboard"
                :options="{ group: 'charts', sort: false }"
        >
        </draggable>

        <grid-layout
                :layout="layout"
                :col-num="12"
                :row-height="30"
                :is-draggable="true"
                :is-resizable="true"
                :is-mirrored="false"
                :vertical-compact="true"
                :margin="[10, 10]"
                :use-css-transforms="true"
        >
            <grid-item
                    v-for="(item, index) in layout"
                    :key="item.i"
                    :x="item.x"
                    :y="item.y"
                    :w="item.w"
                    :h="item.h"
                    :i="item.i"
                    @resize="resize"
            >
                {{index}}<br>
                {{item}}
                <button
                        type="button"
                        class="close"
                        aria-label="Close"
                        @click="removeItem(index);"
                >
                    <span aria-hidden="true">&times;</span>
                </button>
                <div :id="item.i"></div>
            </grid-item>
        </grid-layout>

        <div id="dock-container">
            <ul>
                <draggable
                        :list="chartTypes"
                        :move="onMove"
                        id="dock"
                        :options="{ group: { name: 'charts', pull: 'clone' } }"
                >
                    <li v-for="chart_type in chartTypes">
                        <span>{{ chart_type }}</span>
                        <a href="#">
                            <img
                                    class="toolbox-icons"
                                    :src="'/static/icons/' + chart_type + 'chart.png'"
                            />
                        </a>
                    </li>
                </draggable>
            </ul>
        </div>

    </div>
</template>

<script>
    // import Plotly from "plotly.js-dist";
    import Plotly from "plotly.js/dist/plotly-basic.min.js";

    import draggable from "vuedraggable";
    import VueGridLayout from "vue-grid-layout";
    import ChartProps from "./chartProps";

    let GridLayout = VueGridLayout.GridLayout;
    let GridItem = VueGridLayout.GridItem;

    export default {
        props: {
            reportingInterface: String,
            selectedDashboard: Object,
        },
        data: function () {
            return {
                allowModification: true,
                layout: [],
                usedCharts: [],
                dashboardName: "",
                showChartProps: false,
                currentChartDiv: "",
                chartTypes: ["bar", "scatter", "pie"],
                draggedChart: "",
                chartData: [],
                chart_x_position: 0,
                chart_y_position: 0,
                chart_weight: 6,
                chart_height: 8,
            };
        },
        methods: {
            drawChart() {
                let graph = this.chartData[this.chartData.length - 1];
                Plotly.newPlot(this.currentChartDiv, graph.data, graph.layout).then(function () {
                    alert('22222222222222222222222222222222222');
                    let graphDiv = document.getElementById(this.currentChartDiv);
                    graphDiv.style.width = "95%";
                    graphDiv.style.height = "95%";
                    return Plotly.Plots.resize(graphDiv);
                });
            },
            addChart() {
                let chartDiv = this.draggedChart + (this.usedCharts.length - 1); // - 1
                this.layout[this.usedCharts.length - 1].i = chartDiv; //list.length - 2
                let gridItems = document.getElementsByClassName("vue-grid-item");
                let divDash = gridItems[gridItems.length - 2]; // gridItems.length -2 because last element is the vue-grid-placeholder
                let innerDiv = document.createElement("div");
                innerDiv.id = chartDiv;
                this.currentChartDiv = chartDiv;
                divDash.appendChild(innerDiv);
                this.showChartProps = true;
            },
            removeItem(index) {
                // this.layout.splice(parseInt(index), 1);
                // this.usedCharts.splice(parseInt(index), 1);
                this.layout.splice(index, 1);
                this.usedCharts.splice(index, 1);
            },
            onMove({relatedContext, draggedContext}) {
                this.draggedChart = draggedContext.element;
            },
            resize: function (id) {
                let plotDiv = document.getElementById(id);
                Plotly.Plots.resize(plotDiv);
            },
            saveDashboard() {
                if (this.dashboardName) {
                    let data = {
                        dashboardName: this.dashboardName,
                        usedCharts: this.usedCharts,
                        layout: this.layout,
                        chartData: this.chartData,
                    };
                    this.$http.post("api/dashboard/save", data);

                    this.$notify({
                        group: "user",
                        title: "Successfully Added",
                        type: "success",
                    });
                    this.$emit("refreshDashboards", true);
                    this.$emit("reportingInterface", "main");
                } else {
                    this.$notify({
                        group: "user",
                        title: "Missing dashboard title",
                        type: "error",
                    });
                }
            },
        },
        components: {
            draggable,
            GridLayout,
            GridItem,
            chartProps: ChartProps,
        },
        watch: {
            usedCharts: function (newElements, oldElements) {
                if (newElements.length > oldElements.length && this.draggedChart) {
                    //if add chart not removing one
                    if (this.chart_x_position >= this.chart_weight * 2) {
                        this.chart_x_position = 0;
                        this.chart_y_position += this.chart_height;
                    }
                    this.layout.push({
                        x: this.chart_x_position,
                        y: this.chart_y_position,
                        w: this.chart_weight,
                        h: this.chart_height,
                        i: "",
                    });
                    this.chart_x_position += this.chart_weight;
                }
            },
        },
        created() {
            if (this.selectedDashboard) {
                this.allowModification = false;
                this.layout = this.selectedDashboard["charts_layout"];
                this.usedCharts = this.selectedDashboard["used_charts"];
                this.dashboardName = this.selectedDashboard["name"];
                this.chartData = this.selectedDashboard["charts_data"];
            }
        },
        mounted: function () {
            if (this.selectedDashboard) {
                let gridItems = document.getElementsByClassName("vue-grid-item");
                for (let chart_data in this.selectedDashboard["charts_data"]) {
                    let divDash = gridItems[chart_data];
                    let innerDiv = document.createElement("div");
                    innerDiv.id = this.layout[chart_data].i;
                    divDash.appendChild(innerDiv);
                    Plotly.newPlot(
                        this.layout[chart_data].i,
                        this.selectedDashboard["charts_data"][chart_data].data,
                        this.selectedDashboard["charts_data"][chart_data].layout
                    );
                    let graphDiv = document.getElementById(this.layout[chart_data].i);
                    graphDiv.style.width = "95%";
                    graphDiv.style.height = "95%";
                    Plotly.Plots.resize(graphDiv);
                }
            }
        },
    };
</script>

<style scoped>
    .dash-toolbox {
        position: fixed;
        margin: 32% 22%;
        background: #c7ddef;
        width: 50%;
        height: 50px;
        border-radius: 25px;
        float: right;
    }

    .toolbox-icons {
        margin: 10px 0 0 15px;
        width: 30px;
        height: 30px;
        float: left;
    }

    .dashboard {
        position: absolute;
        top: 135px;
        border-style: dotted;
        height: 100%;
        width: 100%;
    }

    .vue-grid-item:not(.vue-grid-placeholder) {
        /*background: #9dcc31;*/
        /*border: 1px solid black;*/
        background: #ffffff none repeat scroll 0 0;
        margin: 15px 0;
        padding: 20px;
        border: 0 solid #e7e7e7;
        border-radius: 5px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
    }

    .vue-grid-item.resizing {
        opacity: 0.9;
    }

    .vue-grid-item.static {
        background: #cce;
    }

    .vue-grid-item .text {
        font-size: 24px;
        text-align: center;
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        margin: auto;
        height: 100%;
        width: 100%;
    }

    .vue-grid-item .no-drag {
        height: 100%;
        width: 100%;
    }

    .vue-grid-item .minMax {
        font-size: 12px;
    }

    .vue-grid-item .add {
        cursor: pointer;
    }

    .btn-lg {
        padding: 10px 13px;
    }

    /* START MAc style dock*/
    #dock-container {
        position: fixed;
        bottom: 0;
        text-align: center;
        right: 20%;
        left: 20%;
        width: 60%;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px 10px 0 0;
    }

    #dock-container li {
        list-style-type: none;
        display: inline-block;
        position: relative;
    }

    #dock-container li img {
        width: 64px;
        height: 64px;
        -webkit-box-reflect: below 2px -webkit-gradient(linear, left top, left bottom, from(transparent), color-stop(0.7, transparent), to(rgba(255, 255, 255, 0.5)));
        -webkit-transition: all 0.3s;
        -webkit-transform-origin: 50% 100%;
    }

    #dock-container li:hover img {
        -webkit-transform: scale(2);
        margin: 0 2em;
    }

    #dock-container li:hover + li img,
    #dock-container li.prev img {
        -webkit-transform: scale(1.5);
        margin: 0 1.5em;
    }

    #dock-container li span {
        display: none;
        position: absolute;
        bottom: 140px;
        left: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.75);
        padding: 4px 0;
        border-radius: 12px;
    }

    #dock-container li:hover span {
        display: block;
        color: #fff;
    }

    /*END MAc style dock*/
</style>
