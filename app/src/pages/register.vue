<template>
  <div class="page">
    <div class="content">
      <div class="back" @click="doback">&lt; タイトルに戻る</div>
      <p class="title">
        Title
      </p>

      <MailForm
        v-model:myvalue="email"
        class="changecontent"
        v-if="step == 1"
      />
      <div class="bottomstatic" :class="{ isVote: step == 2 }">
        <!--
          To disable button again, replace:
          :disable="enableButton"
          to
          disable="true"
        -->
        <Button
          text="登録 / Register"
          :disable="enableButton"
          class="buttonn"
          @click="donext"
          tagId="register_email"
        />
      </div>
    </div>
  </div>
</template>

<script>
import Button from "../components/Button";
import Progress from "../components/Progress";
import MailForm from "../components/MailForm";
import VoteView from "../components/VoteView";
import CheckView from "../components/CheckView";

const errorMessages = {
  alreadyRegistered: "email already registered",
};

export default {
  name: "CreateVote",
  components: {
    Button,
    Progress,
    MailForm,
    VoteView,
    CheckView,
  },
  mounted() {},
  data() {
    return {
      step: 1,
      email: "",
      vote: 0,
      facedata: "",
      carddata: "",
      is_proccessing: false,
    };
  },
  methods: {
    donext: async function () {
      if (this.is_proccessing) return;

      this.is_proccessing = true;

      const params = new URLSearchParams();
      params.append("email", this.email);
      try {
        await this.axios.post("/api/register", params);
        this.$router.push({ path: "registered" });
      } catch (e) {
        // FIXME: アラートじゃなくて画面に出す？
        console.log("axios error", { json: e });

        // ぜんぶエラーコードで分岐した方がいい あとで読む人ごめん
        if (e.response?.data?.error_code === 1) {
          // API 側でいい感じのメッセージ作ってる
          alert(e.response?.data?.error);
        } else {
          // else で囲まないと２回連続alertでる
          switch (e.response?.data?.error) {
            case errorMessages.alreadyRegistered:
              alert(
                `そのメールアドレスは既に登録されています。 That email address is already used. (E${e.response.data.error_code})`
              );
              break;
            default:
              alert(
                `リクエストの処理に失敗しました。 Failed to process your request: ${e}`
              );
              break;
          }
        }
      }
      this.is_proccessing = false;
    },
    doback: function () {
      if (this.step == 1) {
        this.$router.push("/");
      } else {
        this.step--;
      }
    },
  },
  computed: {
    enableButton: {
      get: function () {
        const regex = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+$/;
        return !regex.test(this.email);
      },
    },
  },
};
</script>

<style lang="scss" scoped>
.ekycimg {
  margin-left: 10px;
}
.ekyc {
  display: flex;
  align-items: center;
  align-self: center;
  margin-top: 45px;
  flex-direction: column;
  text-align: left;
  margin-bottom: 20px;
}
.back {
  font-weight: 700;
  color: $green;
  cursor: pointer;
}
.page {
  padding: 50px 30px;
  justify-content: flex-start;
  flex-direction: column;
}
.title {
  margin-top: 40px;
  text-align: left;
  font-size: 25px;
}
.buttonn {
  margin-top: 240px;
  align-self: center;
  margin: 0;
}
.changecontent {
  width: 100%;
}
.content {
  position: relative;
}
.bottomstatic {
  position: sticky;
  bottom: 0;
  height: 80px;
  width: 100%;
  background-color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}
.isVote {
  box-shadow: 0px -67px 78px #ffffff;
}
.titleeky {
  margin-bottom: 10px;
}
</style>