<template>
  <router-link
    class="newItem"
    to="/home/newproject"
  >
    <i class="el-icon-plus"></i>
    <span>新建项目</span>
  </router-link>
</template>

<script>
export default {
  data() {
    return{
    }
  }
}
</script>

<style lang="less" scoped>
.newItem{
  position: relative;
  width: 300px;
  height: 200px;
  background-color: #D2EFFA;
  border-radius: 20px;
  float: left;
  margin: 10px;
  box-sizing: border-box;
  border: 2px dashed #aceedb;
  text-align: center;
  line-height: 270px;
  cursor: pointer;
  .el-icon-plus{
    font-size: 120px;
    color: #ffffff;
  }
  span{
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    bottom: 12px;
    line-height: 30px;
    letter-spacing: 2px;
    color: #333333;

    -moz-user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }
}
.newItem:hover{
  border: 2px dashed #67b6a0;
}
</style>
