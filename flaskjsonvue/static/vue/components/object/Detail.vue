<script setup>
  import { computed } from '@vue/reactivity';
import { onMounted, ref } from 'vue'

  // declare props
  const props = defineProps({
    objType: String,
    objId: {type: Number, default: null}
  })

  // reactive state
  const obj = ref({});
  const schema = ref({});
  const loadedObject = ref(false);
  const loadedSchema = ref(false);

  // functions that mutate state and trigger updates
  /**
   * fetch detail json schema for object type, store in schema and set loadedSchema value
   */
  async function getObjectDetailSchema() {
    const gResponse = await fetch("http://0.0.0.0:5000/api/v1/" + props.objType + "/schema/detail.schema.json");
    if(gResponse.status == 200) {
      schema.value = await gResponse.json();
      loadedSchema.value = true;
    } else {
      // TODO: Error handling
      console.error("Couldn't get object schema.");
    }
  }

  async function addObject() {
    const gResponse = await fetch("http://0.0.0.0:5000/api/v1/" + props.objType + "/add", {
      method: "POST",
      headers:{
        "Content-Type":"application/json"
      },
      body: JSON.stringify(obj.value)
    });
    const response = await gResponse.json();
    if(gResponse.status == 201) {
        // show success message
        obj.value = response.objects[0];
        this.errors = [];
      } else {
        this.errors = response.errors;
        console.error(`Couldn't add ${props.objType}!`)
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
      return "datetime-local";
    }

    // fallback to text
    return "text";
  }

  // lifecycle hooks
  onMounted(() => {
    console.log(`Initial log message.`, props.objType, props.objId);
    getObjectDetailSchema();
    if (loadedSchema) {
      console.log(`Successfuly loaded ${props.objType} schema.`)
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
    <template v-for="(prop, name, index) in schema.properties" :key="index" class="row">
      <div v-if="name != 'id'" class="row">
        <div class="col">
          <label :for="`${props.objType}-prop-${name}`">{{ name }}</label>
          <input v-model="obj[name]" :id="`${props.objType}-prop-${name}`" :type="getInputType(prop)">
        </div>
      </div>
    </template>
    <div v-if="obj.id" class="row">
      <!-- TODO: update object -->
    </div>
    <div v-else>
      <button @click="addObject(obj)" type="button" class="btn btn-outline-primary">Add new {{ this.objType }}</button>
    </div>
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
