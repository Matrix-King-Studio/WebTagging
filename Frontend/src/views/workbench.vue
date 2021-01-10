<template>
  <div class="workbench">
    <div class="header">
      <div title="返回主界面" class="icon" @click="backHome">
        <span>◀安软标记平台</span>
      </div>
      <div class="user">
        <i class="el-icon-user-solid"></i>
        <el-dropdown trigger="click" @command="handleUserClick">
          <span class="el-dropdown-link">
            <span v-text="userInfo.username"></span>
            <i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
      <router-link
        v-if="mod === 'task' && ifOwner"
        class="to-setting"
        :to="'/workbench/setting/' + taskId"
        tag="div"
        @click.native="changeMod"
      >
        <i class="el-icon-s-tools"></i>
        <span>项目设置</span>
      </router-link>
      <div
        v-if="mod === 'set' && ifOwner"
        class="to-task"
      >
        <el-dropdown>
          <span class="el-dropdown-link">
            <i class="el-icon-menu"></i>去往工作台
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>黄金糕</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  data(){
    return{
      mod: 'task',
      taskId: '',
      userInfo: {},
      userId: '',
      ifAdmin: '',
      ifOwner: false,
    }
  },
  created() {
    //获取task id用于获取数据
    this.getTaskId(this.$route.params.index)
    //获取当前用户信息
    this.getCurrentUserInfo()
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
    },
    //获取当前登录用户信息
    //TODO: 用户身份判断需完善
    getCurrentUserInfo(){
      this.$http.get('v1/users/self').then((e)=>{
        console.log('当前用户信息', e.data);
        this.userInfo = e.data
        this.userId = e.data.groups[0] !== 'annotator';
      })
      this.ifAdmin = this.$store.state.userInfo.ifAdmin
      this.ifOwner = this.$store.state.userInfo.ifOwner

    },
    //用户下拉菜单点击事件处理
    handleUserClick(command){
      if(command === 'logout'){
        this.$http.post('v1/auth/logout').then((e)=>{
          console.log(e);
          window.sessionStorage.removeItem('token')
          this.$message({
            message:"退出登录成功",
            type: "success"
          })
          this.$router.push('/login')
        })
      }
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
      width: 140px;
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
      right: 120px;
      height: 100%;
      width: 120px;
      border-left: 1px solid #b3d9cb;
      line-height: 35px;
      text-align: center;
      cursor: pointer;
      span{
        font-size: 14px;
      }
      .el-dropdown-link{
        color: #222222;
      }
    }
    .user{
      position: absolute;
      top: 0;
      right: 0;
      height: 100%;
      width: 120px;
      border-left: 1px solid #b3d9cb;
      line-height: 35px;
      text-align: center;
      cursor: pointer;
      span{
        font-size: 14px;
      }
    }
  }
}
/deep/ .el-dropdown-menu__item:hover{
  background-color: transparent;
}
</style>
