<template>
  <div class="freevote">
    <br />
    <div class="votetitle">{{ title }}</div>
    <div class="desc" v-html="this.desc"></div>
    <textarea class="textArea" v-model="text" id="freevote"></textarea>
  </div>
</template>

<script>
export default {
  name: "FreeVote",
  components: {},
  props: {
    title: String,
    desc: String,
    text: String,
  },
  data() {
    return {};
  },
  methods: {},
  computed: {
    text: {
      get: function () {
        return this.text;
      },
      set: function (newValue) {
        this.$emit("textUpdated", newValue);
      },
    },
  },
};
</script>

<style lang="scss" scoped>
.freevote {
  .votetitle {
    font-size: 17px;
    font-weight: 700;
    text-align: left;
    margin-bottom: 10px;
  }
  .desc {
    text-align: left;
  }
}
.textArea {
  margin-top: 16px;
  background: #ffffff;
  height: 200px;
  width: 100%;
  border: 1px solid #50c68d;
  border-radius: 4px;
  padding: 16px 12px;
  font-size: 13px;
}
</style>