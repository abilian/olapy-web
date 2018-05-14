import Vue from "vue";
import VueResource from "vue-resource";
import App from "./App.vue";
import Reporting from "./reporting/BaseReport.vue";

Vue.use(VueResource);

Vue.http.options.root = "http://127.0.0.1:5000/";

window.$ = require("jquery");
window.jQuery = window.$;
window.$ = $.extend(require("jquery-ui"));
window.$ = $.extend(require("jquery-csv"));

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
