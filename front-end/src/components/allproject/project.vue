<template>
  <div class="item-box">
    <projectitem v-for="item in projectData" :key="item.url" :proInfo="item"></projectitem>
    <newprojectitem v-if="ifAdmin === 'admin'"></newprojectitem>
  </div>
</template>

<script>
import projectitem from "@/components/allproject/projectitem";
import newprojectitem from "@/components/newproject/newprojectitem";
export default {
  components: {
    projectitem,
    newprojectitem
  },
  data() {
    return{
      ifAdmin: '',
      projectData: []
    }
  },
  created(){
    this.getAllProject()
    this.getUserInfo()
  },
  methods: {
    getAllProject(){
      this.$http.get('v1/tasks',{
        params: {
          pagesize: 9,
          page: 1
        }
      }).then((res)=>{
        console.log(res);
        this.projectData = res.data.results
      })
    },
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
  .item-box {
    margin: 10px 60px 0 60px;
  }
</style>
