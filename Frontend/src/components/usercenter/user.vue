<template>
  <div class="logout" @click="logout">
    <span>退出登录</span>
  </div>
</template>

<script>
export default {
  data(){
    return{

    }
  },
  methods: {
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
  }
}
</script>

<style lang="less" scoped>
.logout {
  height: 40px;
  width: 100px;
  border-radius: 5px;
  background-color: #90eec2;
  text-align: center;
  line-height: 40px;
  cursor: pointer;
}
</style>
