<template>
  <div class="item" @mouseenter="showStart" @mouseleave="hideStart">
    <span class="pro-name">{{ proInfo.name }}</span>
    <span class="pro-info">{{ proInfo.describe }}</span>
    <div class="done">
      <span class="remain">剩余待标记: {{ remain }}</span>
      <span class="ratio">任务完成度: {{ ratio }}</span>
    </div>
    <div class="cover" ref="cover">
      <router-link
        tag="div"
        class="start"
        :to="'/workbench/' + projectId "
      >
        开始标记
      </router-link>
      <router-link
        tag="div"
        class="exam"
        :to="'/workbench/' + projectId "
      >
        复查
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  props: ["proInfo"],
  data() {
    return{
      projectId: '1',
      remain: '15',
      ratio: '50%'
    }
  },
  methods: {
    showStart(){
      this.$refs.cover.style.top = "0px"
    },
    hideStart(){
      this.$refs.cover.style.top = "300px"
    }
  }
}
</script>

<style lang="less" scoped>
  .item{
    position: relative;
    width: 300px;
    height: 200px;
    background-color: #D4F5F7;
    border-radius: 20px;
    float: left;
    margin: 10px;
    overflow: hidden;
    .pro-name{
      position: absolute;
      left: 15px;
      top: 15px;
      font-size: 18px;
    }
    .pro-info{
      position: absolute;
      left: 15px;
      top: 37px;
      font-size: 14px;
      color: #888888;
    }
    .done{
      position: absolute;
      bottom: 0;
      width: 100%;
      height: 100px;
      background-color: #8DD6C1;
      .remain{
        position: absolute;
        left: 12px;
        bottom: 36px;
      }
      .ratio{
        position: absolute;
        left: 12px;
        bottom: 10px;
      }
    }
    .cover{
      position: absolute;
      top: 200px;
      width: 100%;
      height: 100%;
      transition: top 0.2s ease;
      div{
        position: absolute;
        background-color: rgba(0,0,0,0.6);
        transition: background-color 0.2s;
        margin: 0;
        line-height: 200px;
        text-align: center;
        height: 100%;
        font-size: 18px;
        color: #eeeeee;
        letter-spacing: 2px;
        cursor: pointer;

        -moz-user-select: none;
        -webkit-user-select: none;
        -ms-user-select: none;
        user-select: none;
      }
      .start{
        left: 0;
        width: 200px;
      }
      .start:hover{
        background-color: rgba(0,0,0,0.4);
      }
      .exam{
        right: 0;
        width: 100px;
      }
      .exam:hover{
        background-color: rgba(0,0,0,0.4);
      }
    }
  }
</style>
