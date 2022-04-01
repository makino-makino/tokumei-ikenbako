<template>
  <div>
    <button
      v-on:click="send_email"
      style="background-color: lightblue; border: 1px; margin: 1rem"
    >
      メールを送る
    </button>
    <button
      v-on:click="erase_db"
      style="background-color: lightblue; border: 1px; margin: 1rem"
    >
      データベースのデータを削除する
    </button>
  </div>
</template>

<script>
export default {
  name: "Incubator",
  methods: {
    erase_db: function (_event) {
      const ok = confirm("大いなる力には大いなる責任が伴います。\n本当に全てのデータを削除しますか？");

      if (ok) {
        const params = new URLSearchParams();
        params.append("confirm", 'OK');

        this.axios
          .post("/incubator/api/erase_db", params)
          .then((response) => {
            alert(response.data);
          })
          .catch((e) => {
            alert(e);
          });
      } else {
        alert('skipped');
      }
    },
    send_email: function (_event) {
      this.axios
        .post("/incubator/api/send_email")
        .then((_response) => {
          alert("done");
        })
        .catch((e) => {
          alert(e);
        });
    },
  },
};
</script>