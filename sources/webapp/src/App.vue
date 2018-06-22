<template>
  <div id="app">
    <img src="./assets/logo.png">
    <b-nav justified tabs>
      <b-nav-item v-bind:to="'/'">Hello</b-nav-item>
      <b-nav-item v-bind:to="'hi'">Hi</b-nav-item>
      <b-nav-item v-bind:to="'bye'">Bye</b-nav-item>
      <b-nav-item v-bind:to="'404'">Not Found</b-nav-item>
    </b-nav>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
