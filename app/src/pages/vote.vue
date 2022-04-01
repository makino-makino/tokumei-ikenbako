<template>
  <StartView
    title="Title"
    submitText="投票開始 / Continue"
    nextPage="choose"
    :showPolicy="false"
    tagId="start_vote"
  ></StartView>
</template>

<script>
import StartView from "../components/StartView";
export default {
  name: "Vote",
  components: { StartView },
  methods: {
    window: (onload = function () {
      const blind_signature = location.hash.slice(1);
      localStorage.setItem("blind_signature", blind_signature);
    }),
  },
};
</script>

