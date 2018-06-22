import axios from 'axios'

export function fetchHi() {
  return axios.get('/hi').then(response => { return response.data }).catch(error => { /* console.error(error); */ return Promise.reject(error) })
}

export function fetchHiName(name) {
  return axios.get('/hi/' + name).then(response => { return response.data }).catch(error => { /* console.error(error); */ return Promise.reject(error) })
}
