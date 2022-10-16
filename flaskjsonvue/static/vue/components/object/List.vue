<script setup>
import { computed, onMounted, ref } from 'vue'

// declare props
const props = defineProps({
  objType: String
})

// reactive state
const objectList = ref([]);
const loadedObjects = ref(false);
const errors = ref([])
const warnings = ref([])
const success = ref([])
const infos = ref([])

// functions that mutate state and trigger updates
async function getObjectList() {
  const gResponse = await fetch(`http://0.0.0.0:5000/api/v1/${props.objType}/list`);
  if(gResponse.status == 200) {
    objectList.value = await gResponse.json();
    loadedObjects.value = true;
  } else {
    // TODO: Error handling
    console.error("Couldn't get object list.");
  }
}

async function deleteObject(obj) {
  const gResponse = await fetch(`http://0.0.0.0:5000/api/v1/${props.objType}/delete`, {
    method: "DELETE",
    headers:{
      "Content-Type":"application/json"
    },
    body: JSON.stringify(obj.data)
  });
  const response = await gResponse.json();
  if(gResponse.status == 200) {
    getObjectList()
    errors.value = response.errors
    warnings.value = response.warnings
    success.value = response.success
    infos.value = response.infos
  } else {

    console.error(`Couldn't delete ${props.objType} with id: ${obj.data.id}!`)
  }
}

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
    <div v-if="errors.length" class="alert alert-danger alert-dismissible fade show" role="alert">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/>
      </svg>
      <ul class="mb-0 d-inline-block">
        <li v-for="error in errors">
          <a :href="`#${props.objType}-prop-${error.field}`" class="alert-link">{{ error.field }}</a>: {{ error.message }}
        </li>
      </ul>
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <div v-if="warnings.length" class="alert alert-warning alert-dismissible fade show" role="alert">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
        <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
      </svg>
      <ul class="mb-0 d-inline-block">
        <li v-for="message in warnings">
          {{ message }}
        </li>
      </ul>
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <div v-if="success.length" class="alert alert-success alert-dismissible fade show" role="alert">
      <svg class="pt-0" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
      </svg>
      <ul class="mb-0 d-inline-block">
        <li v-for="message in success">
          {{ message }}
        </li>
      </ul>
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <div v-if="infos.length" class="alert alert-info alert-dismissible fade show" role="alert">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
        <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
      </svg>
      <ul class="mb-0  d-inline-block">
        <li v-for="message in infos">
          {{ message }}
        </li>
      </ul>
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    <div :class="`list-container ${props.objType}`">
      <div v-for="(obj, index) in objectList"  :key="index" class="row">
        <div class="col">
          {{ obj.meta.display_name }}
        </div>
        <div class="col">
          <a :href="`/${props.objType}/update/${obj.data.id}`" class="btn btn-outline-secondary">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
              <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
              <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"/>
            </svg>
          </a>
        </div>
        <div class="col">
          <button @click="deleteObject(obj)" type="button" class="btn btn-outline-danger">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-basket-fill" viewBox="0 0 16 16">
              <path d="M5.071 1.243a.5.5 0 0 1 .858.514L3.383 6h9.234L10.07 1.757a.5.5 0 1 1 .858-.514L13.783 6H15.5a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-.5.5H15v5a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V9H.5a.5.5 0 0 1-.5-.5v-2A.5.5 0 0 1 .5 6h1.717L5.07 1.243zM3.5 10.5a.5.5 0 1 0-1 0v3a.5.5 0 0 0 1 0v-3zm2.5 0a.5.5 0 1 0-1 0v3a.5.5 0 0 0 1 0v-3zm2.5 0a.5.5 0 1 0-1 0v3a.5.5 0 0 0 1 0v-3zm2.5 0a.5.5 0 1 0-1 0v3a.5.5 0 0 0 1 0v-3zm2.5 0a.5.5 0 1 0-1 0v3a.5.5 0 0 0 1 0v-3z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
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
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p>
          Loading {{ props.objType }} list view.
        </p>
      </div>
    </div>
  </template>
</template>
