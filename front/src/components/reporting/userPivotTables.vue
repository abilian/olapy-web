<template>
  <li>
    <div class="nav-btn">
      <button class="white-btn" @click="selectPivotTable()">
        <i class="fa fa-tachometer"></i> <span>Query Builder</span>
      </button>
    </div>

    <a class="has-arrow  " href="#" aria-expanded="false">
      <span class="hide-menu">
        <span class="label label-rouded label-success pull-right">{{
          userPivotTables.length
        }}</span>
      </span>
    </a>
    <ul aria-expanded="false" class="collapse">
      <li
        v-for="(userPivotTable, index) in userPivotTables"
        :key="userPivotTable + index"
      >
        <button
          class="btn btn-default btn-outline btn-rounded m-b-10"
          @click="selectPivotTable(userPivotTable)"
        >
          {{ userPivotTable }}
        </button>
      </li>
    </ul>
  </li>
</template>

<script>
import axios from "axios";

export default {
  props: {
    userPivotTables: Array,
  },

  methods: {
    selectPivotTable(userPivotTable) {
      if (userPivotTable) {
        this.$emit("reportingInterface", "");
        axios.get("api/pivottable/" + userPivotTable).then(response => {
          this.$emit("selectedPivotTable", response.data);
          this.$emit("reportingInterface", "QBuilder");
        });
      } else {
        const emptyPVT = {
          name: "",
          cube_name: "",
          columns: [],
          rows: [],
        };
        this.$emit("selectedPivotTable", emptyPVT);
        this.$emit("reportingInterface", "QBuilder");
      }
    },
  },
};
</script>
