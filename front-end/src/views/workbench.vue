<template>
  <div>
    <span>workbench</span>
    <DrawPage></DrawPage>
  </div>
</template>

<script>
export default {
  comments: {
    DrawPage,
  },
  created() {
    this.showId()
  },
  data(){
    return{

    }
  },
  methods: {
    showId(){
      console.log(this.$route.query.id);
    }
  }
}
</script>

<style lang="less" scoped>

</style>
