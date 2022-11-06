import {createRouter, createWebHashHistory} from 'vue-router';
import ObjectList from '../components/object/List.vue';
import ObjectDetail from '../components/object/Detail.vue';

// 1. Define route components.
// These can be imported from other files
const Home = { template: '<div>Home</div>' }

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
// TODO: call endpoint with objtypes,

const routes = [
  // will match everything and put it under `$route.params.pathMatch`
  { name: 'root', path: '/', component: Home },
  { name: 'list', path: '/:objtype(demo|address)', component: ObjectList },
  { name: 'add', path: '/:objtype(demo|address)/add', component: ObjectDetail },
  { name: 'update', path: '/:objtype(demo|address)/update/:id', component: ObjectDetail },
]

// 3. Create the router instance and pass the `routes` option
// You can pass in additional options here, but let's
// keep it simple for now.
const router = createRouter({
  // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
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
