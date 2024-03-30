<template>
  <img alt="Vue logo" src="./assets/logo.png" />
  <div>
    <button @click="startPolling()">cors_test button</button>
  </div>
  <div>
    <p>
      {{ msg }}
    </p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data: () => {
    return {
      msg: "Welcome to Your Vue.js App",
    };
  },
  components: {},
  methods: {
    async cors_test() {
      try {
        const response = await axios.get("http://localhost:5000/numPlus");
        console.log(response);
        this.msg = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    startPolling() {
      this.pollingInterval = setInterval(() => {
        this.cors_test();
      }, 5000);
    },
    stopPolling() {
      clearInterval(this.pollingInterval);
    },
    created() {
      this.startPolling();
    },
    beforeDestroy() {
      this.stopPolling();
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
