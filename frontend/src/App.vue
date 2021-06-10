<template>
  <div>
    <img alt="Vue logo" src="./assets/logo.png" />
    <HelloWorld msg="Welcome to Your Vue.js App" />
    <HelloWorld msg="Welcome to our Frontend" />
    <div class="container">
      <div class="chat">
        <div class="chat-box">
          <Message msg="Hi, Elias" right="true"/>
          <Message msg="Oh! hi" />
          <div class="chat-r">
            <div class="sp"></div>
            <div class="mess mess-r">
              <p>How are you doing?</p>
            </div>
          </div>
          <div class="chat-l">
            <div class="mess">
              <p>I'm doing alright. How about you?</p>
            </div>
            <div class="sp"></div>
          </div>

          <div class="chat-r">
            <div class="sp"></div>
            <div class="mess mess-r">
              <p>Not too bad. The weather is great isn't it?</p>
            </div>
          </div>

          <div class="chat-l">
            <div class="mess">
              <p>Yes. It's absolutely beautiful today.</p>
            </div>
            <div class="sp"></div>
          </div>
          <div class="chat-r">
            <div class="sp"></div>
            <div class="mess mess-r">
              <p>I wish it was like this more frequently.</p>
            </div>
          </div>
          <div class="chat-l">
            <div class="mess">
              <p>Me too.</p>
            </div>
            <div class="sp"></div>
          </div>
          <div class="chat-r">
            <div class="sp"></div>
            <div class="mess mess-r">
              <p>So where are you going now?</p>
            </div>
          </div>
        </div>

        <div class="chat-footer">
          <textarea placeholder="Type a message"></textarea>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";
import Message from "./components/Message.vue";

export default {
  name: "App",
  components: {
    HelloWorld,
    Message
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
