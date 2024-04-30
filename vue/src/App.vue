<template>
  <body
    topmargin="0"
    bottommargin="0"
    leftmargin="0"
    rightmargin="0"
    style="background-color: #f6f6f6"
  >
    <div class="menu">
      <nav class="clearfix">
        <ul class="clearfix"></ul>
        <a id="pull" href="#"></a>
      </nav>
    </div>
  </body>
  <div>
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
<style>
nav {
  font-size: 12pt;
  font-family: "PT Sans", Arial, Sans-serif;
  position: relative;
}
nav ul {
  padding: 0;
  margin: 0 auto;
  width: auto;
}
nav a {
  line-height: 50px;
  height: 50px;
}
nav li a {
  box-sizing: border-box;
  -moz-box-sizing: border-box;
  -webkit-box-sizing: border-box;
}
nav li:last-child a {
  border-right: 0;
}
nav a#pull {
  display: none;
}
html {
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  user-select: none;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
}
ul {
  /*list-style-type: none;*/
  margin: 0;
  padding: 0;
  background-color: #333;
  text-align: center;
}
li {
  /*position: relative;*/
  display: inline-block;
}
li a {
  color: #ffffff;
  text-align: center;
  padding: 14.5px 16px;
  text-decoration: none;
}
li a:hover {
  color: #ffd400;
  font-weight: normal;
}
.menu {
  width: 100%;
  height: 50px;
  text-align: center;
  max-width: 100%;
  background-position: center;
  background-size: cover;
  background-color: #333333;
  color: white;
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
}
</style>
