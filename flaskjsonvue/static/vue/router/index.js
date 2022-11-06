import {createRouter, createWebHashHistory} from 'vue-router';
import ObjectList from '../components/object/List.vue';
import ObjectDetail from '../components/object/Detail.vue';
import Home from '../views/Home.vue';
import NotFound from '../views/NotFound.vue';

// TODO: call endpoint with objtypes,
const routes = [
  // will match everything and put it under `$route.params.pathMatch`
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
  { name: 'root', path: '/', component: Home },
  { name: 'list', path: '/:objtype(demo|address)', component: ObjectList },
  { name: 'add', path: '/:objtype(demo|address)/add', component: ObjectDetail },
  { name: 'update', path: '/:objtype(demo|address)/update/:id', component: ObjectDetail },
]

// create the router instance and pass the `routes` option
const router = createRouter({
  // Provide the history implementation to use.
  history: createWebHashHistory(),
  routes, // short for `routes: routes`,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      }
    }
  },
})

export default router
