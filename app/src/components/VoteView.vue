<template>
  <div class="VoteView">
    <Title
      title="title"
      url="example.com"
    />
    <div v-for="vote in this.votes.slice(0, 5)" :key="vote.id">
      <BoolVote
        :title="vote.title"
        :desc="vote.desc"
        :vote="vote.vote"
        :id="vote.id"
        @voted="voted"
        yes="信任する / Approve"
        no="信任しない / Disapprove"
      />
    </div>

    <Title
      title="title"
      url="example.com"
    />
    <div v-for="vote in this.votes.slice(5, 8)" :key="vote.id">
      <BoolVote
        :title="vote.title"
        :desc="vote.desc"
        :vote="vote.vote"
        :id="vote.id"
        @voted="voted"
        yes="承認する / Approve"
        no="承認しない / Disapprove"
      />
    </div>

    <Title
      title="3. 憲章改正について / Amendment of the constitution"
      url="example.com"
    />

    <div v-for="vote in this.votes.slice(8, 12)" :key="vote.id">
      <BoolVote
        :title="vote.title"
        :desc="vote.desc"
        :vote="vote.vote"
        :id="vote.id"
        @voted="voted"
        yes="改正に賛成する / Agree with the amendment"
        no="改正に反対する / Oppose the amendment"
      />
    </div>

    <Title
      title="title"
      url="example.com"
    />

    <div v-for="vote in this.votes.slice(12, 14)" :key="vote.id">
      <BoolVote
        :title="vote.title"
        :desc="vote.desc"
        :vote="vote.vote"
        :id="vote.id"
        @voted="voted"
        yes="採択に賛成する / Approve the adoption of the Statement"
        no="採択に反対する / Disapprove the adoption of the Statement"
      />
    </div>

    <FreeVote
      title="5. アンケート / Questionnaire"
      desc="desc"
      :text="freeDescription"
      @textUpdated="textUpdated"
    />
    <Button
      text="次へ / Continue"
      class="buttonn"
      :disable="isDisableNext"
      @click="donext"
      tagId="donext"
    />
  </div>
</template>

<script>
import BoolVote from "../components/BoolVote";
import FreeVote from "../components/FreeVote";
import Button from "../components/Button";
import Title from "../components/Title";

// @ is an alias to /src
export default {
  name: "VoteView",
  components: {
    BoolVote,
    FreeVote,
    Button,
    Title,
  },
  props: {
    votes: [],
    freeDescription: String,
  },
  data() {
    return {};
  },
  methods: {
    voted: function (val, index) {
      this.$emit("voted", val, index);
    },
    textUpdated: function (val) {
      this.$emit("freeDescriptionUpdated", val);
    },
    donext: function () {
      this.$emit("nextDidTap");
    },
  },
  computed: {
    isDisableNext: function () {
      console.log(this.votes);
      return this.votes.findIndex((x) => x.vote == null) != -1;

      return false;
      // return this.votes.findIndex((x) => (x.vote = null)) == -1;
    },
  },
};
</script>

<style lang="scss" scoped>
.VoteView {
  margin-top: 20px;
  width: 100%;
  gap: 1rem;
  overflow: scroll;
  padding-bottom: 100px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
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
.buttonn {
  margin-top: 16px !important;
  align-self: center;
  margin: 0;
}
</style>