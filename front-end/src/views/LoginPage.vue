<template>
  <div class="background">
    <div class="login-box">
      <Login />
    </div>
  </div>
</template>

<script>
import Login from '../components/login.vue'
export default {
  components: {
    Login
  }
}
</script>

<style lang="less" scoped>
.background{
  height: 100%;
  background-color: #636363;
}
.login-box{
  width: 600px;
  height: 400px;
  background-color: transparent;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
</style>
