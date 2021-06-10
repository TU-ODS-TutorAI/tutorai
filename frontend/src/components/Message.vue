<template>
  <div v-if="this.right">
    <div class="chat-r">
      <div class="sp"></div>
      <div class="mess mess-r">
        <p>{{ msg }}</p>
      </div>
    </div>
  </div>
  <div v-else>
    <div class="chat-l">
      <div class="mess">
        <p>{{ msg }}</p>
      </div>
      <div class="sp"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Message",
  props: {
    msg: String,
    right: Boolean,
  },
};
</script>

<style>
</style>