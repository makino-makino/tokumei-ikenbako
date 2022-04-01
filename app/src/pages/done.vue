<template>
  <div class="page">
    <div class="content">
      <p class="title">
        投票を完了しました。<br />You have successfully voted!
      </p>
      <img src="../assets/thank.svg" />
      <p>
        thanks
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Done",
  props: {
    title: String,
    message: String,
  },
};
</script>

<style lang="scss" scoped>
.page {
  justify-content: center;
  align-items: center;
}
.content {
  justify-content: center;
  align-items: center;
}
.title {
  margin-bottom: 70px;
}
.buttonn {
  margin-top: 125px;
}
p {
  margin-top: 50px;
  font-weight: bold;
}
.content {
  padding: 20px;
  text-align: left;
}
</style>

