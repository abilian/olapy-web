import Vue from "vue";
import VueResource from "vue-resource";
import App from "./App.vue";
import Reporting from "./reporting/BaseReport.vue";

Vue.use(VueResource);

Vue.http.options.root = "http://127.0.0.1:5000/";

// Vue.config({
// 	delimiters: ["<%", "%>"]
// });

Vue.mixin({ delimiters: ["<%", "%>"] });

window.$ = require("jquery");
window.jQuery = window.$;
window.$ = $.extend(require("jquery-ui"));

export const eventBus = new Vue({
  methods: {
    queriedCube(cubeName) {
      this.$emit("queriedCube", cubeName);
    },
  },
});

Vue.config.devtools = true;

if (document.getElementById("designer")) {
  new Vue({
    el: "#designer",
    // delimiters: ["[[", "]]"],
    render: h => h(App),
  });
}

if (document.getElementById("reporting")) {
  new Vue({
    el: "#reporting",
    // delimiters: ["<%", "%>"],
    // delimiters: ["[[", "]]"],
    // components: Reporting,
      render: h => h(Reporting),

  });
}
    // render: h => h(Reporting),
// var vue = new Vue({
//   el: '#vue-app',
//   router,
//   store,
//   template: '<App/>',
//   mixins: [Mixins],
//   components: { App }
// })

