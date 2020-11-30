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
        console.log('2.获取第' + this.page + '页项目信息', res);
        //查找所有的项目
        for (let index = 0; index < res.data.results.length; index++) {
          //筛选 掉 没有分配的项目
          if (res.data.results[index].segments[0] !== undefined) {
            for (let i = 0; i < res.data.results[index].segments[0].jobs.length; i++) {
              //筛选 出 是拥有者或者是被分配的项目
              if (res.data.results[index].segments[0].jobs[i].assignee === userId || res.data.results[index].owner === userId) {
                this.projectData.push(res.data.results[index])
              }
            }
          }
        }
        if(this.page * 10 <  res.data.count) {
          this.page = this.page + 1
          this.getAllProject(userId)
        } else {
          console.log('3.项目信息获取完成');
        }
      })
    },
    getUserInfo() {
      this.$http.get('v1/users/self').then((res) => {
        this.ifAdmin = res.data.groups.find(val => {
          return val === 'admin'
        })
        console.log('1.获取用户信息完成, 用户id:' + res.data.id);
        return new Promise(resolve => {
          resolve(res.data.id)
        })
      }).then(value => {
        this.getAllProject(value)
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
