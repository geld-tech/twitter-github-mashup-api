import axios from 'axios'

export function fetchData(name) {
  return axios.get('/projects/' + name).then(response => { return response.data }).catch(error => { /* console.error(error); */ return Promise.reject(error) })
}
