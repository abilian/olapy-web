import Vue from 'vue'
import VueResource from 'vue-resource';
import App from './App.vue'


Vue.use(VueResource);

Vue.http.options.root = 'http://127.0.0.1:5000/api/';

new Vue({
  el: '#designer',
  delimiters: ['[[', ']]'],
  render: h => h(App)
});
