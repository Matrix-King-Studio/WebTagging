<template>
  <div>
    <div id="grzx"><span>个人中心</span></div>
    <div id="userInformation">
        <ul>
          <li><i class="el-icon-user">&nbsp;用户名：</i>{{userInfo.username}}</li>
          <li><i class="el-icon-message">&nbsp;邮箱：</i>{{userInfo.email}}</li>
          <li><i class="el-icon-date">&nbsp;注册日期：</i>{{userInfo.date_joined|timefilters}}</li>
          <li><i class="el-icon-time">&nbsp;上次登录：</i>{{userInfo.last_login|timefilters}}</li>
        </ul>
    </div>

    <div class="logout"  @click="logout">
      <span>退出登录</span>
    </div>

  </div>
</template>

<script>
export default {
  data(){
    return{
      userInfo:{}
    }
  },
  methods: {
    //获取用户信息
    getUserInfo(){
      this.$http.get('v1/users/self').then((res)=>{
        this.userInfo = res.data;
        console.log(this.userInfo);
      })
    },
    //退出登录
    logout(){
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
  },
  created() {
    this.getUserInfo()
  },
  filters: {
    //UTC时间格式转换为北京时间
    timefilters(val) {
      if (val == null || val == "") {
        return "暂无时间";
      } else {
        let d = new Date(val);   //val 为表格内取到的后台时间
        let month =
                d.getMonth() + 1 < 10 ? "0" + (d.getMonth() + 1) : d.getMonth() + 1;
        let day = d.getDate() < 10 ? "0" + d.getDate() : d.getDate();
        let hours = d.getHours() < 10 ? "0" + d.getHours() : d.getHours();
        let min = d.getMinutes() < 10 ? "0" + d.getMinutes() : d.getMinutes();
        let sec = d.getSeconds() < 10 ? "0" + d.getSeconds() : d.getSeconds();
        let times=d.getFullYear() + '-' + month + '-' + day + ' ' + hours + ':' + min + ':' + sec;
        return times;
      }
    }
  }
}
</script>

<style lang="less" scoped>
#grzx{
  height: 40px;
  margin-bottom: 10px;
  background-color: #9a6e3a;
  border-radius: 10px;
  text-align: center;
}
#grzx span{
  line-height:40px;
}

#userInformation{
  width: 500px;
  /*height: 300px;*/
  /*阴影*/
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-radius: 15px;
  background-color: #a1f2ff;
  border:1px solid #9a6e3a;
}

#userInformation li{
  padding-top: 10px;
  padding-bottom: 10px;
  list-style:none;
}

.logout {
  height: 40px;
  width: 100px;
  margin-top: 50px;
  border-radius: 5px;
  background-color: #90eec2;
  text-align: center;
  line-height: 40px;
  cursor: pointer;
}
  .logout:hover{
    background-color: #89ee90;
  }


</style>
