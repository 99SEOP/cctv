<template>
  <div>
    <button @click="video_test()">video_test button</button>
    <button @click="cors_test()">cors_test button</button>
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
    async video_test() {
      try {
        const response = await axios.get("http://localhost:5000/video");
        this.msg = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async cors_test() {
      try {
        const response = await axios.get("http://localhost:5000/api/data");
        this.msg = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    startPolling() {
      this.cors_test();
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
