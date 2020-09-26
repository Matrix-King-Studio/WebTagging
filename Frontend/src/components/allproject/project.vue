<template>
  <div class="item-box">
    <projectitem v-for="item in projectData" :key="item.url" :proInfo="item" :userInfo="ifAdmin"></projectitem>
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
      projectData: [],
      userId: 0,
    }
  },
  created(){
    this.getUserInfo()
  },
  mounted() {
    setTimeout(()=>{
      this.getAllProject()
    },100)
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
        for(let index = 0; index < res.data.results.length; index++){
          for(let i = 0; i < res.data.results[index].segments[0].jobs.length; i++){
            if(res.data.results[index].segments[0].jobs[i].assignee === this.userId || res.data.results[index].owner === this.userId){
              this.projectData.push(res.data.results[index])
            }
          }
        }
      })
    },
    getUserInfo(){
      this.$http.get('v1/users/self').then((res)=>{
        this.userId = res.data.id
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
