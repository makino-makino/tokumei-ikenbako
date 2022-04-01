<template>
  <div>
    <h1>
      {{ this.title }}
    </h1>
    <p>
      議題本文は<a :href="this.url">こちら</a>
      /Click
      <a :href="this.url">here</a>
      to read the full agenda
    </p>
  </div>
</template>

<script>
export default {
  name: "Title",
  components: {},
  props: {
    title: String,
    url: String,
  },
  data() {
    return {};
  },
};
</script>

<style lang="scss" scoped>
h1 {
  margin-bottom: 10px;
  font-size: 17px;
  text-align: left;
  margin-top: 35px;
}
p {
  font-size: 15px;
  text-align: left;
}
</style>