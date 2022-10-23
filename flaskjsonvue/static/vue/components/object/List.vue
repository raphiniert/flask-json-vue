<script setup>
  import { computed, onMounted, ref } from 'vue'
  // import object store
  import useObjectStore from '../../stores/object'

  // import alert display component
  import alertDisplay from '../alert/display.vue'


  const store = useObjectStore()

  // declare props
  const props = defineProps({
    objType: String
  })

  // reactive state
  // tbd.

  // lifecycle hooks
  onMounted(() => {
    console.log(`Initial log message.`);
  })
</script>

<template>
  <h1>{{ props.objType }} list component</h1>
  <template v-if="!store.loadingObjects">
    <alertDisplay alert-type="danger" :obj-type="`${props.objType}`" :alerts="store.alertMessages.errors"></alertDisplay>
    <alertDisplay alert-type="warning" :obj-type="`${props.objType}`" :alerts="store.alertMessages.warnings"></alertDisplay>
    <alertDisplay alert-type="success" :obj-type="`${props.objType}`" :alerts="store.alertMessages.success"></alertDisplay>
    <alertDisplay alert-type="info" :obj-type="`${props.objType}`" :alerts="store.alertMessages.infos"></alertDisplay>
    <div :class="`list-container ${props.objType}`">
      <div v-for="(obj, index) in store.objectList"  :key="index" class="row">
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
          <button @click="store.deleteObject(obj.data.id)" type="button" class="btn btn-outline-danger">
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
