import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    //用户信息
    userInfo: '',
    //job信息
    jobInfo: {},
    //选择的模式：1代表用户上传数据集，2代表用户使用已经存在的数据集
    userChoiceModel: 1,
    //项目基本信息
    projectInfo: {
      "name": "",
      "describe": '',
      "labels": [

      ],
      "z_order": false,
    },
    //所有图片数据
    //用户拖拽上传的数据集
    allFileList: [],
    //使用服务器上的数据集
    allFileList02: [],
    //树形结构被选中的节点的key，用来回退上一步的时候进行恢复
    treeCheckedKeyList: [],
    //图片压缩质量
    image_quality: 70,
    //图片标注信息
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
    //保存当前登录的用户信息
    saveUserInfo(state, userInfo){
      state.userInfo = userInfo
      console.log('1.3.保存用户信息到仓库', state.userInfo);
    },
    //当前进入的job信息
    saveJobInfo(state, jobInfo){
      state.jobInfo.jobId = jobInfo
    },
    //设置用户选择的上传模式
    changeUserChoiceModel(state,num){
      state.userChoiceModel = num;
    },
    //新建项目时保存label信息
    /** label中的信息有变化，需要清洗*/
    addToStore(state, labData){
      //先删除原有数据
      state.projectInfo.labels = []
      //添加更新后的数据
      for(let i = 0; i < labData.length; i++){
        let item = {}
        item.name = labData[i].name
        item.id = labData[i].id
        item.attributes = labData[i].attributes
        state.projectInfo.labels.push(item)
      }
      console.log("仓库数据更新完成", state.projectInfo.labels);
    },
    updateLabels(state, labdata){
      //先删除原有数据
      state.projectInfo.labels = []
      state.projectInfo.labels = JSON.parse(labdata)
      console.log("通过row格式更改数据完成");
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
    },
    //图片数据上传到服务器完成后清除
    cleanFileList(){
      this.state.allFileList = []
      this.state.allFileList02 = []
      this.state.treeCheckedKeyList = []
      this.state.userChoiceModel = 1
      this.state.image_quality = 70
    },
    //保存图片数据，用户拖拽上传时使用
    saveFileList(state, listData){
      state.allFileList = listData
    },
    //保存图片数据，使用服务器存在的数据集上传时使用
    saveFileList02(state, listData){
      state.allFileList02 = listData
    },
    //保存图片数据，使用服务器存在的数据集上传时使用
    saveTreeCheckedKeyList(state, listData){
      state.treeCheckedKeyList = listData
    },
    //标注时保存标注对象信息
    saveTagsInfo(state, shapes) {
      console.log('开始保存新的矩形框信息');
      for(let i = 0;i < shapes.rectangles.length;i++){

        // console.log('正在保存第'+shapes.rectangles[i].index+'个矩形框的信息')

        state.imageTags.shapes.push({
          "type":"rectangle",
          "occluded":false,
          "z_order":0,
          "points":shapes.rectangles[i].points,
          "attributes":[
            // {
            //   "spec_id":"17",
            //   "value":""
            // }
          ],
          "frame":shapes.rectangles[i].frame,
          id: shapes.rectangles[i].id,
          "label_id":shapes.rectangles[i].label_id,
          "isCover":shapes.rectangles[item].isCover,
          "group":0
        })
      }
      console.log('新数据保存成功', state.imageTags.shapes)
    },
    //多次保存到时候先清除标注对象
    cleanTagsInfo(state,frame){
      // console.log(state.imageTags.shapes)
      console.log('开始删除第'+frame+'张图片的信息')
      for(let l = 0;l < state.imageTags.shapes.length;l++){
        if(state.imageTags.shapes[l].frame === frame){
          state.imageTags.shapes.splice(l,1)
          l--
        }
      }
      console.log('原数据清空完成');
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
      console.log(state.allUsers);
    },
    //单独修改job数量
    saveSeg(state, seg){
      state.projectInfo["segment_size"] = seg
    },
    //清除参与人员信息
    cleanUsersInfo(state){
      state.allUsers = []
    }
  },
  actions: {
  },
  modules: {
  }
})
