<template>
  <div class="boolvote">
    <div class="votetitle">{{ title }}</div>
    <div class="desc">{{ desc }}</div>
    <div class="voteButtons" :id="`vote_buttons${id}`">
      <div
        class="voteButton"
        :class="{ selected: voteBool(true) }"
        @click="voteDidTap(true)"
      >
        {{ this.yes }}
      </div>
      <div
        class="voteButton"
        :class="{ selected: voteBool(false) }"
        @click="voteDidTap(false)"
      >
        {{ this.no }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BoolVote",
  components: {},
  props: {
    title: String,
    desc: String,
    vote: Boolean | null,
    id: Number,
    yes: String,
    no: String,
  },
  data() {
    return {};
  },
  methods: {
    voteBool: function (val) {
      if (this.vote != null) {
        return this.vote == val;
      } else {
        return false;
      }
    },
    voteDidTap: function (val) {
      this.$emit("voted", val, this.id);
    },
  },
};
</script>

<style lang="scss" scoped>
.boolvote {
  .votetitle {
    font-size: 16px;
    font-weight: 700;
    text-align: left;
  }
  .desc {
    text-align: left;
  }
}
.voteButtons {
  display: flex;
  margin-top: 16px;
  .voteButton {
    cursor: pointer;
    border-radius: 5px;
    transition: 0.3s;
    width: 50%;
    min-height: 50px;
    border: 1px solid $green;
    font-weight: 700;
    background: white;
    color: $green;
    display: flex;
    justify-content: center;
    align-items: center;
    &:first-child {
      margin-right: 32px;
    }
    @media (hover: hover) {
    }
  }
  .selected {
    background: #e2ffdd;
  }
}
</style>