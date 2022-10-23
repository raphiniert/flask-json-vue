import {createApp} from 'vue';
import {createPinia} from 'pinia';
import ObjectList from './components/object/List.vue';
import useObjectStore from './stores/object'

const pinia = createPinia()


const app = createApp({})
app.use(pinia)
app.component('list-component', ObjectList)
app.mount('#app')

const objectStore = useObjectStore()
objectStore.getObjectList()
