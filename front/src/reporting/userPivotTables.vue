<template>
    <li>

        <div class="nav-btn">
            <button class="white-btn" @click="selectPivotTable()">
                <i class="fa fa-tachometer"></i>
                <span>Query Builder</span>
            </button>
        </div>

        <a class="has-arrow  " href="#" aria-expanded="false">
            <span class="hide-menu">
                <span class="label label-rouded label-success pull-right">{{userPivotTables.length}}</span>
            </span>
        </a>
        <ul aria-expanded="false" class="collapse">
            <li v-for="userPivotTable in userPivotTables">
                <button class="btn btn-default btn-outline btn-rounded m-b-10"
                        @click="selectPivotTable(userPivotTable)">{{userPivotTable}}
                </button>
            </li>
        </ul>
    </li>
</template>

<script>
    export default {
        props: {
            refreshPivotTables: Boolean,
        },
        data: function () {
            return {
                userPivotTables: [],
            };
        },
        methods: {
            selectPivotTable(userPivotTable) {
                if (userPivotTable) {
                    this.$http.get("api/pivottable/" + userPivotTable).then(response => {
                        this.$emit("selectedPivotTable", response.body);
                        this.$emit("reportingInterface", "QBuilder");
                    });
                } else {
                    let emptyPVT = {
                        name: "",
                        cube_name: "",
                        columns: [],
                        rows: [],
                    };
                    this.$emit("selectedPivotTable", emptyPVT);
                    this.$emit("reportingInterface", "QBuilder");
                }
            },
            getAllPivotTables() {
                let pivotTables = [];
                this.$http
                    .get("api/pivottable/all")
                    .then(response => {
                        return response.json();
                    })
                    .then(data => {
                        for (let key in data) {
                            pivotTables.push(data[key]);
                        }
                    });
                this.userPivotTables = pivotTables;
            },
        },

        watch: {
            refreshPivotTables: function (val) {
                if (val === true) {
                    this.getAllPivotTables();
                    this.$emit("refreshPivotTables", false);
                }
            },
        },
        mounted() {
            this.getAllPivotTables();
        },
    };
</script>

<style scoped>
</style>
