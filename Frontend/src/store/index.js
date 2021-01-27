import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    //用户信息
    userInfo: '',
    //job信息
    jobInfo: {},
    allJobs: [],
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
  /** 基本信息相关 */
    //保存当前登录的用户信息
    saveUserInfo(state, userInfo){
      state.userInfo = userInfo
      console.log('1.2.保存用户信息到仓库', state.userInfo);
    },
    saveIfOwnerToUserInfo(state, ifOwner){
      state.userInfo.ifOwner = ifOwner
      console.log('1.3.保存用户权限信息到仓库', state.userInfo);
    },
    //当前进入的job信息
    saveJobInfo(state, jobInfo){
      state.jobInfo.jobId = jobInfo
    },
    //setting界面中返回项目job时的列表
    saveAllJobs(state, jobs){
      state.allJobs = jobs
    },

  /** 新建项目相关数据 */
    //设置用户选择的上传模式
    changeUserChoiceModel(state,num){
      state.userChoiceModel = num;
    },
    //新建项目时保存label信息
    addToStore(state, labData){
      //先删除原有数据
      state.projectInfo.labels = []
      //添加更新后的数据
      for(let i = 0; i < labData.length; i++){
        let item = {}
        item.name = labData[i].name
        //TODO： 这个id好像不需要 我也忘了当初为什么要加这个东西了，先留着吧
        // item.id = labData[i].id
        item.attributes = labData[i].attributes
        state.projectInfo.labels.push(item)
      }
      console.log("仓库数据更新完成", state.projectInfo.labels);
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

  /** 页面标注数据相关操作 */
    //每创建一个标注对象时添加到本地仓库
    saveTagsInfo(state, shape) {
      state.imageTags.shapes.push(shape)
    },
    //修改标注数据
    changeTagInfo(state, TagInfo) {
      for(let i = 0; i < state.imageTags.shapes.length; i++){
        if(state.imageTags.shapes[i].id === TagInfo.id){
          state.imageTags.shapes[i] = TagInfo
        }
      }
      console.log('仓库标签信息修改结束', state.imageTags.shapes);
    },
    //删除标注数据
    delTagInfo(state, shapeId){
      for(let item of state.imageTags.shapes){
        if(item.id === shapeId){
          state.imageTags.shapes.splice(state.imageTags.shapes.indexOf(item), 1)
        }
      }
    },
    //退出工作台清除仓库中标注数据缓存
    cleanTagsInfo(state){
      state.imageTags = {
        "shapes":[
        ],
        "tracks":[
        ],
        "tags":[
        ],
        "version":26
      }
      console.log('仓库标注缓存已被清除');
    },

  /** 下面未分类 */
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
