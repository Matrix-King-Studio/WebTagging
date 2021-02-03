<template>
  <div class="item-box">
    <projectitem
      v-for="item in projectData"
      :key="ifAdmin ? item.id : item.segments[item.segIndex].jobs[0].id"
      :proInfo="item"
      :userInfo="ifAdmin"
      :ifOwner="item.ifOwner"
    ></projectitem>
    <newprojectitem v-if="ifAdmin"></newprojectitem>
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
    return {
      ifAdmin: '',
      projectData: [],
      page: 1,
    }
  },
  mounted() {
    this.getUserInfo()
  },
  methods: {
    getAllProject(userId) {
      this.$http.get('v1/tasks', {
        params: {
          pagesize: 10,
          page: this.page
        }
      }).then((res) => {
        console.log('2.获取第' + this.page + '页项目信息', res)
        //查找所有的项目
        for (let index = 0; index < res.data.results.length; index++) {
          //筛出由此用户创建的项目
          if(res.data.results[index].owner.id === userId){
            res.data.results[index].ifOwner = true
            this.projectData.push(res.data.results[index])
          } else if (res.data.results[index].segments[0] !== undefined) {
            //如果不是创建者，遍历job查看是否有被分配的项目
            for(let segIndex = 0; segIndex < res.data.results[index].segments.length; segIndex++){
              //如果只是一个job中的标注员，push一个job后继续查找后面的job
              if(res.data.results[index].segments[segIndex].jobs[0].assignee && res.data.results[index].segments[segIndex].jobs[0].assignee.id === userId){
                //将项目对象深拷贝
                let jobData = JSON.parse(JSON.stringify(res.data.results[index]))
                //添加对应的jobId 用于组件的循环渲染
                jobData.segIndex = segIndex
                this.projectData.push(jobData)
              }
            }
          }
        }
        if(this.page * 10 <  res.data.count) {
          this.page = this.page + 1
          this.getAllProject(userId)
        } else {
          console.log('3.项目信息获取完成,清洗后为', this.projectData)
        }
      })
    },
    getUserInfo() {
      this.$http.get('v1/users/self').then((res) => {
        this.ifAdmin = res.data.groups.indexOf('admin') !== -1;
        console.log('1.1.获取用户信息, 用户id:' + res.data.id + '用户是否是管理员:' + this.ifAdmin);
        res.data.ifAdmin = this.ifAdmin
        this.$store.commit('saveUserInfo', res.data)
        return new Promise(resolve => {
          resolve(res.data)
        })
      }).then(value => {
        this.getAllProject(value.id)

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
