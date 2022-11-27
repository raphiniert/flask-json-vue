<script setup>
  import { computed, onMounted, ref } from 'vue'

  // import object store
  import useObjectStore from '../../stores/object'
  const store = useObjectStore()

  const props = defineProps({
    modelValue: {
      type: Number,
      default: null
    },
    objType: String,
    propertyName: String,
    hasError: {
      type: Boolean,
      default: false
    },
    validated: {
      type: Boolean,
      default: false
    }
  })

  const emit = defineEmits(['update:modelValue'])

  const computedRelationId = computed({
    get() {
      return props.modelValue !== null ? parseInt(props.modelValue) : null
    },
    set(value) {
      emit('update:modelValue', value !== null ? parseInt(value) : null)
    }
  })

  function validClass() {
    if(!props.validated) {
      return ""
    }
    if (props.hasError) {
      return "is-invalid";
    }
    return "is-valid";
  }

  // lifecycle hooks
  onMounted(() => {
    store.getObjectList(props.objType)
    emit('update:modelValue', computedRelationId.value)
  })

</script>

<template>
  <template v-if="store.objects[props.objType]?.loaded">
    <div :class="`select-related-list ${props.objType}`">
      <select v-model="computedRelationId" :id="`${props.objType}-prop-${props.propertyName}`" :class="`form-control ${validClass()}`" :aria-label="`Select ${props.objType}`" required>
        <option value="null">No {{ props.objType }}</option>
        <option v-for="(obj, index) in store.objects[props.objType]?.list" :key="index" :value="`${obj.data.id}`">
          {{ obj.meta.display_name }}
        </option>
      </select>
    </div>
  </template>
  <template v-else>
    <div>Couldn't fetch {{ props.objType }} list</div>
  </template>
</template>
