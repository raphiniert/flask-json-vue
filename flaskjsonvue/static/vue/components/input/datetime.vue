<script setup>
  import { computed, onMounted } from 'vue'
  import { DateTime } from 'luxon'

  // custom date-time input component
  const name = "DateTimeInput";

  // declare props
  const props = defineProps({
    modelValue: {
      type: String,
      default: DateTime.now().toISO()
    },
    objType: String,
    propertyName: String
  })

  const emit = defineEmits(['update:modelValue'])

  // Luxon interprets the time as being specified with that offset,
  // but converts the resulting DateTime into the system's local zone
  // see https://moment.github.io/luxon/#/zones?id=strings-that-specify-an-offset
  // therefore, setZone: true must be specified to not alter the time part
  const computedDate = computed({
    get() {
      const dateTimeObj = DateTime.fromISO(props.modelValue, { setZone: true })
      // get the YYYY-mm-dd part
      return dateTimeObj.toISO().split("T")[0]
    },
    set(value) {
      emit('update:modelValue', `${value}T${computedTime.value}${computedOffset.value}`)
    }
  })

  const computedTime = computed({
    get() {
      const dateTimeObj = DateTime.fromISO(props.modelValue, { setZone: true })
      // get the HH:MM:ss.SSS part
      return dateTimeObj.toISO().split("T")[1].substring(0, 12)
    },
    set(value) {
      emit('update:modelValue', `${computedDate.value}T${value}${computedOffset.value}`)
    }
  })

  const computedOffset = computed({
    get() {
      const dateTimeObj = DateTime.fromISO(props.modelValue, { setZone: true })
      // get the +HH:MM part, set to +00:00 if it's UTC (Z)
      if(dateTimeObj.toISO().includes("Z")){
        return "+00:00"
      }
      return dateTimeObj.toISO().substring(dateTimeObj.toISO().length - 6)
    },
    set(value) {
      emit('update:modelValue', `${computedDate.value}T${computedTime.value}${value}`)
    }
  })

  // lifecycle hooks
  onMounted(() => {
    emit('update:modelValue', `${computedDate.value}T${computedTime.value}${computedOffset.value}`)
  })

</script>

<template>
  <div class="row">
    <div class="col">
      <label :for="`${props.objType}-prop-${props.propertyName}-date`">{{ props.propertyName }} date</label>
      <input v-model="computedDate" :id="`${props.objType}-prop-${props.propertyName}-date`" type="date">
    </div>
    <div class="col">
      <label :for="`${props.objType}-prop-${props.propertyName}-time`">{{ props.propertyName }} time</label>
      <input v-model="computedTime" :id="`${props.objType}-prop-${props.propertyName}-time`" step="0.001" type="time">
    </div>
    <div class="col">
      <label :for="`${props.objType}-prop-${props.propertyName}-offset`">{{ props.propertyName }} offset</label>
      <!-- TODO: complete list of 38 utc offsets -->
      <select v-model="computedOffset" :id="`${props.objType}-prop-${props.propertyName}-offset`">
        <option value="-02:00">-02:00</option>
        <option value="-01:00">-01:00</option>
        <option value="+00:00">+00:00</option>
        <option value="+01:00">+01:00</option>
        <option value="+02:00">+02:00</option>
      </select>
    </div>
  </div>
</template>
