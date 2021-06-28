<template>
  <div class="chat-footer">
    <textarea placeholder="Type a message" v-model="message"></textarea>
    <button v-on:click="$emit('send', message)">Send</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: "",
    };
  },
  emits: ["send"],
};
</script>

<style>
</style>