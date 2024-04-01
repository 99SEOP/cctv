<template>
  <div>
    <h1>영상 프레임</h1>
    <div v-if="videoFrames">
      <img :src="videoFrames" alt="Video Frame" />
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "App",
  data: () => {
    return {
      msg: "",
      videoFrames: null,
    };
  },
  mounted() {
    this.video_test();
    this.startPolling();
  },
  components: {},
  methods: {
    async video_test() {
      try {
        const response = await axios.get("http://localhost:5000/video");
        this.videoFrames = response.data;
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
      this.pollingInterval = setInterval(() => {
        this.video_test();
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
<style></style>
