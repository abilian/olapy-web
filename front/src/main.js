/* eslint-disable no-new */

import Vue from "vue";
import App from "./App.vue";
import Notifications from "vue-notification";
// import Reporting from "./reporting/BaseReport.vue";

Vue.use(Notifications);

window.$ = require("jquery");

export const eventBus = new Vue({
  methods: {
    queriedCube(cubeName) {
      this.$emit("queriedCube", cubeName);
    },
  },
});

Vue.config.devtools = true;

// if (document.getElementById("designer")) {
//   new Vue({
//     el: "#designer",
//     render: h => h(App),
//   });
// }
//
// if (document.getElementById("reporting")) {
//   new Vue({
//     el: "#reporting",
//     render: h => h(Reporting),
//   });
// }

if (document.getElementById("app")) {
  new Vue({
    el: "#app",
    render: h => h(App),
  });
}
