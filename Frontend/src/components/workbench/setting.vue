<template>
  <div>
    setting
    <div class="download" @click="downloadData"></div>
  </div>
</template>

<script>
export default {
  methods: {
    downloadData(){
      this.$http.get()
    }
  }
}
</script>

<style lang="less" scoped>
.download{
  width: 100px;
  height: 100px;
  background-color: lightgreen;
}
</style>
