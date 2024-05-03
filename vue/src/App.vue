<template>
  <body>
    <div class="top">
      <img src="./assets/cwnu_logo.png" height="45" />
    </div>
  </body>
  <body>
    <div class="menu"></div>
  </body>
  <div class="video">
    <iframe src="http://localhost:5000/video" width="720" height="480" />
  </div>
  <div class="container">
    <div class="textData">
      <p>car_up : {{ msg.car_count_up }}</p>
      <p>car_down : {{ msg.car_count_down }}</p>
      <p>car_left : {{ msg.car_count_left }}</p>
      <p>car_right : {{ msg.car_count_right }}</p>
      <br />
      <p>측정 시작 시간 :</p>
      <p>측정 시간 :</p>
    </div>
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
<style>
.menu {
  width: 100%;
  height: 65px;
  background-position: center;
  background-size: cover;
  background-color: #134b8e;
  color: white;
  position: absolute;
  left: 0;
  box-shadow: 0 10px 10px rgba(0, 0, 0, 0.15);
}
.video {
  margin: 100px;
  float: left;
}
.container {
  position: fixed;
  left: 30%;
  margin-top: 100px;
  margin-left: 300px;
  width: 720px;
  height: 480px;
  border-radius: 15px;
  background-color: #ffffff;
  display: flex;
}
.textData {
  font-family: arial;
  font-size: 20px;
  margin: 25px;
}
</style>
