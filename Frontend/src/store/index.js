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
    },
    //参与人员的key
    allUsers: []
  },
  mutations: {
    //新建项目时保存label信息
    addToStore(state, labData){
      state.projectInfo.labels = labData
    },
    //新建项目时保存图片质量
    addImageQuality(state, image_quality){
      state.image_quality = image_quality
    },
    //新建项目完成后清除信息
    cleanStore(){
      this.state.projectInfo = {
        "name": "",
        "describe": '',
        "labels": [

        ],
        "z_order": false,
      }
      this.state.image_quality = 70
      this.state.allUsers = []
    },
    //图片数据上传完成后清除
    cleanFileList(){
      this.state.allFileList = []
    },
    //啊这
    saveFileList(state, listData){
      state.allFileList = listData
    },
    //标注时保存标注对象信息
    saveTagsInfo(state, shapes) {
      console.log('开始保存新的矩形框信息');
      for(let item = 0;item < shapes.rectangles.length;item++){
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
    //多次保存到时候先清除标注对象
    cleanTagsInfo(state,frame){
      let imgIndex = frame + 1
      console.log(state.imageTags.shapes)
      console.log('开始删除第'+imgIndex+'张图片的信息')
      for(let l = 0;l < state.imageTags.shapes.length;l++){
        console.log(l)
        if(state.imageTags.shapes[l].frame === imgIndex){
          console.log(state.imageTags.shapes[l])
          state.imageTags.shapes.splice(l,1)
          l--
        }
      }
      console.log('删除完成');
    },
    //保存任务分配
    //没有设置人员列表无segmentsize，设置人员列表segmentsize等于列表长度
    saveAllUsers(state, users){
      state.allUsers = users
      if(state.allUsers.length === 0){
        delete state.projectInfo.segment_size
      } else {
        state.projectInfo["segment_size"] = state.allUsers.length
      }
    }
  },
  actions: {
  },
  modules: {
  }
})
