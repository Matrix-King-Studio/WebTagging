<template>
  <div class="item" ref="item" @mouseenter="showStart" @mouseleave="hideStart">
    <span class="pro-name">{{ proInfo.name }}</span>
    <span class="pro-info">{{ proInfo.describe }}</span>
    <span v-if="!userInfo" class="pro-id">任务Id:{{ proInfo.segIndex }}</span>
<!--    <div class="done">-->
<!--      <span class="remain">剩余待标记: {{ remain }}</span>-->
<!--      <span class="ratio">任务完成度: {{ ratio }}</span>-->
<!--    </div>-->
    <div class="bg"></div>
    <div class="cover" ref="cover">
      <div
        class="start"
        @click.stop="toWorkbench(proInfo.id, jobId)"
      >
        开始标记
      </div>
      <div
        v-if="userInfo"
        class="exam"
        @click="toTaskSetting(proInfo.id, jobId)"
      >
        配置
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["proInfo","userInfo","jobId"],
  data() {
    return{
      projectId: '1',
      remain: '15',
      ratio: '50%',

      //开始标注传输的日志
      log: [{
        "name": 'Send user activity',
        "time": '',
        "clientId": '642862',
        "is_active": true,
        "payload": {
          "working_time": 6666,
        }
      }]
    }
  },
  created() {
    this.getCoverImg()
  },
  methods: {
    showStart(){
      this.$refs.cover.style.top = "0px"
    },
    hideStart(){
      this.$refs.cover.style.top = "300px"
    },
    //开始标记
    toWorkbench(index, jobId){
      //组织数据
      let logs = this.log
      let newDate = new Date()
      logs[0].time = newDate.toISOString()
      //创建log数据
      this.$http.post('v1/server/logs',logs).then(()=>{
        // console.log('-1.创建log成功')
      }).catch(()=>{
        // console.log('-1.创建log失败')
      })
      if(this.userInfo){
        //管理员进入整个task
        this.$router.push('/workbench/task/' + index)
      } else {
        //标注员获取对应job的图片
        this.$store.commit('saveJobInfo', jobId)
        this.$router.push('/workbench/task/' + index + '/job/' + jobId)
      }
    },
    // //获取标注员对应的jobId
    // /** 先规定一个人只能拥有一个task中的一个job*/
    // /** 之后考虑一个人被分配了多个不相邻的job啊啊啊啊啊啊啊啊啊啊*/
    // getJobId(){
    //   console.log(this.proInfo);
    //   for(let item of this.proInfo.segments){
    //     if(item.jobs[0].assignee === this.$store.state.userInfo.id){
    //       console.log('该标注员对应的jobId', item.jobs[0].id);
    //       return item.jobs[0].id
    //     }
    //   }
    // },
    //转到Task控制台
    toTaskSetting(index){
      this.$router.push('/workbench/setting/' + index)
    },
    //获取预览图片
    getCoverImg(){
      this.$http.get('v1/tasks/'+ this.proInfo.id + '/data?type=preview',{
        responseType:'arraybuffer',
      }).then(e=>{
        let imgdata = "data:image/jpeg;base64," + window.btoa(String.fromCharCode(...new Uint8Array(e.data)))
        this.$refs.item.style.background = "url("+ imgdata +")"
      })
    }
  }
}
</script>

<style lang="less" scoped>
  .item{
    position: relative;
    width: 300px;
    height: 200px;
    background-size: cover !important;
    background-repeat: no-repeat !important;
    border-radius: 16px;
    float: left;
    margin: 10px;
    overflow: hidden;
    .pro-name{
      position: absolute;
      left: 15px;
      top: 15px;
      font-size: 18px;
      color: #cccccc;
    }
    .pro-info{
      position: absolute;
      left: 15px;
      top: 37px;
      font-size: 14px;
      color: #aaaaaa;
    }
    .pro-id{
      position: absolute;
      left: 15px;
      top: 56px;
      font-size: 14px;
      color: #aaaaaa;
    }
    .done{
      position: absolute;
      bottom: 0;
      width: 100%;
      height: 100px;
      background-color: rgba(166, 252, 226, 0.7);
      .remain{
        position: absolute;
        left: 12px;
        bottom: 36px;
      }
      .ratio{
        position: absolute;
        left: 12px;
        bottom: 10px;
      }
    }
    .cover{
      position: absolute;
      top: 200px;
      width: 100%;
      height: 100%;
      transition: top 0.2s ease;

      display: flex;
      div{
        //position: absolute;
        background-color: rgba(0,0,0,0.8);
        transition: background-color 0.2s;
        margin: 0;
        line-height: 200px;
        text-align: center;
        height: 100%;
        font-size: 18px;
        color: #999999;
        letter-spacing: 2px;
        cursor: pointer;

        -moz-user-select: none;
        -webkit-user-select: none;
        -ms-user-select: none;
        user-select: none;
      }
      .start{
        flex: 2;

        left: 0;
        width: 200px;
        transition: all 0.2s;
      }
      .start:hover{
        background-color: rgba(0,0,0,0.4);
        color: #eeeeee;
      }
      .exam{
        flex: 1;

        right: 0;
        width: 100px;
        transition: all 0.2s;
      }
      .exam:hover{
        background-color: rgba(0,0,0,0.3);
        color: #eeeeee;
      }
    }
    .bg{
      width: 100%;
      height: 100%;
      background-color: rgba(0,0,0,0.4);
    }
  }
</style>
