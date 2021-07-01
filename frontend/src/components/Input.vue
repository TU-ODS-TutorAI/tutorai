<template>
  <form class="chat-footer" v-on:submit.prevent="submit">
    <input type="text" placeholder="Type a message" v-model="message" />
  </form>
</template>

<script>
export default {
  data() {
    return {
      message: "",
    };
  },
  emits: ["send"],
  methods: {
    submit() {
      if (this.message.length > 0) {
        this.$emit("send", this.message);
        this.message = "";
      }
    },
  },
};
</script>

<style>
</style>