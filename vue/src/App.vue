<template>
  <div>
    <h1>영상 테스트</h1>
    <iframe src="http://localhost:5000/video" width="720" height="480" />
  </div>
  <div>
    <p>car_up : {{ msg.car_count_up }}</p>
    <p>car_down : {{ msg.car_count_down }}</p>
    <p>car_left : {{ msg.car_count_left }}</p>
    <p>car_right : {{ msg.car_count_right }}</p>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "App",
  data: () => {
    return {
      msg: "통신 실패",
      videoFrames: null,
    };
  },
  created() {
    this.startPolling();
  },
  beforeUnmount() {
    this.stopPolling();
  },
  methods: {
    async stats_test() {
      try {
        const response = await axios.get("http://localhost:5000/statistics");
        if (response) {
          this.msg = response.data;
        }
      } catch (error) {
        console.error(error);
      }
    },
    startPolling() {
      this.pollingInterval = setInterval(() => {
        this.stats_test();
      }, 1000);
    },
    stopPolling() {
      clearInterval(this.pollingInterval);
    },
  },
};
</script>
<style></style>
