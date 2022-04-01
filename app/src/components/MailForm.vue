<template>
  <div class="MailForm">
    <p class="maildec">
      メールアドレスを入力してください<br />Please provide your  e-mail
      address
    </p>
    <br />
    <input
      id="email_input"
      type="text"
      class="textfiled"
      v-model="text"
      v-on:blur="scrolltop"
      placeholder="example@example.com"
    />
  </div>
</template>

<script>
export default {
  name: "MailForm",
  components: {},
  props: {
    myvalue: String,
  },
  methods: {
    scrolltop: function () {
      window.scroll({ top: 0, behavior: "smooth" });
    },
  },
  computed: {
    text: {
      get: function () {
        return this.myvalue;
      },
      set: function (newValue) {
        this.$emit("update:myvalue", newValue);
      },
    },
  },
};
</script>

<style lang="scss" scoped>
.page {
  justify-content: center;
  align-items: center;
}
.title {
  margin-bottom: 140px;
}
.buttonn {
  margin-top: 125px;
}
.textfiled {
  background: #ffffff;
  height: 55px;
  width: 100%;
  border: 1px solid #50c68d;
  box-sizing: border-box;
  border-radius: 4px;
  padding: 16px 12px;
  font-size: 13px;
}
.maildec {
  align-self: flex-start;
  font-weight: 700;
  text-align: left;
}
.MailForm {
  margin-top: 40px;
}
</style>