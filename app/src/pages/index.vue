<template>
  <StartView
    title="投票登録<br>Voting Registration"
    submitText="登録に進む / Continue"
    nextPage="register"
    :showPolicy="true"
    
    tagId="start_register"
  ></StartView>
</template>

<script>
import StartView from "../components/StartView";
export default {
  name: "Home",
  components: { StartView },
};
</script>

