<template>
  <div
    class="buttoncomponent"
    @click="click"
    :class="{ disabled: disable }"
    :id="this.tagId"
  >
    {{ text }}
  </div>
</template>

<script lang="ts">
import { defineComponent, toRefs } from "vue";

type Props = {
  text: string;
  disable: boolean;
  tagId: string | undefined;
};

export default defineComponent({
  props: {
    text: {
      type: String,
      required: true,
    },
    disable: {
      type: Boolean,
      required: false,
      default: false,
    },
    tagId: {
      type: String,
      required: false,
    },
  },

  emits: ["click"],
  setup(props: Props, context) {
    const { disable, tagId } = toRefs(props);
    console.log({ props });
    console.log({ id: props.tagId });
    const click = () => {
      if (!disable.value) {
        context.emit("click");
      }
    };

    return { click, disable, tagId };
  },
});
</script>

<style lang="scss" scoped>
.buttoncomponent {
  cursor: pointer;
  border-radius: 5px;
  transition: 0.3s;
  width: 144px;
  height: 50px;
  border: 1px solid $green;
  line-height: 50px;
  font-weight: 700;
  background: white;
  color: $green;
  @media (hover: hover) {
    &:hover {
      background: #e2ffdd;
    }
  }
}
.disabled {
  pointer-events: none;
  color: #c4c4c4;
  border-color: #c4c4c4;
}
</style>
