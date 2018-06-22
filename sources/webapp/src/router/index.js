import Vue from 'vue'
import Router from 'vue-router'

import HelloWorld from '@/components/HelloWorld'
import HiName from '@/components/HiName'
import GoodBye from '@/components/GoodBye'
import NotFound from '@/components/NotFound'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/hi',
      name: 'HiName',
      component: HiName
    },
    {
      path: '/bye',
      name: 'GoobBye',
      component: GoodBye
    },
    {
      path: '/404',
      name: '404',
      component: NotFound
    },
    {
      path: '*',
      redirect: '/404'
    }
  ]
})
