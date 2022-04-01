<template>
  <div class="page">
    <div class="content">
      <p class="title" v-html="this.title" />
      <img src="../assets/topimage.svg" />
      <div class="buttonWrapper">
        <div v-if="showPolicy">
          事前登録を開始すると、<a
            href="example.com"
            class="policy"
            target="_blank"
            >利用規約</a
          >に同意したものとします。
          <br />
          By starting pre-registration, you agree to the
          <a
            href="example.com"
            class="policy"
            target="_blank"
            >Terms of Service</a
          >.
        </div>
        <br />
        ※最新のPC版Chrome, Firefoxをお使いください / Please use latest Chrome
        or Firefox for PC
        <Button
          class="buttonn"
          @click="next"
          v-text="this.submitText"
          :tagId="this.tagId"
        />
      </div>
    </div>
  </div>
</template>

<script>
import Button from "./Button";
export default {
  name: "StartView",
  components: {
    Button,
  },
  methods: {
    next: function () {
      this.$router.push({ path: this.nextPage });
    },
  },
  props: {
    title: String,
    submitText: String,
    nextPage: String,
    showPolicy: Boolean,
    tagId: String,
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
  margin-bottom: 80px;
  font-size: 20px;
}
.buttonWrapper {
  margin-top: 120px;
  display: flex;
  align-items: center;
  flex-direction: column;
  font-size: 13px;
}
.buttonn {
  margin-top: 16px;
}
.policy {
  color: $green;
  font-weight: 700;
}
</style>
