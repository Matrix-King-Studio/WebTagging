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
    image_quality: 70,
    imageTags: {
      "shapes":[
      ],
      "tracks":[
      ],
      "tags":[
      ],
      "version":26
    }
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
    },
    saveTagsInfo(state, shapes) {
      console.log('开始保存新的矩形框信息');
      for(let item in shapes.rectangles){
        console.log('正在保存第'+shapes.rectangles[item].index+'个矩形框的信息')
        state.imageTags.shapes.push({
          "type":"rectangle",
          "occluded":false,
          "z_order":0,
          "points":shapes.rectangles[item].points,
          "attributes":[
            // {
            //   "spec_id":"17",
            //   "value":""
            // }
          ],
          "frame":shapes.rectangles[item].frame,
          "label_id":shapes.rectangles[item].label_id,
          "group":0
        })
      }
      console.log(state.imageTags.shapes)
    },
    cleanTagsInfo(state,frame){
      let imgIndex = frame + 1
      console.log('开始删除第'+imgIndex+'张图片的信息');
      for(let item in state.imageTags.shapes){
        if(state.imageTags.shapes[item].frame === imgIndex){
          console.log(state.imageTags.shapes[item]);
          state.imageTags.shapes.splice(item,1)
        }
      }
      console.log('删除完成');
    }
  },
  actions: {
  },
  modules: {
  }
})
