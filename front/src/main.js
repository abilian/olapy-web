import Vue from 'vue'
import App from './App.vue'


import CubeDetail from "./cubes/cube-details.vue"

new Vue({
  el: "#cube-details",
  delimiters: ["[[", "]]"],
  components: {
    CubeDetail,
  },
});


// new Vue({
//   el: '#cube-details',
//   components: {
//       CubeDetail,
//     },
//   render: h => h(App)
// })
