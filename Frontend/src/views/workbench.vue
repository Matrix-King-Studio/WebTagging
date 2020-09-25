<template>
  <div class="workbench">
    <div class="header">
      <div class="icon" @click="backHome">
        <span>安软标记平台</span>
      </div>
      <div class="user">
        <i class="el-icon-user-solid"></i>
        <span>用户名</span>
      </div>
      <router-link
        v-if="mod === 'task'"
        class="to-setting"

        :to="'/workbench/setting/' + taskId"
        tag="div"
        @click.native="changeMod"
      >
        <i class="el-icon-s-tools"></i>
        <span>项目设置</span>
      </router-link>
      <router-link
        v-if="mod === 'set'"
        class="to-task"
        :to="'/workbench/task/' + taskId"
        tag="div"
        @click.native="changeMod"
      >
        <i class="el-icon-menu"></i>
        <span>工作台</span>
      </router-link>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  data(){
    return{
      mod: 'task',
      taskId: ''
    }
  },
  created() {
    //获取task id用于获取数据
    this.getTaskId(this.$route.params.index)
    /** 这里还是无法区分task和setting*/
  },
  mounted() {
    this.getMod()
  },
  methods: {
    //加载时获取模式
    getMod(){
      // console.log(this.$route.path);
      // console.log(this.$route.path.indexOf('task'));
      if(this.$route.path.indexOf('task') !== -1){
        this.mod = 'task'
      } else if (this.$route.path.indexOf('setting') !== -1){
        this.mod = 'set'
      } else {
        console.log('getMod error');
      }
    },
    //切换工作台和项目设置
    changeMod(){
      if(this.mod === 'task'){
        this.mod = 'set'
      } else if (this.mod === 'set'){
        this.mod = 'task'
      }
    },
    //拿到项目id
    getTaskId(id){
      this.taskId = id
    },
    //点击左上角图标回home
    backHome(){
      this.$router.push('/home')
    }
  }
}
</script>

<style lang="less" scoped>
.workbench{
  padding-top: 35px;
  height: 100%;
  overflow: hidden;
  box-sizing: border-box;
  .header{
    position: absolute;
    top: 0;
    width: 100%;
    height: 35px;
    background-color: #bbe6d6;
    box-shadow: 0 0 4px 1px #a3c4b7;
    z-index: 4;
    .icon{
      height: 100%;
      width: 120px;
      text-align: center;
      cursor: pointer;
      span{
        line-height: 35px;
        font-weight: 600;
        font-size: 18px;
      }
    }
    .to-setting,.to-task{
      position: absolute;
      top: 0;
      right: 100px;
      height: 100%;
      width: 100px;
      border-left: 1px solid #b3d9cb;
      line-height: 35px;
      text-align: center;
      cursor: pointer;
      span{
        font-size: 14px;
      }
    }
    .user{
      position: absolute;
      top: 0;
      right: 0;
      height: 100%;
      width: 100px;
      border-left: 1px solid #b3d9cb;
      line-height: 35px;
      text-align: center;
      span{
        font-size: 14px;
      }
    }
  }
}
</style>
