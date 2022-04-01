<template>
  <div class="page">
    <div class="content">
      <p class="title">
        ダウンロードしたファイルは大切に保管して下さい / Please keep this file.
      </p>
      <img src="../assets/thank.svg" />
      <p>
        登録が完了しました。投票期間の開始と同時に、投票用URLが登録したアドレスに送信されます。
        投票期間は11月21日0時0分から11月27日23時59分です。
        期間内に投票用URLから投票ページにアクセスし、投票を完了してください。
        <bold>
          このページでダウンロードしたファイル（鍵ファイルといいます）は、投票の際に利用します。他人に公開せず、安全に保管してください。
          鍵ファイルをなくした場合、投票が無効となる可能性があります。 </bold
        >登録ありがとうございました。

        <br /><br />
        Registration completed. Voting period starts at November 21, 00:00 and
        ends at November 27, 23:59, both in JST. Another e-mail with the voting
        URL will be delivered to your  address when the voting period has
        begun. Please visit the voting webpage and complete the vote within this
        period. Thank you for registration!
        <bold>
          You will need this (key) file when you will vote. Please do not share
          this file and save it safely. If you lost the file, may make your
          ballot invalid.
        </bold>

        <br /><br />鍵ファイルの再ダウンロードは
        <a download="keys.json" v-bind:href="data">こちら</a> です。Click
        <a download="keys.json" v-bind:href="data">here</a>
        to re-download the key file.
        <br /><br />
      </p>
    </div>
  </div>
</template>

<script>
import init, { blind } from "sender";

const generateEncodedKeyPair = async () => {
  const keypairs = await window.crypto.subtle.generateKey(
    {
      name: "RSASSA-PKCS1-v1_5",
      modulusLength: 2048,
      publicExponent: new Uint8Array([1, 0, 1]), // 24 bit representation of 65537
      hash: { name: "SHA-256" },
    },
    true,
    ["sign", "verify"]
  );

  const rawPubkey = await window.crypto.subtle.exportKey(
    "spki",
    keypairs.publicKey
  );

  const rawPrivkey = await window.crypto.subtle.exportKey(
    "pkcs8",
    keypairs.privateKey
  );

  const encodedPubkey = btoa(String.fromCharCode(...new Uint8Array(rawPubkey)));

  const encodedPrivkey = btoa(
    String.fromCharCode(...new Uint8Array(rawPrivkey))
  );

  return {
    encodedPubkey,
    encodedPrivkey,
  };
};

const doBlind = async (msg, pubkey) => {
  await init("static/sender_bg.wasm");

  const blindResult = blind(msg, pubkey);

  if (!blindResult) {
    throw new Error("failed to blind");
  }

  if (blindResult.startsWith("err: ")) {
    // err: hoge => hoge
    throw new Error(
      "認証データの生成中にエラーが発生しました: " + blindResult.substr(5)
    );
  }

  const { blinded_digest, unblinder } = JSON.parse(blindResult);

  return { blinded_digest, unblinder };
};

const saveLocally = (unblinder, pubkey, privkey) => {
  localStorage.setItem("unblinder", unblinder);
  localStorage.setItem("pubkey", pubkey);
  localStorage.setItem("privkey", privkey);
};

export default {
  name: "Registered",

  data() {
    return {
      data: "",
      keys: "",
      regenerate: false,
    };
  },
  methods: {
    send: async function () {
      const signerPubkeyResp = await this.axios.get("/api/pubkey");
      const signerPubkey = signerPubkeyResp.data;
      console.log(signerPubkey);

      const { encodedPubkey, encodedPrivkey } = await generateEncodedKeyPair();
      const { blinded_digest, unblinder } = await doBlind(
        encodedPubkey,
        signerPubkey
      );

      const password = location.hash.slice(1);

      console.log("blinded ", blinded_digest);

      const params = new URLSearchParams();
      params.append("password", password);
      params.append("blind_digest", blinded_digest);
      params.append("regenerate", this.regenerate);

      try {
        await this.axios.post("/api/confirm", params);
        saveLocally(unblinder, encodedPubkey, encodedPrivkey);
      } catch (e) {
        // ぜんぶエラーコードで分岐した方がいい あとで読む人ごめん
        if (e.response?.data?.error_code === 1) {
          // API 側でいい感じのメッセージ作ってる
          alert(e.response?.data?.error);
        } else if (e.response?.data?.error === "鍵の再生成") {
          const doRegenerate = confirm(
            `鍵の再生性をしようとしています。再生成をすると、過去に生成した鍵ファイルは使えなくなりますが、続行しますか？\n\nDo you want to regenerate key? When it regenerate, the previously generated key file will no longer be available, do you continue?`
          );
          this.regenerate = doRegenerate;

          if (doRegenerate) {
            this.send();
            return;
          }
        }

        if (e.response?.data?.error === "認証情報が間違っています") {
          alert(
            `認証情報が間違っています。 Your authentication information is wrong. (E${e.response.data.error_code})`
          );
          return;
        }

        alert(
          `リクエストの処理に失敗しました。 Failed to process your request: ${e}`
        );
        return;
      }
      const keys = JSON.stringify({
        pubkey: encodedPubkey,
        privkey: encodedPrivkey,
        unblinder: unblinder,
      });

      const url = "data:text/plain;base64," + btoa(keys);

      const a = document.createElement("a");
      document.body.appendChild(a);
      a.download = "keys.json";
      a.href = url;
      a.click();
      document.body.removeChild(a);

      this.data = url;
    },
  },
  mounted: async function () {
    this.send();
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
  font-size: 20px;
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
bold {
  color: red;
}
</style>