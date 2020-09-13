<template>
  <div class="item" ref="item" @mouseenter="showStart" @mouseleave="hideStart">
    <span class="pro-name">{{ proInfo.name }}</span>
    <span class="pro-info">{{ proInfo.describe }}</span>
    <div class="done">
      <span class="remain">剩余待标记: {{ remain }}</span>
      <span class="ratio">任务完成度: {{ ratio }}</span>
    </div>
    <div class="bg"></div>
    <div class="cover" ref="cover">
      <div
        class="start"
        @click="toWorkbench(proInfo.id)"
      >
        开始标记
      </div>
      <router-link
        tag="div"
        class="exam"
        :to="'/workbench/setting'"
      >
        配置
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  props: ["proInfo"],
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
    toWorkbench(index){
      //组织数据
      let logs = this.log
      let newDate = new Date()
      logs[0].time = newDate.toISOString()
      //创建log数据
      this.$http.post('v1/server/logs',logs).then(()=>{
        console.log('-1.创建log成功');
      }).catch(()=>{
        console.log('-1.创建log失败');
      })
      this.$router.push('/workbench/task/' + index)
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
    background-size: cover;
    border-radius: 20px;
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
      div{
        position: absolute;
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
        left: 0;
        width: 200px;
        transition: all 0.2s;
      }
      .start:hover{
        background-color: rgba(0,0,0,0.4);
        color: #eeeeee;
      }
      .exam{
        right: 0;
        width: 100px;
        transition: all 0.2s;
      }
      .exam:hover{
        background-color: rgba(0,0,0,0.4);
        color: #eeeeee;
      }
    }
    .bg{
      width: 100%;
      height: 100%;
      background-color: rgba(0,0,0,0.6);
    }
  }
</style>
