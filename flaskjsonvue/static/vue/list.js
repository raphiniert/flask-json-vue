import {createApp} from 'vue';
import ObjectList from './components/object/List.vue';

const app = createApp({})
app.component('list-component', ObjectList)
app.mount('#app')
