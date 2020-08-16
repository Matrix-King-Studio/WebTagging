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
    allFileList: []
  },
  mutations: {
    addToStore(state, labData){
      state.projectInfo.labels = labData
    },
    cleanStore(){
      this.state.projectInfo = {
        "name": "",
        "describe": '',
        "labels": [

        ],
        "z_order": false,
      }
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
