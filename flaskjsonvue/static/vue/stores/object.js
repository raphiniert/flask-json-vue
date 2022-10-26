// stores/object.js
import { defineStore } from 'pinia'
import { useRoute } from 'vue-router'

export default defineStore('object', {
    state: () => {
      return {
        count: 0,
        objType: 'demo',
        activeObjId: null,
        objectList: [],
        loadingObjects: true,
        alertMessages: {
            errors: [],
            warnings: [],
            success: [],
            infos: []
        }
     }
    },
    // could also be defined as
    // state: () => ({ count: 0 })
    getters: {
    },
    actions: {
      increment() {
        this.count++
      },
      activeObj(objId) {
        return this.objectList.find(element => element.data.id == objId)
      },
      async getObjectList() {
        const route = useRoute()
        const gResponse = await fetch(`http://0.0.0.0:5000/api/v1/${route.params.objtype}/list`);
        if(gResponse.status == 200) {
          this.$patch({
            objectList: await gResponse.json(),
            loadingObjects: false
          })
        } else {
          // TODO: Error handling
          console.error("Couldn't get object list.");
        }
      },
      async deleteObject(objId) {
        console.log("objId", objId)
        console.log("this.activeObj", this.activeObj(objId))
        const gResponse = await fetch(`http://0.0.0.0:5000/api/v1/${this.objType}/delete`, {
          method: "DELETE",
          headers:{
            "Content-Type":"application/json"
          },
          body: JSON.stringify(this.activeObj(objId).data)
        });
        const response = await gResponse.json();
        if(gResponse.status == 200) {
          this.getObjectList()
          this.$patch({ alertMessages: {
                errors: response.errors,
                warnings: response.warnings,
                success: response.success,
                infos: response.infos
            }
          })
        } else {
          console.error(`Couldn't delete ${this.objType} with id: ${objId}!`)
        }
      }
    }
})
