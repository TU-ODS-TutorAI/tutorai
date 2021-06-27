<template>
  <div>
    <div class="container chat">
      <div class="chat-box">
        <Message
          v-for="(item, index) in messages"
          :key="index"
          :msg="item.msg"
          :right="item.right"
        />
      </div>

      <Input v-on:send="sendRequest" />
    </div>
  </div>
</template>

<script>
import Message from "@/components/Message.vue";
import Input from "@/components/Input.vue";
import axios from "axios";

export default {
  components: {
    Message,
    Input,
  },
  data() {
    return {
      messages: [],
    };
  },
  methods: {
    sendRequest(message) {
      this.messages.push({ msg: message, right: true });
      console.log(this.messages);
      axios({
        method: "GET",
        url: "http://localhost:3000/moses/search/german.content",
        params: {
          q: message,
        },
      }).then(
        (result) => {
          this.messages.push({ msg: result, right: false });
          console.log(this.messages);
        },
        (error) => {
          console.error(error);
        }
      );
    },
  },
};
</script>

<style>
</style>