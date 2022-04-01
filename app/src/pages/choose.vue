<template>
  <div class="page">
    <div class="content">
      <div class="back" @click="doback">
        {{ getBackText }}
      </div>
      <p class="title">
        Title<br />Vote
      </p>
      <Progress :step="step" />
      <LoadKey v-if="step == 1" :onFileLoadFinished="onFileLoadFinished" />

      <VoteView
        v-if="step == 2"
        :votes="votes"
        :freeDescription="freeDescription"
        @voted="voted"
        @freeDescriptionUpdated="freeDescriptionUpdated"
        @nextDidTap="donext"
      />
      <CheckView
        v-if="step == 3"
        :votes="votes"
        :freeDescription="freeDescription"
      />
      <div
        class="bottomstatic"
        id="button-around"
        :class="{ isVote: step == 3 }"
        v-if="step == 3"
      >
        <Button
          :text="getButtonText"
          :disable="enableButton"
          class="buttonn"
          tagId="donext"
          @click="donext"
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
import LoadKey from "../components/LoadKey";

const VOTES = [
  {
    id: 0,
    title: "1-1 A",
    desc: "",
    vote: null,
  },
  { id: 1, title: "1-2 B", desc: "", vote: null },
  { id: 2, title: "1-3 C", desc: "", vote: null },
  { id: 3, title: "1-4 D", desc: "", vote: null },
  { id: 4, title: "1-5 E", desc: "", vote: null },
  { id: 5, title: "2-1 F", desc: "", vote: null },
  { id: 6, title: "2-2 G", desc: "", vote: null },
  { id: 7, title: "2-3 H", desc: "", vote: null },
  {
    id: 8,
    title: "3-1",
    desc: "",
    vote: null,
  },
  {
    id: 9,
    title: "3-3",
    desc: "",
    vote: null,
  },
  { id: 10, title: "10", desc: "", vote: null },
  { id: 11, title: "11", desc: "", vote: null },
  {
    id: 12,
    title:
      "12",
    desc: "",
    vote: null,
  },
];

const errorMessages = {
  invalidFormat: "data you sent have an invalid format",
  invalidKeySigPair: "invalid RSA signature and pubkey pair",
  signatureAlreadyUsed: "that signature is already used",
  signatureInvalid: "signature verification failed",
};

const str2ab = (str) => {
  const buf = new ArrayBuffer(str.length);
  const bufView = new Uint8Array(buf);
  for (let i = 0, strLen = str.length; i < strLen; i++) {
    bufView[i] = str.charCodeAt(i);
  }
  return buf;
};

const importPrivkey = async (pem) => {
  const binaryDerString = window.atob(pem);
  const binaryDer = str2ab(binaryDerString);

  return await window.crypto.subtle.importKey(
    "pkcs8",
    binaryDer,
    {
      name: "RSASSA-PKCS1-v1_5",
      hash: "SHA-256",
    },
    true,
    ["sign"]
  );
};

export default {
  name: "Choose",
  components: {
    Button,
    Progress,
    MailForm,
    VoteView,
    CheckView,
    LoadKey,
  },
  mounted() {},
  data() {
    return {
      step: 1,
      votes: VOTES,
      freeDescription: "",
      fileLoaded: true,
    };
  },
  methods: {
    voted: function (val, index) {
      this.votes[index].vote = val;
    },
    freeDescriptionUpdated: function (val) {
      this.freeDescription = val;
    },
    onFileLoadFinished: function () {
      this.step++;
    },
    donext: async function () {
      if (this.step == 3) {
        const unblindSignature = localStorage.getItem("unblind_signature");
        const encodedPubkey = localStorage.getItem("pubkey");
        const encodedPrivkey = localStorage.getItem("privkey");
        const privkey = await importPrivkey(encodedPrivkey);

        const jsonMessage = {
          votes: this.votes.map((v) => v.vote),
        };

        const message = JSON.stringify(jsonMessage);

        const rawSiganature = await window.crypto.subtle.sign(
          {
            name: "RSASSA-PKCS1-v1_5",
          },
          privkey,
          str2ab(message)
        );

        const encodedSiganature = btoa(
          String.fromCharCode(...new Uint8Array(rawSiganature))
        );

        console.log("unblind signature", unblindSignature);

        const params = new URLSearchParams();
        params.append("message", message);
        params.append("free_description", this.freeDescription);
        params.append("signature", encodedSiganature);
        params.append("unblind_signature", unblindSignature);
        params.append("pubkey", encodedPubkey);

        try {
          await this.axios.post("/api/vote", params);
          this.$router.push({ path: "done" });
        } catch (e) {
          // FIXME: アラートじゃなくて画面に出す？
          console.log("axios error", { json: e });
          switch (e.response?.data?.error) {
            case errorMessages.invalidFormat:
              alert(
                `署名のデータ形式が不正です。 The ignature's format was invalid. (E${e.response.data.error_code})`
              );
              break;
            case errorMessages.invalidKeySigPair:
              alert(
                `署名データと鍵の組み合わせが不正です。 Invalid pair of signature and key. (E${e.response.data.error_code})`
              );
              break;
            case errorMessages.signatureAlreadyUsed:
              alert(
                `署名データが既に使用済みです。 The signature has already used. (E${e.response.data.error_code})`
              );
              break;
            case errorMessages.signatureInvalid:
              alert(
                `誤った署名です。 Wrong signature. (E${e.response.data.error_code})`
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

      this.step++;
    },
    doback: function () {
      console.log(this.fileLoaded);
      if (this.step == 1) {
        this.$router.push("/vote");
      } else if (this.step == 2 && !this.fileLoaded) {
        this.$router.push("/vote");
      } else {
        this.step--;
      }
    },
  },
  computed: {
    enableButton: {
      get: function () {
        if (this.step == 1) {
        } else if (this.step == 1) {
          return this.vote == 0;
        } else if (this.step == 2) {
          return false;
        }
      },
    },
    getButtonText: function () {
      const msgs = ["", "次へ / Continue", "投票する / Submit your vote"];
      return msgs[this.step - 1];
    },
    getBackText: function () {
      const msgs = [
        "< タイトルへ戻る",
        "< 鍵ファイル選択に戻る",
        "< 投票画面へ戻る",
      ];
      return msgs[this.step - 1];
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
  margin-bottom: 30px;
  text-align: left;
  font-size: 21px;
}
.buttonn {
  margin-top: 240px;
  align-self: center;
  margin: 0;
  width: 200px;
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