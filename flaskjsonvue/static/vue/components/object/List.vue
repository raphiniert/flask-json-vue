<script setup>
import { computed, onMounted, ref } from 'vue'

// declare props
const props = defineProps({
  objType: String
})

// reactive state
const objectList = ref([]);
const loadedObjects = ref(false);

// functions that mutate state and trigger updates
async function getObjectList() {
  const gResponse = await fetch("http://0.0.0.0:5000/api/v1/" + props.objType + "/list");
  if(gResponse.status == 200) {
    objectList.value = await gResponse.json();
    loadedObjects.value = true;
  } else {
    // TODO: Error handling
    console.error("Couldn't get object list.");
  }
}

// const add_url = computed(() => {
//   return `/${props.objType}/add`;
// })

// lifecycle hooks
onMounted(() => {
  console.log(`Initial log message.`, loadedObjects.value);
  getObjectList();
  console.log(objectList.value, loadedObjects.value);
})
</script>

<template>
  <h1>{{ props.objType }} list component</h1>
  <template v-if="loadedObjects">
    <a :href="`/${props.objType}/add`" class="btn btn-outline-primary">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-square" viewBox="0 0 16 16">
        <path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"></path>
        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"></path>
      </svg>
      <span> Add {{ props.objType }}</span>
    </a>
  </template>
  <template v-else>
    <div class="row">
      <div class="col">
        <p>
          Not yet loaded...
        </p>
      </div>
    </div>
  </template>
</template>
