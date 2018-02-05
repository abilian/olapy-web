import Vue from 'vue'
import App from './App.vue'


new Vue({
  el: '#designer',
  delimiters: ['[[', ']]'],
  render: h => h(App)
});
