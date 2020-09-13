<template>
  <div class="new-container">
    <div class="guide-line-box">
      <div :class="['guide', 'bacic', step===1 ? 'guide-active' : '']">
        <span>1</span>
        <span class="text">基本信息</span>
      </div>
      <div class="line"></div>
      <div :class="['guide', 'data', step===2 ? 'guide-active' : '']">
        <span>2</span>
        <span class="text">上传数据集</span>
      </div>
      <div class="line"></div>
      <div :class="['guide', 'template', step===3 ? 'guide-active' : '']">
        <span>3</span>
        <span class="text">基本配置</span>
      </div>
    </div>
    <div class="project-info-box">
      <basicinfo v-if="step === 1"></basicinfo>
      <uploaddata v-if="step === 2"></uploaddata>
      <module v-if="step === 3"></module>
    </div>
    <div class="btn-box">
      <div
        class="btn back"
        v-if="step === 2 || step === 3"
        @click="back()"
      >
        <span>上一步</span>
      </div>
      <div
        class="btn next"
        v-if="step === 1 || step === 2"
        @click="nextStep()"
      >
        <span>下一步</span>
      </div>
      <div
        class="btn submit"
        v-if="step === 3"
        @click="submit()"
      >
        <span>{{ text }}</span>
      </div>
      <div
        ref="progress"
        class="btn upload-progress"
      >
        <div class="upload-progress-line" ref="progressLine"></div>
        <span>{{ progressText }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import basicinfo from '@/components/newproject/basicinfo.vue'
import uploaddata from '@/components/newproject/uploaddata.vue'
import module from '@/components/newproject/module.vue'
export default {
  components :{
    basicinfo,
    uploaddata,
    module
  },
  data(){
    return{
      step: 1,
      text: '创建新项目',
      progressText: '开始创建',
    }
  },
  methods: {
    //控制步骤
    back(){
      if(this.step > 1){
        this.step --
      }
    },
    nextStep(){
      if(this.step < 3){
        this.step ++
      }
    },

    //开始提交新建项目请求
    submit(){
      //从vuex中获取要新建的项目数据
      let proData = this.$store.state.projectInfo
      //判断项目基本信息是否填写
      if(proData.name !== '' && proData.describe !== '') {
        this.$http.post('v1/tasks', proData).then(e => {
          console.log(e.data);
          this.progressText = '正在创建'
          this.$refs.progressLine.style.width = "100px"
          //成功后将vuex中的数据删除
          this.$store.commit('cleanStore')
          //开始上传数据集
          this.uploadData(e.data.url)
          //展示上传数据集的进度
          this.showProgress(e.data.url)
        })
      } else {
        //转到第一步
        this.step = 1
        //提示填写数据
        this.open()
      }
    },
    //上传数据集
    uploadData(url){
      //组织数据
      let data = new FormData()
      data.append("image_quality", this.$store.state.image_quality)
      this.$store.state.allFileList.forEach((item, index) => {
        data.append("client_files["+ index +"]", item)
      })
      data.append("use_zip_chunks", false)

      //展示进度条
      this.$refs.progress.style.width = "900px"
      //发送请求
      this.$http.post(url + '/data', data).then(e=>{
        console.log(e);
        if(e.status === 202){
          this.progressText = '上传成功'
          this.$refs.progressLine.style.transition = "width 0.5s ease"
          this.$refs.progressLine.style.width = "900px"
          //跳转
          this.$router.push({path:'/home'})
          //清除文件列表
          this.$store.commit('cleanFileList')
        }
      })
    },
    //上传进度展示
    async showProgress(url){


      let state = await this.getStatus(url)
      console.log(state);
      if(state === "Finished"){
        this.progressText = '创建完成，正在上传数据'
        this.$refs.progressLine.style.width = "850px"

      }
    },
    //获取上传进度
    getStatus(url){
      return this.$http.get(url + '/status').then(e => {
        return e.data.state
      })
    },
    //未填写消息
    open() {
      this.$message.error('请填写必要的信息');
    },
  }
}
</script>

<style lang="less" scoped>
.new-container{
  width: 100%;
  .guide-line-box{
    width: 1000px;
    height: 60px;
    margin-top: 20px;
    padding-left: 50px ;
    .guide{
      height: 100%;
      width: 60px;
      border-radius: 50%;
      background-color: #D4EBDB;
      float: left;
      text-align: center;
      line-height: 60px;
      span{
        color: #ffffff;
        font-size: 20px;
      }
      .text{
        color: #222222;
        font-size: 14px;
        display: block;
        height: 26px;
        width: 80px;
        text-align: left;
        line-height: 26px;
      }
    }
    .guide-active{
      background-color: #318B71;
    }
    .line{
      float: left;
      width: 300px;
      height: 2px;
      background-color: #D4EBDB;
      margin:  28px 10px;
    }
  }
  .project-info-box{
    width: 900px;
    background-color: transparent;
    margin: 40px 20px 0 20px;
    border-radius: 30px;
  }
  .btn-box{
    position: relative;
    width: 900px;
    height: 50px;
    margin: 20px;
    .btn{
      height: 100%;
      background-color: #7EC492;
      position: absolute;
      border-radius: 8px;
      text-align: center;
      line-height: 50px;
      color: #ffffff;
      font-size: 18px;
      transition: 0.2s;
      cursor: pointer;
    }
    .btn:hover{
      background-color: #318B71;
    }
    .back{
      width: 120px;
      left: 0;
    }
    .next{
      width: 120px;
      left: 130px;
    }
    .submit{
      width: 150px;
      right: 0;
    }
    .upload-progress{
      left: 0;
      width: 0;
      height: 50px;
      transition: width 0.3s ease;
      overflow: hidden;
      .upload-progress-line{
        position: absolute;
        left: 0;
        top: 0;
        width: 0;
        height: 100%;
        background-color: #318B71;
        transition: width 10s linear;
      }
      span{
        position: absolute;
        display: block;
        height: 50px;
        width: 500px;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        z-index: 2;
      }
    }
    .upload-progress:hover{
      background-color: #7EC492;
    }
  }
}
</style>
