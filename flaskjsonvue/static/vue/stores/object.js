// stores/object.js
import { defineStore } from 'pinia'

export default defineStore('object', {
    state: () => {
      return {
        objects: {},
        alertMessages: {
            errors: [],
            warnings: [],
            success: [],
            infos: []
        }
     }
    },
    getters: {
    },
    actions: {
      increment() {
        this.count++
      },
      activeObj(objId, objType) {
        return this.objects[objType].list.find(element => element.data.id == objId)
      },
      async getObjectList(objType) {
        console.log(`Getting object list for: ${objType}.`)
        const gResponse = await fetch(`http://0.0.0.0:5000/api/v1/${objType}/list`);
        if(gResponse.status == 200) {
          this.$patch({
            objects: {
              [objType]: {
                list: await gResponse.json(),
                loaded: true
              }
            }
          });
          console.log(`Got ${this.objects}.`);
        } else {
          // TODO: Error handling
          console.error(`Couldn't get object list for ${objType}.`);
          this.$patch({ alertMessages: {
              errors: [`Couldn't get object list for ${objType}.`]
            }
          });
        }
      },
      async deleteObject(objId, objType) {
        const gResponse = await fetch(`http://0.0.0.0:5000/api/v1/${objType}/delete`, {
          method: "DELETE",
          headers:{
            "Content-Type":"application/json"
          },
          body: JSON.stringify(this.activeObj(objId, objType).data)
        });
        const response = await gResponse.json();
        if(gResponse.status == 200) {
          this.getObjectList(objType)
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
