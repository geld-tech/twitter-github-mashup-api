<template>
  <div id="app">
    <!-- Navigation -->
    <b-navbar class="navbar-expand-lg navbar-light bg-white fixed-top" toggleable>
        <b-navbar-nav>
          <b-navbar-brand href="/"><img src="/static/images/geld.tech_32x32.png" width="30" height="30" alt="" /> __PACKAGE_NAME__</b-navbar-brand>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
            <b-nav-form @submit="onSubmit" @reset="onReset">
              <b-form-input id="searchInput" type="search"  v-model="form.keyword" class="form-control mr-sm-2 ml-auto" placeholder="" aria-label="Search"></b-form-input>
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
        <b-row align-v="start">
            <b-col>
                <div v-if="loading" class="loading">
                  <img src="../src/assets/spinner.gif" width="32" height="32"/>
                </div>
                <div v-else>
                    <ul id="projects">
                      <li v-for="(index, item) in data" v-bind:key="index">
                        <p v-if="data[item].length > 0"><a href="#" v-on:click="selected=item">{{ item }}</a> ({{ data[item].length }} tweets)</p>
                        <p v-else>{{ item }} (no tweets)</p>
                      </li>
                    </ul>
                </div>
            </b-col>
            <b-col>
                <ul id="tweets">
                  <li v-for="(text, index) in tweets" v-bind:key="index"><p>{{ text }}</p></li>
                </ul>
            </b-col>
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
      form: {
        keyword: ''
      },
      data: [],
      selected: '',
      loading: false,
      show: true
    }
  },
  methods: {
    onSubmit(evt) {
      this.loading = true
      evt.preventDefault()
      fetchData(this.form.keyword)
        .then(response => {
          this.data = response.data
          this.loading = false
        })
    },
    onReset(evt) {
      evt.preventDefault()
      /* Reset our form values */
      this.form.keyword = ''
      this.data = []
      this.selected = ''
      this.loading = false
      /* Trick to reset/clear native browser form validation state */
      this.show = false
      this.$nextTick(() => { this.show = true })
    }
  },
  computed: {
    tweets: function () {
      var mentions = []
      if (this.selected !== '') {
        for (var i = 0, len = this.data[this.selected].length; i < len; i++) {
          mentions.push(this.data[this.selected][i]['user']['name'] + ': ' + this.data[this.selected][i]['text'])
        }
      }
      return mentions
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 30px;
  padding-top: 50px;
}
@media screen and (min-width: 601px) {
  #app {
    margin-top: 5px;
    padding-top: 70px;
    font-size: 24px;
  }
}
@media screen and (max-width: 600px) {
  #app {
    margin-top: 15px;
    padding-top: 170px;
    font-size: 14px;
  }
}
.loading {
    width: 50%;
    margin: 0;
    padding-left: 20px;
}
</style>
