<template>
  <div class="page">
    <div class="content">
      <p class="title">
        登録はまだ完了していません。 <br />
        Your registration is NOT completed yet!
      </p>
      <img src="../assets/thank.svg" />
      <p>
        メールアドレス確認用リンクを先ほどのメールアドレスに送信しました。
        <br />
        A verification link has been delivered to your e-mail address.
        Please check the inbox of your e-mail address.
        <br /><br />

        メールの受信ボックスをご確認ください。
        メールの受信には数分要する場合があります。
        メールを受信できない場合は、迷惑メールフォルダに振り分けられているか、先ほど入力されたアドレスが間違っています。双方ご確認の上、もう一度お試しください。
        <br />
        The e-mail may take few minutes to be delivered. If you don’t see our
        e-mail, it may be in the spam box, or provided address is wrong. Please
        check both and try again.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Registered",

  data() {
    return {
      data: "",
      keys: "",
    };
  },
  mounted: function () {},
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
  font-size: 28px;
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