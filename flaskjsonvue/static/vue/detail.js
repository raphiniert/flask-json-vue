import {createApp} from 'vue';
import ObjectDetail from './components/object/Detail.vue';

const app = createApp({})
app.component('detail-component', ObjectDetail)
app.mount('#app')
