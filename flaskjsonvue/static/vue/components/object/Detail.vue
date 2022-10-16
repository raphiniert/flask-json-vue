<script setup>
  import { computed, onMounted, ref } from 'vue'
  // import custom date-time input component
  import DateTimeInput from '../input/datetime.vue'

  // declare props
  const props = defineProps({
    objType: String,
    objId: {type: Number, default: null}
  })

  // reactive state
  const obj = ref({});
  const errors = ref([])
  const schema = ref({});
  const loadedObject = ref(false);
  const loadedSchema = ref(false);
  const validated = ref(false);

  function formSubmit(){
    if(loadedObject.value) {
      updateObject()
    } else {
      addObject()
    }
    validated.value = true
  }

  // functions that mutate state and trigger updates
  /**
   * fetch detail json schema for object type, store in schema and set loadedSchema value
   */
  async function getObjectDetailSchema() {
    const gResponse = await fetch(`http://0.0.0.0:5000/api/v1/${props.objType}/schema/detail.schema.json`);
    if(gResponse.status == 200) {
      schema.value = await gResponse.json();
      loadedSchema.value = true;
    } else {
      // TODO: Error handling
      console.error("Couldn't get object schema.");
    }
  }

  /**
   * post new objType object, store data in obj on success
   */
  async function addObject() {
    const gResponse = await fetch(`http://0.0.0.0:5000/api/v1/${props.objType}/add`, {
      method: "POST",
      headers:{
        "Content-Type":"application/json"
      },
      body: JSON.stringify(obj.value)
    });
    const response = await gResponse.json();
    if(gResponse.status == 201) {
      // show success message
      obj.value = response.objects[0].data;
      window.location = `http://0.0.0.0:5000/${props.objType}/update/${obj.value.id}`
    } else {
      errors.value = response.errors
      console.error(`Couldn't add ${props.objType}!`)
    }
  }

  /**
   * fetch object with prop objId
   */
  async function getObject() {
    const gResponse = await fetch(`http://0.0.0.0:5000/api/v1/${props.objType}/get/${props.objId}`);
    const response = await gResponse.json();
    if(gResponse.status == 200) {
      obj.value = response.objects[0].data;
      loadedObject.value = true;
    } else {
      console.error(`Couldn't get ${props.objType} with id: ${props.objId}!`)
    }
  }

  /**
   * patch object, store data in obj on success
   */
  async function updateObject() {
    const gResponse = await fetch(`http://0.0.0.0:5000/api/v1/${props.objType}/update`, {
      method: "PATCH",
      headers:{
        "Content-Type":"application/json"
      },
      body: JSON.stringify(obj.value)
    });
    const response = await gResponse.json();
    if(gResponse.status == 200) {
      // show success message
      obj.value = response.objects[0].data;
      errors.value = []
    } else {
      errors.value = response.errors;
      console.error(`Couldn't update ${props.objType} with id: ${props.objId}!`)
    }
  }

  /**
   * delete object set window location to objType route
   */
  async function deleteObject() {
    const gResponse = await fetch(`http://0.0.0.0:5000/api/v1/${props.objType}/delete`, {
      method: "DELETE",
      headers:{
        "Content-Type":"application/json"
      },
      body: JSON.stringify(obj.value)
    });
    const response = await gResponse.json();
    if(gResponse.status == 200) {
      window.location = `http://0.0.0.0:5000/${props.objType}`;
    } else {
      console.error(`Couldn't delete ${props.objType} with id: ${props.objId}!`)
    }
  }

  /**
   * @param {Object} prop - json schema property inlcuding type, descirption and optional format info
   */
  function getInputType(property) {
    // get type or format defined in json schema
    let jsonSchemaType = property.type
    if ('format' in property) {
      jsonSchemaType = property.format
    }

    if (jsonSchemaType.includes("integer") || jsonSchemaType.includes("number")) {
      return "number";
    } else if (jsonSchemaType.includes("date-time")) {
      return "datetime";
    }

    // fallback to text
    return "text";
  }

  function isRequired(propertyName) {
    if (loadedSchema) {
      return schema.value.required.includes(propertyName);
    }
    return false;
  }

  function hasError(propertyName) {
    // iterate errors array
    return errors.value.some(element => {
      if(element.field == propertyName){
        return true;
      }
    });
  }

  function getErrorMessages(propertyName) {
    const errorMessages = []
    errors.value.find(element => {
      if(element.field == propertyName){
        errorMessages.push(element.message)
      }
    });
    return errorMessages
  }

  function validClass(name) {
    if(!validated.value) {
      return ""
    }
    if (hasError(name)) {
      return "is-invalid";
    }
    return "is-valid";
  }

  // lifecycle hooks
  onMounted(() => {
    console.log(`Initial log message.`, props.objType, props.objId);
    getObjectDetailSchema();
    if (loadedSchema) {
      console.log(`Successfuly loaded ${props.objType} schema.`)
    }
    if (props.objId) {
      getObject();
      if (loadedObject) {
        console.log(`Successfuly loaded ${props.objType} object.`)
      }
    }
  })
