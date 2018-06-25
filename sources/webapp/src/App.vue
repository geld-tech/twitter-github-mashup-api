<template>
  <div id="app">
    <!-- Navigation -->
    <b-navbar class="navbar navbar-expand-lg navbar-light bg-white fixed-top">
      <b-navbar-brand href="/">
        <img src="/static/images/geld.tech_32x32.png" width="30" height="30" alt="" />__PACKAGE_NAME__
      </b-navbar-brand>
      <b-navbar-nav class="ml-auto">
        <b-nav-form @submit="onSubmit" @reset="onReset">
          <b-form-input id="searchInput" class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search"></b-form-input>
          <b-button class="my-2 my-sm-0" variant="primary" type="submit">Search</b-button>
        </b-nav-form>
      </b-navbar-nav>
    </b-navbar>
    <!-- Container -->
    <b-container class="bv-example-row">
        <b-row align-v="start">
            <b-col>Twitter</b-col>
            <b-col>GitHub</b-col>
        </b-row>
    </b-container>
  </div>
</template>

<script>
import { fetchData } from '@/api'

export default {
  name: 'App',
  data() {
    return {
      data: [],
      projects: [],
      tweets: [],
      show: true
    }
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault()
      fetchData(this.form.name).then(response => { this.data = response.data })
    },
    onReset(evt) {
      evt.preventDefault()
      /* Reset our form values */
      this.form.name = ''
      this.data = ''
      /* Trick to reset/clear native browser form validation state */
      this.show = false
      this.$nextTick(() => { this.show = true })
    }
  }
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
  padding-top: 70px;
}
</style>
