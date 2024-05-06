<template>
  <body>
    <div>
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
      <p>
        <span>Upward</span> :
        <span class="data-left-align">{{ msg.car_count_up }}</span>
      </p>
      <p>
        <span>Downward</span> :
        <span class="data-left-align">{{ msg.car_count_down }}</span>
      </p>
      <p>
        <span>Leftward</span> :
        <span class="data-left-align">{{ msg.car_count_left }}</span>
      </p>
      <p>
        <span>Rightward</span> :
        <span class="data-left-align">{{ msg.car_count_right }}</span>
      </p>
      <br />
      <p>
        <span>측정 시작 시각</span> :
        <span class="data-left-align">{{ this.timeString }}</span>
      </p>
      <p>
        <span>총 측정 시간</span> :
        <span class="data-left-align">{{ this.onGoingString }}</span>
      </p>
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
      onGoingTime: 0,
      timeString: "",
      onGoingString: "",
    };
  },
  created() {
    this.gotClock();
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
        this.onGoingTime += 1;
        this.updateCounter();
      }, 1000);
    },
    stopPolling() {
      clearInterval(this.pollingInterval);
    },
    gotClock() {
      var now = new Date();
      var year = now.getFullYear();
      var month = now.getMonth() + 1;
      var day = now.getDate();
      var hours = now.getHours();
      var minutes = now.getMinutes();
      var seconds = now.getSeconds();

      month = month < 10 ? "0" + month : month;
      day = day < 10 ? "0" + day : day;
      hours = hours < 10 ? "0" + hours : hours;
      minutes = minutes < 10 ? "0" + minutes : minutes;
      seconds = seconds < 10 ? "0" + seconds : seconds;

      this.timeString =
        year +
        "/" +
        month +
        "/" +
        day +
        " " +
        hours +
        ":" +
        minutes +
        ":" +
        seconds;
    },
    updateCounter() {
      var hours = Math.floor(this.onGoingTime / 3600);
      var minutes = Math.floor((this.onGoingTime % 3600) / 60);
      var seconds = Math.floor(this.onGoingTime % 60);

      hours = hours < 10 ? "0" + hours : hours;
      minutes = minutes < 10 ? "0" + minutes : minutes;
      seconds = seconds < 10 ? "0" + seconds : seconds;

      this.onGoingString = hours + ":" + minutes + ":" + seconds;
    },
  },
};
</script>

<style>
@font-face {
  font-family: "Roboto", "Orbit";
  src: url("./assets/fonts/Roboto/Roboto-Light.ttf"),
    url("./assets/fonts/Orbit/Orbit-Regular.ttf");
}
.menu {
  width: 100%;
  height: 65px;
  background-position: center;
  background-size: cover;
  background-color: #134b8e;
  color: white;
  position: absolute;
  left: 0;
}
.video {
  margin-top: 150px;
  margin-left: 100px;
  float: left;
}
.container {
  position: fixed;
  left: 30%;
  margin-top: 150px;
  margin-left: 450px;
  width: 720px;
  height: 480px;
  border-radius: 15px;
  background-color: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.2);
  box-shadow: 4px 4px 4px 1px rgba(0, 0, 0, 0.2);
  display: flex;
}
.textData {
  font-family: Roboto;
  font-size: 20px;
  margin: 45px;
}
p {
  display: flex; /* 요소들을 수평으로 배열하기 위해 flexbox 사용 */
  justify-content: space-between; /* 요소들 사이의 공간을 최대한 활용하여 정렬 */
}
p span {
  flex: 1; /* 텍스트의 너비를 균일하게 만들기 위해 사용 */
  margin-right: 0px;
}
.data-left-align {
  text-align: left;
  margin-left: 30px;
}
</style>