</script>

<template>
  <h1>{{ props.objType }} detail component</h1>
  <template v-if="loadedSchema">
    <h2>{{ schema.title }}</h2>
    <div class="row">
      <div class="col">
        {{ schema.description }}
      </div>
    </div>
    <!-- do not display id property -->
    <form @submit.prevent="formSubmit()" class="needs-validation" novalidate>
      <template v-for="(prop, name, index) in schema.properties" :key="index" class="row">
        <div v-if="name != 'id'" class="row">
          <div v-if="getInputType(prop) == 'datetime'" class="col">
            <DateTimeInput v-model="obj[name]" :propertyName="name" :objType="props.objType" :hasError="hasError(name)" :validated="validated"/>
          </div>
          <div v-else-if="getInputType(prop) == 'number'" class="col form-group has-validation">
            <label :for="`${props.objType}-prop-${name}`">{{ name }}</label>
            <input v-model="obj[name]" :id="`${props.objType}-prop-${name}`" type="number" :class="`form-control ${validClass(name)}`" step="0.000001" :required="isRequired(name)">
            <div class="invalid-feedback" v-if="hasError(name)">
              <ul v-for="(message, index) in getErrorMessages(name)" :key="index">
                <li>{{ message }}</li>
              </ul>
            </div>
          </div>
          <div v-else class="col form-group has-validation">
            <label :for="`${props.objType}-prop-${name}`">{{ name }}</label>
            <input v-model="obj[name]" :id="`${props.objType}-prop-${name}`" :type="getInputType(prop)" :class="`form-control ${validClass(name)}`" :required="isRequired(name)">
            <div class="invalid-feedback" v-if="hasError(name)">
              <ul v-for="(message, index) in getErrorMessages(name)" :key="index">
                <li>{{ message }}</li>
              </ul>
            </div>
          </div>
        </div>
      </template>
      <div v-if="loadedObject" class="row">
        <!-- TODO: update object -->
        <button class="btn btn-outline-secondary">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16">
            <path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708l-3-3zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207l6.5-6.5zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.499.499 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11l.178-.178z"/>
          </svg>
          <span> Edit</span>
        </button>
        <button class="btn btn-outline-danger" @click="deleteObject()" type="button">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-basket-fill" viewBox="0 0 16 16">
            <path d="M5.071 1.243a.5.5 0 0 1 .858.514L3.383 6h9.234L10.07 1.757a.5.5 0 1 1 .858-.514L13.783 6H15.5a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-.5.5H15v5a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V9H.5a.5.5 0 0 1-.5-.5v-2A.5.5 0 0 1 .5 6h1.717L5.07 1.243zM3.5 10.5a.5.5 0 1 0-1 0v3a.5.5 0 0 0 1 0v-3zm2.5 0a.5.5 0 1 0-1 0v3a.5.5 0 0 0 1 0v-3zm2.5 0a.5.5 0 1 0-1 0v3a.5.5 0 0 0 1 0v-3zm2.5 0a.5.5 0 1 0-1 0v3a.5.5 0 0 0 1 0v-3zm2.5 0a.5.5 0 1 0-1 0v3a.5.5 0 0 0 1 0v-3z"/>
          </svg>
          <span> Delete</span>
        </button>
      </div>
      <div v-else>
        <button class="btn btn-outline-primary">Add new {{ this.objType }}</button>
      </div>
    </form>
  </template>
  <template v-else>
    <div class="row">
      <div class="col">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p>
          Loading {{ props.objType }} detail view.
        </p>
      </div>
    </div>
  </template>
</template>
