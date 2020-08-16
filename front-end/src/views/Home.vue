<template>
  <div class="home-box">
    <el-container>
      <el-aside width="160px">
        <div class="title">
          安软标记平台
        </div>
        <div class="tab-box">
          <router-link
            to="/home/project"
            class="app-project tabs"
            tag="div"
            active-class="selected"
          >
            <i class="el-icon-menu"> 全部项目</i>
          </router-link>
          <router-link
            to="/home/user"
            class="user-center tabs"
            tag="div"
            active-class="selected"
          >
            <i class="el-icon-user-solid"> 个人中心</i>
          </router-link>
          <router-link
            v-if="ifAdmin === 'admin'"
            to="/home/management"
            class="management tabs"
            tag="div"
            active-class="selected"
          >
            <i class="el-icon-s-tools"> 管理中心</i>
          </router-link>
        </div>
      </el-aside>
      <el-container>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>

export default {
  data(){
    return {
      path: '',
      ifAdmin: ''
    }
  },
  created() {
    this.getUserInfo()
  },
  methods: {
    //判断是不是管理员
    getUserInfo(){
      this.$http.get('v1/users/self').then((res)=>{
        this.ifAdmin = res.data.groups.find(val=>{
          return val === 'admin'
        })
      })
    }
  },
}
</script>

<style lang="less" scoped>
  .home-box{
    height: 100%;
    .el-container{
      height: 100%;
    }
    .el-aside{
      background-color: #3c4147;

      -moz-user-select: none;
      -webkit-user-select: none;
      -ms-user-select: none;
      user-select: none;
      .title{
        width: 100%;
        height: 80px;
        background-color: #272b34;
        text-align: center;
        line-height: 80px;
        color: #eeeeee;
        font-size: 22px;
      }
      .tab-box{
        width: 100%;
        padding-top: 20px;
        .tabs{
          width: 100%;
          height: 50px;
          margin-bottom: 8px;
          text-align: center;
          line-height: 50px;
          transition: background-color 0.2s;
          i{
            font-size: 18px;
            line-height: 50px;
            padding-right: 8px;
            color: #cccccc;
          }
        }
        .tabs:hover{
          background-color: #272b34;
        }
        .selected{
          background-color: #2d3135;
          i{
            color: #ffffff;
          }
        }
      }
    }
    .el-main{
      background-color: #eeeeee;
    }
  }
</style>
