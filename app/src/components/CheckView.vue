<template>
  <div class="CheckView">
    <Title
      title="title"
    />
    <div v-for="vote in this.votes.slice(0, 5)" :key="vote.id">
      <div class="checktitle">{{ vote.title }}</div>
      <div class="checkdescriptin">
        {{ getBoolString(vote.vote) }}
      </div>
    </div>

    <Title
      title="title"
    />
    <div v-for="vote in this.votes.slice(5, 8)" :key="vote.id">
      <div class="checktitle">{{ vote.title }}</div>
      <div class="checkdescriptin">
        {{ getBoolString(vote.vote) }}
      </div>
    </div>

    <Title
      title="title"
    />

    <div v-for="vote in this.votes.slice(8, 12)" :key="vote.id">
      <div class="checktitle">{{ vote.title }}</div>
      <div class="checkdescriptin">
        {{ getBoolString(vote.vote) }}
      </div>
    </div>

    <Title
      title="title"
    />

    <div v-for="vote in this.votes.slice(12, 13)" :key="vote.id">
      <div class="checktitle">{{ vote.title }}</div>
      <div class="checkdescriptin">
        {{ getBoolString(vote.vote) }}
      </div>
    </div>

    <h1>5. アンケート / Questionnaire</h1>
    <div class="checkdescriptin">
      {{ getFree() }}
    </div>
  </div>
</template>

<script>
import Title from "../components/Title";
export default {
  name: "CheckView",
  components: { Title },
  props: {
    votes: [],
    freeDescription: String,
  },
  data() {
    return {};
  },
  methods: {
    getBoolString: function (val) {
      return val ? "はい YES" : "いいえ NO";
    },
    getFree: function (val) {
      if (this.freeDescription) {
        return this.freeDescription;
      } else {
        return "記入なし / No Content";
      }
    },
  },
};
</script>

<style lang="scss" scoped>
p {
  font-size: 20px;
}
h1 {
  font-size: 17px;
  text-align: left;
  margin-top: 35px;
}
.CheckView {
  margin-top: 10px;
  width: 100%;
  text-align: left;
  padding-bottom: 100px;
}
.checktitle {
  margin-top: 30px;
  font-weight: 700;
  font-size: 15px;
}
.checkdescriptin {
  margin-top: 5px;
}
</style>