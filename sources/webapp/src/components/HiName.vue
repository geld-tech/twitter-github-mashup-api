<template>
  <div class="hi">
    <h1>{{ msg }}</h1>
    <h2>{{ greetings }}</h2>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group id="inputGroup"
                    label="Your Name:"
                    label-for="inputName">
        <b-form-input id="inputName"
                      type="text"
                      v-model="form.name"
                      required
                      placeholder="Enter name">
        </b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
  </div>
</template>

<script>
import { fetchHi, fetchHiName } from '@/api'

export default {
  name: 'HiName',
  data() {
    return {
      msg: 'Hi',
      greetings: 'there',
      form: {
        name: ''
      },
      show: true
    }
  },
  methods: {
    getHi() {
      fetchHi().then(response => { this.greetings = response.data })
    },
    onSubmit(evt) {
      evt.preventDefault()
      fetchHiName(this.form.name).then(response => { this.greetings = response.data })
    },
    onReset(evt) {
      evt.preventDefault()
      /* Reset our form values */
      this.form.name = ''
      this.greetings = ''
      /* Trick to reset/clear native browser form validation state */
      this.show = false
      this.$nextTick(() => { this.show = true })
    }
  },
  created() {
    this.getHi()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
