import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    projectInfo: {
      "name": "",
      "describe": '',
      "labels": [

      ],
      "z_order": false,
    },
    allFileList: [],
    image_quality: 70
  },
  mutations: {
    addToStore(state, labData){
      state.projectInfo.labels = labData
    },
    addImageQuality(state, image_quality){
      state.image_quality = image_quality
    },
    cleanStore(){
      this.state.projectInfo = {
        "name": "",
        "describe": '',
        "labels": [

        ],
        "z_order": false,
      }
      this.state.image_quality = 70
    },
    cleanFileList(){
      this.state.allFileList = []
    },
    saveFileList(state, listData){
      state.allFileList = listData
    }
  },
  actions: {
  },
  modules: {
  }
})
