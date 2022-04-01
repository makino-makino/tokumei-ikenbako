<template>
  <div class="progresscontent">
    <div class="circles">
      <div class="bar1" :class="{ already: step > 1 }"></div>
      <div class="bar2" :class="{ already: step > 2 }"></div>
      <div class="box">
        <div
          class="circle"
          :class="{ nowcircle: step == 1, already: step > 1 }"
        ></div>
        <div class="name">鍵読込（自動）<br />Load Key(Auto)</div>
      </div>

      <div class="box">
        <div
          class="circle"
          :class="{ nowcircle: step == 2, already: step > 2 }"
        ></div>
        <div class="name">投票内容入力<br />Enter Vote</div>
      </div>

      <div class="box">
        <div
          class="circle"
          :class="{ nowcircle: step == 3, already: step > 3 }"
        ></div>
        <div class="name">投票確認<br />Confirm Vote</div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

type Props = {
  step: number;
};

export default defineComponent({
  props: {
    step: {
      type: Number,
      required: true,
      defalult: 0,
    },
  },
  emits: ["click"],
  setup(props: Props, context) {
    let classs = props.step;
    return { classs };
  },
});
</script>

<style lang="scss" scoped>
.bar1 {
  position: absolute;
  width: 50%;
  top: 7.5px;
  background-color: #c4c4c4;
  height: 1px;
}
.bar2 {
  position: absolute;
  width: 50%;
  top: 7.5px;
  left: 50%;
  background-color: #c4c4c4;
  height: 1px;
}
.progresscontent {
  height: 50px;
  width: 90%;
  padding: 10px;
  margin-left: auto;
  margin-right: auto;
}
.circles {
  display: flex;
  width: 100%;
  justify-content: space-between;
  position: relative;
}
.circle {
  height: 16px;
  width: 16px;
  border-radius: 50%;
  background-color: #c4c4c4;
}
.box {
  z-index: 99;
  position: relative;
}
.name {
  position: absolute;
  width: 100px;
  transform: translateX(-50%);
  left: 50%;
  font-weight: 700;
  margin-top: 10px;
}
.already {
  background-color: $green;
}
.nowcircle {
  background: #f08548;
}
</style>
