import Vue from "vue";
import App from "./App.vue";
import router from "./router";

import Notifications from "vue-notification";
import vDialogs from "v-dialogs";

Vue.use(vDialogs);
Vue.use(Notifications);

export const eventBus = new Vue({
  methods: {
    queriedCube(cubeName) {
      this.$emit("queriedCube", cubeName);
    }
  }
});

Vue.config.devtools = true;

Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
