<template>
  <div class="loadcomponent">
    <h1>鍵ファイルの読み込み / Load Key</h1>
    <br />
    <p>
      お使いのブラウザでは鍵の保存を確認できませんでした。ファイルから読み込んでください。<br />
      It couldn't confirm the key storage in your browser. Please load from the
      file.
    </p>
    <input type="file" ref="file" style="display: none" @change="onFileLoad" />
    <div class="bottomstatic" :class="{ isVote: step == 2 }">
      <Button
        text="鍵ファイルを読み込む / Load key file"
        :disable="enableButton"
        class="buttonn"
        @click="onTryFileLoad"
        tagId="load_key"
      />
    </div>
  </div>
</template>
<script>
import Button from "./Button";
import init, { verify, unblind } from "sender";

export default {
  name: "LoadKey",
  components: { Button },
  data() {
    return {
      text: "ファイルを読み込む / Read File",
    };
  },
  props: {
    onFileLoadFinished: () => {},
  },
  mounted: function () {
    // check local storage keys
    const pubkey = localStorage.getItem("pubkey");
    const privkey = localStorage.getItem("privkey");
    const unblinder = localStorage.getItem("unblinder");

    if (pubkey && privkey && unblinder) {
      const loadKey = confirm(
        "お使いのブラウザに鍵を確認できました。自動で読み込みますか？"
      );
      if (loadKey) this.checkKeys(pubkey, privkey, unblinder);
    }
  },
  methods: {
    checkKeys: async function (pubkey, privkey, unblinder) {
      await init("static/sender_bg.wasm");

      const signerPubkeyResp = await this.axios.get("/api/pubkey");
      const signerPubkey = signerPubkeyResp.data;

      const blindSignature = localStorage.getItem("blind_signature");
      const unblindSignature = unblind(unblinder, blindSignature, signerPubkey);

      let res = false;
      try {
        res = verify(pubkey, unblindSignature, signerPubkey) === "valid";
        console.log("hello: ", verify(pubkey, unblindSignature, signerPubkey));
      } catch (e) {
        alert(
          "認証データの検証に失敗しました。 Your authentication information was invalid." +
            e
        );
      }

      if (res) {
        localStorage.setItem("unblind_signature", unblindSignature);
        this.onFileLoadFinished();
      } else {
        alert(
          "鍵または投票用URLが不正です。 Your secret key or URL used to vote was wrong. (E101)"
        );
      }
    },
    onTryFileLoad: function (event) {
      this.$refs.file.click();
    },

    onFileLoad: async function (event) {
      const checkKeys = this.checkKeys;

      const file = event.target.files[0];
      console.log(file);

      const reader = new FileReader();
      reader.readAsText(file);

      reader.onload = async function () {
        const { pubkey, privkey, unblinder } = JSON.parse(reader.result);

        localStorage.setItem("pubkey", pubkey);
        localStorage.setItem("privkey", privkey);
        localStorage.setItem("unblinder", unblinder);

        checkKeys(pubkey, privkey, unblinder);
      };
    },
  },
};
</script>

<style lang="scss" scoped>
.loadcomponent {
  margin-top: 20px;
  width: 100%;
  display: grid;
  padding: 10px;
  padding-bottom: 100px;
}
.anvote {
  height: 0;
  padding-bottom: 100%;
  position: relative;
  box-shadow: 0px 0px 2px rgba(0, 0, 0, 0.25);
  border-radius: 4px;
  cursor: pointer;
  @media (hover: hover) {
    &:hover {
      box-shadow: 0px 0px 2px $green;
    }
  }
}
.anvotecontent {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  p {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
    overflow: hidden;
    width: 100%;
  }
  padding: 8px;
  text-align: center;
  font-weight: bold;
  display: flex;
  align-items: center;
}
.isselected {
  background-color: #e9ffe6;
}

.bottomstatic {
  margin-top: 50px;
  position: sticky;
  bottom: 0;
  height: 80px;
  width: 100%;
  background-color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}
.buttonn {
  width: 250px;
}
</style>