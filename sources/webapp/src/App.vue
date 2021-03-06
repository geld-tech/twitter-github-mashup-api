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
    <!-- Alerting -->
    <div class="alerting col-md-4 col-md-offset-4">
      <b-alert :show="dismissCountDown" dismissible variant="danger" @dismissed="error=''" @dismiss-count-down="countDownChanged">
        <p>{{ error }}</p>
      </b-alert>
    </div>
    <!-- Container -->
    <b-container class="bv-example-row">
        <b-row align-v="start" align-h="around">
            <b-col sm="4">
                <h4>GitHub Projects</h4>
                <div v-if="loading" class="loading">
                  <img src="/static/images/spinner.gif" width="32" height="32"/>
                </div>
                <div v-else>
                    <ul id="projects" class="list-no-bullet">
                      <li v-for="(index, item) in data" v-bind:key="index">
                        <p v-if="data[item].length > 0"><a href="#" v-on:click="selectProject(item)">{{ item }}</a><br /><small>({{ data[item].length }} tweets)</small></p>
                        <p v-else>{{ item }}<br /><small>(no tweets)</small></p>
                      </li>
                    </ul>
                </div>
            </b-col>
            <b-col sm="4">
                <h4>Twitter Mentions</h4>
                <ul id="tweets" class="list-no-bullet">
                  <li v-if="show" v-for="(tweet, index) in tweets" v-bind:key="index" v-on:delete-row="deleteThisRow(index)">
                    <Tweet :id="tweet.id_str">
                      <div class="spinner">
                        <p><small><strong>{{ tweet.user_name }}</strong> {{ tweet.text }}</small></p>
                      </div>
                    </Tweet>
                  </li>
                </ul>
            </b-col>
        </b-row>
    </b-container>
  </div>
</template>

<script>
import { fetchData } from '@/api'
import { Tweet } from 'vue-tweet-embed'

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
      dismissCountDown: 0,
      error: '',
      show: true
    }
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault()
      var searchKeyword = this.sanitizeString(this.form.keyword)
      this.form.keyword = ''
      this.loading = false
      this.dismissCountDown = 0
      this.error = ''
      if (searchKeyword !== '') {
        /* Trick to reset/clear native browser form validation state */
        this.selected = ''
        this.data = []
        this.show = false
        this.$nextTick(() => { this.show = true })
        /* Fetching the data */
        this.loading = true
        fetchData(searchKeyword)
          .then(response => {
            this.data = response.data
            this.loading = false
          })
          .catch(err => {
            this.error = err.message
            this.loading = false
            this.dismissCountDown = 6
          })
      }
    },
    onReset(evt) {
      evt.preventDefault()
      /* Reset our form values */
      this.form.keyword = ''
      this.selected = ''
      this.data = []
      this.loading = false
      /* Trick to reset/clear native browser form validation state */
      this.show = false
      this.$nextTick(() => { this.show = true })
    },
    sanitizeString(input) {
      input = input.trim()
      input = input.replace(/[`~!$%^&*|+?;:'",\\]/gi, '')
      input = input.replace('/', '')
      input = input.trim()
      return input
    },
    selectProject(project) {
      if (this.selected === project) {
        this.selected = ''
      } else {
        this.selected = ''
        this.show = false
        this.$nextTick(() => { this.show = true })
        this.selected = project
      }
      return true
    },
    countDownChanged (dismissCountDown) {
      this.dismissCountDown = dismissCountDown
    }
  },
  computed: {
    tweets: function () {
      var mentions = []
      if (this.selected !== '') {
        for (var i = 0, len = this.data[this.selected].length; i < len; i++) {
          mentions.push({
            id: this.data[this.selected][i]['id'],
            id_str: this.data[this.selected][i]['id_str'],
            created_at: this.data[this.selected][i]['created_at'],
            text: this.data[this.selected][i]['text'],
            user_name: this.data[this.selected][i]['user']['name'],
            user_desc: this.data[this.selected][i]['user']['description'],
            user_image: this.data[this.selected][i]['user']['profile_background_image_url_https']
          })
        }
      }
      return mentions
    }
  },
  components: {
    Tweet
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
  margin-bottom: 10px;
  padding-bottom: 20px;
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
    margin-bottom: 10px;
    padding-top: 170px;
    font-size: 14px;
  }
}
.alerting {
  margin: 0 auto;
  text-align: center;
  display: block;
  line-height: 15px;
}
.loading {
  width: 50%;
  margin: 0;
  padding-top: 40px;
  padding-left: 40px;
}
.list-no-bullet {
  padding: 0;
  margin: 0;
  list-style-type: none;
}
</style>
