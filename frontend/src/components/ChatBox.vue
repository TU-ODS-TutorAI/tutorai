<template>
  <div>
    <div class="container chat">
      <select class="form-select" v-model="selected">
        <option disabled value="">Please Select the Module Context</option>
        <option
          v-for="(item, index) in modules"
          :key="index"
          :value="item.number"
        >
          {{ item.title }}
        </option>
      </select>
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
      modules: [],
      selected: "",
    };
  },
  created() {
    axios({
      method: "GET",
      url: `http://tutorai.ddns.net:3000/moses`,
    }).then(
      (result) => {
        this.modules = result.data.modules.sort(function (a, b) {
          return ("" + a.title).localeCompare(b.title);
        });
      },
      (error) => {
        console.error(error);
      }
    );
  },
  methods: {
    sendRequest(message) {
      this.messages.push({ msg: message, right: true });
      axios({
        method: "GET",
        url: `http://tutorai.ddns.net:5000/tutorai/classic/${message.replace(
          "?",
          "%3F"
        )}/${this.selected}`,
      }).then(
        (result) => {
          this.messages.push({ msg: result.data.answer, right: false });
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