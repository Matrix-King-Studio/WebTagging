<template>
  <div class="info-box">
    <input
      v-model="$store.state.projectInfo.name"
      type="text"
      placeholder="项目名称"
      class="info pro-name"
    >
    <input
      v-model="$store.state.projectInfo.describe"
      type="text"
      placeholder="项目描述"
      class="info pro-name"
    >
  </div>
</template>

<script>
export default {
  data () {
    return{

    }
  }
}
</script>
<style lang="less" scoped>
.info-box{
  width: 100%;
  height: 320px;
  padding-top: 20px;
  background-color: #ecf5f3;
  border-radius: 30px;
  box-sizing: border-box;
  border: 2px solid #aceedb;

  .info{
    background-color: transparent;
    height: 30px;
    width: 600px;
    border: 0;
    border-bottom: 1px solid #318B71;
    margin: 50px ;
    outline: none;
    font-size: 18px;
    color: #0c2f2c;
  }
}
</style>
