<template>
  <div class="item" ref="item" @mouseenter="showStart" @mouseleave="hideStart">
    <span class="pro-name">{{ proInfo.name }}</span>
    <span class="pro-info">{{ proInfo.describe }}</span>
    <span v-if="!ifOwner" class="pro-id">任务序号:{{ proInfo.segments[proInfo.segIndex].jobs[0].id }}</span>
    <div class="bg"></div>
    <div class="cover" ref="cover">
      <div
        class="start"
        v-if="!ifOwner && proInfo.mode === 'annotation'"
        @click.stop="toWorkbench(proInfo.id, proInfo.segments[proInfo.segIndex].jobs[0].id)"
      >
        开始标记
      </div>
      <div
        class="allJobs"
        v-if="ifOwner"
      >
        <div
          class="job"
          v-for="item in proInfo.segments"
          :key="item.jobs[0].id"
          @click.stop="toWorkbench(proInfo.id, item.jobs[0].id)"
        >
          <div class="id-box">
            <span>任务序号:{{ item.jobs[0].id }}</span>
          </div>
          <div class="status-box">
            <span class="status">状态:{{ whichStatus(item.jobs[0].status) }}</span>
          </div>
        </div>
      </div>
      <div
        v-if="ifOwner"
        class="exam"
        @click="toTaskSetting(proInfo.id)"
      >
        配置
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["proInfo","userInfo","ifOwner"],
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
    //卡片中job状态翻译函数
    whichStatus(status){
      if(status === 'annotation'){
        return '正在标注'
      } else if(status === 'validation'){
        return '正在质检'
      } else if(status === 'completed'){
        return '标注完成'
      }
    },
    //鼠标放到卡片上滑出效果
    showStart(){
      this.$refs.cover.style.top = "0px"
    },
    hideStart(){
      this.$refs.cover.style.top = "200px"
    },
    //开始标记
    toWorkbench(index, jobId){
      //组织数据
      let logs = this.log
      let newDate = new Date()
      logs[0].time = newDate.toISOString()
      // //创建log数据
      // this.$http.post('v1/server/logs',logs).then(()=>{
      //   // console.log('-1.创建log成功')
      // }).catch(()=>{
      //   // console.log('-1.创建log失败')
      // })
      //保存用户对于当前点击的job的身份是否是创建者(拥有者)
      this.$store.commit('saveIfOwnerToUserInfo', this.ifOwner)
      //保存当前点击的job的id用于之后的对比
      this.$store.commit('saveJobInfo', jobId)
      //跳转
      this.$router.push('/workbench/task/' + index + '/job/' + jobId)
    },
    //转到Task控制台
    toTaskSetting(index){
      this.$store.commit('saveIfOwnerToUserInfo', this.ifOwner)
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
      .start, .exam{
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
        transition: all 0.2s;
        background-color: rgba(0,0,0,0.4);
      }
      .start:hover{
        background-color: rgba(0,0,0,0.9);
        color: #ffffff;
      }
      .allJobs{
        flex: 2;
        overflow: auto;
        display: flex;
        flex-wrap: wrap;
        align-content: stretch;
        .job{
          box-sizing: border-box;
          transition: all 0.2s;
          width: 100%;
          min-height: 30px;
          padding-left: 6px;
          cursor: pointer;

          display: flex;
          justify-content: center;
          align-content: center;
          flex-wrap: wrap;
          background-color: rgba(0,0,0,0.4);
          .id-box{
            width: 100%;
            min-height: 18px;
            text-align: center;
            color: #aaaaaa;
          }
          .status-box{
            width: 100%;
            min-height: 12px;
            text-align: center;
            font-size: 10px;
            color: #999999;
          }
        }
        .job:hover{
          background-color: rgba(0,0,0,0.9);
        }
        .job:hover .id-box{
          color: #ffffff;
        }
        .job:hover .status-box{
          color: #eeeeee;
        }
      }
      .exam{
        flex: 1;

        right: 0;
        width: 100px;
        transition: all 0.2s;
      }
      .exam:hover{
        background-color: rgba(0,0,0,0.9);
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
