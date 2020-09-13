<template>
  <div class="workbench">
    <div class="header">
      <div class="icon">
        <span>安软标记平台</span>
      </div>
      <div class="user">
        <i class="el-icon-user-solid"></i>
        <span>用户名</span>
      </div>
      <router-link
        v-show="mod === 'task'"
        class="to-setting"
        to="/workbench/setting"
        tag="div"
        @click.native="changeMod"
      >
        <i class="el-icon-s-tools"></i>
        <span>项目设置</span>
      </router-link>
      <router-link
        v-show="mod === 'set'"
        class="to-task"
        to="/workbench/task"
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
  created() {
    if(this.$route.path === '/workbench/task'){
      this.mod = 'task'
    } else if (this.$route.path === '/workbench/setting'){
      this.mod = 'set'
    }
  },
  data(){
    return{
      mod: 'task'
    }
  },
  methods: {
    changeMod(){
      if(this.mod === 'task'){
        this.mod = 'set'
      } else if (this.mod === 'set'){
        this.mod = 'task'
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
      width: 120px;
      text-align: center;
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
