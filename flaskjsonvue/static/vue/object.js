import {createApp} from 'vue';
import {createPinia} from 'pinia';
import router from './router';


const pinia = createPinia()
const app = createApp({})
// Make sure to _use_ the router instance to make the
// whole app router-aware.
app.use(router)
app.use(pinia)
app.mount('#app')
