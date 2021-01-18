<template>
  <div class="home-box">
    <el-container>
      <el-aside width="160px">
        <div class="title">
          安软标记平台
        </div>
        <div class="tab-box">
          <!--全部项目-->
          <router-link
            to="/home/project"
            class="app-project tabs"
            tag="div"
            active-class="selected"
            style="cursor: pointer;"
          >
            <i class="el-icon-menu"> 全部项目</i>
          </router-link>

          <!--日志分析-->
          <router-link
            to="/home/logAnalysis"
            class="app-project tabs"
            tag="div"
            active-class="selected"
            style="cursor: pointer;"
          >
            <i class="el-icon-menu"> 日志分析 </i>
          </router-link>

          <!--用户中心-->
          <router-link
            to="/home/user"
            class="user-center tabs"
            tag="div"
            active-class="selected"
            style="cursor: pointer;"
          >
            <i class="el-icon-user-solid">
              &nbsp;
              <!--              <span id="myCenter">{{userInfo.username | handleText}}</span>-->
              <span id="myCenter" :title="userInfo.username+'个人中心'">{{ userInfo.username }}</span>
            </i>

            <!--管理中心-->
          </router-link>
          <a
            v-if="ifAdmin === 'admin'"
            href="http://alexking.site:8080/admin/"
            class="management tabs"
          >
            <i class="el-icon-s-tools"> 管理中心</i>
          </a>
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
  data() {
    return {
      path: '',
      ifAdmin: '',
      userInfo: {}
    }
  },
  created() {
    this.getUserInfo()
  },
  methods: {
    //判断是不是管理员
    getUserInfo() {
      this.$http.get('v1/users/self').then((res) => {
        this.userInfo = res.data;
        this.ifAdmin = res.data.groups.find(val => {
          return val === 'admin'
        })
      })
    },
  },
  filters: {
    //显示省略号的过滤器，目前没有使用
    handleText(value) {
      // if (!value) return '';
      if (value.length > 6) {
        return value.slice(0, 6) + '...'
      }
      return value
    }
  }
}
</script>

<style lang="less" scoped>
.home-box {
  height: 100%;

  .el-container {
    height: 100%;
  }

  .el-aside {
    background-color: #3c4147;

    -moz-user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
    user-select: none;

    .title {
      width: 100%;
      height: 80px;
      background-color: #272b34;
      text-align: center;
      line-height: 80px;
      color: #eeeeee;
      font-size: 22px;
    }

    .tab-box {
      width: 100%;
      padding-top: 20px;

      .tabs {
        display: block;
        width: 100%;
        height: 50px;
        margin-bottom: 8px;
        text-align: center;
        line-height: 50px;
        transition: background-color 0.2s;

        i {
          font-size: 18px;
          line-height: 50px;
          padding-right: 8px;
          color: #cccccc;
        }
      }

      .tabs:hover {
        background-color: #272b34;
      }

      .selected {
        background-color: #2d3135;

        i {
          color: #ffffff;
        }
      }
    }
  }

  .el-main {
    background-color: #eeeeee;
  }
}

#myCenter {
  width: 75px;
  height: 48px;
  /*border: 1px solid #9ce8d2;*/
  white-space: nowrap;
  /*使用下面这两行会导致图标下坠一点点*/
  overflow: hidden;
  text-overflow: ellipsis;
  display: inline-block;
  /*解决塌陷问题*/
  vertical-align: top;
}
</style>
