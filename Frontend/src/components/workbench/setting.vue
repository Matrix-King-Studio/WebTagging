<template>
  <div class="setting-page">
    <div class="task-info">
      <div class="basic-info-box">
        <div class="task-name">
          <span>项目名</span>
        </div>
        <div class="basic-info">
          <div class="info">
            <div>图像质量</div>
            <span>80</span>
          </div>
          <div class="info">
            <div>图片数量</div>
            <span>num</span>
          </div>
          <div class="info">
            <div>overlap-size</div>
            <span>0</span>
          </div>
          <div class="info">
            <div>z-order</div>
            <span>0</span>
          </div>
        </div>
        <div class="func-box">
          <div class="export-data func-btn" @click="updateData">
            <span>导出数据</span>
          </div>
          <div class="delete func-btn" @click="deleteTask">
            <span>删除</span>
          </div>
        </div>
      </div>
      <div class="update-info-box">
        <div class="labels-box"></div>
      </div>
    </div>
    <div class="jobs-info">
      <div class="job" v-for="item in jobsInfo" :key="item.jobs[0].id">
        <div class="job-title">
          <div class="job-id title-box">
            <span>jobId</span>
          </div>
          <div class="frames title-box">
            <span>图片范围</span>
          </div>
          <div class="status title-box">
            <span>状态</span>
          </div>
          <div class="start-time title-box">
            <span>开始时间</span>
          </div>
          <div class="duration title-box">
            <span>时长</span>
          </div>
          <div class="assignee title-box">
            <span>标注人</span>
          </div>
        </div>
        <div class="job-info" >
          <div class="job-id info-box">
            <span v-text="item.jobs[0].id"></span>
          </div>
          <div class="frames info-box">
            <span v-text="item.start_frame + '-' + item.stop_frame"></span>
          </div>
          <div class="status info-box">
            <span v-text="item.jobs[0].status"></span>
          </div>
          <div class="start-time info-box">
            <span>undefined</span>
          </div>
          <div class="duration info-box">
            <span>undefined</span>
          </div>
          <div class="assignee info-box">
            <div class="select-box">
              <el-select
                v-model="item.jobs[0].assignee"
                filterable
                size="mini"
                placeholder="请选择"
                @change="modifyJobAssign(item.index)"
              >
                <el-option
                  v-for="i in usersInfo"
                  :key="i.key"
                  :label="i.label"
                  :value="i.id"
                >
                </el-option>
              </el-select>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data(){
    return{
      jobsInfo: [],
      usersInfo: []
    }
  },
  created() {
    this.getTaskInfo()
    this.getUsersInfo()
  },
  methods: {
    //两个用于下载标注数据
    updateData(){
      this.$http.get('v1/tasks/'+ this.$route.params.index +'/annotations?format=COCO%201.0',{
        responseType: 'blob'
      }).then((e)=>{
        console.log(e);
        if(e.status === 202){
          this.updateData()
        } else if(e.status === 201){
          this.downloadData()
        }
      })
    },
    downloadData(){
      this.$http.get('v1/tasks/'+ this.$route.params.index +'/annotations?action=download',{
        responseType: 'blob'
      }).then((res)=>{
        console.log(res);
        const blob = new Blob([res.data], {
          type: 'application/octet-stream'
        })
        let link = document.createElement('a')
        let body = document.querySelector('body')
        link.href = window.URL.createObjectURL(blob)
        console.log(link.href)
        link.style.display = 'none'
        body.appendChild(link)
        link.click()
        body.removeChild(link)
        window.URL.revokeObjectURL(link.href)
      })
    },
    //删除项目
    deleteTask(){
      console.log('delete');
    },
    //拿task数据用于job配置
    getTaskInfo(){
      this.$http.get('v1/tasks',{
        params: {
          page_size: 10,
          id: this.$route.params.index
        }
      }).then((e)=>{
        console.log(e);
        this.jobsInfo = e.data.results[0].segments
        for(let i = 0; i<this.jobsInfo.length; i++){
          this.jobsInfo[i]["index"] = i
        }
        console.log(this.jobsInfo);
      })
    },
    //拿所有人员的数据用于分配任务
    getUsersInfo(){
      this.$http.get('v1/users?page_size=all').then((e)=>{
        e.data.results.forEach((user, index)=>{
          this.usersInfo.push({
            label: user.username,
            key: index,
            id: user.id
          })
        })
        // console.log(this.usersInfo);
      })
    },
    //点选之后patch修改后端数据
    modifyJobAssign(index){
      this.$http.patch('v1/jobs/'+this.jobsInfo[index].jobs[0].id,{
        "status":"annotation",
        "assignee":this.jobsInfo[index].jobs[0].assignee
      }).then((e)=>{
        if(e.status === 200){
          this.$message({
            message: "修改成功",
            type: "success"
          })
        }
      })
      console.log(this.jobsInfo);
    }
  }
}
</script>

<style lang="less" scoped>
.setting-page{
  width: 100%;
  height: 100%;
  background-color: #e4f5ef;
  overflow: auto;
  .task-info,.jobs-info{
    width: 800px;
    height: 300px;
    margin: 30px auto;
    background-color: #f8f8f8;
    border-radius: 5px;
    border: 1px solid #9ce8d2;
    overflow: hidden;
  }
  .task-info{
    overflow: hidden;
    .basic-info-box{
      height: 100%;
      width: 240px;
      float: left;
      position: relative;
      .task-name{
        width: 100%;
        height: 60px;
        padding: 0 16px;
        overflow: hidden;
        span{
          font-size: 22px;
          line-height: 60px;
        }
      }
      .basic-info{
        width: 100%;
        height: 120px;
        box-sizing: border-box;
        padding-left: 16px;
        .info{
          width: 110px;
          height: 60px;
          float: left;
          div{
            width: 100%;
            height: 30px;
            line-height: 30px;
            font-size: 16px;
            font-weight: 500;
          }
          span{
            font-size: 14px;
            font-weight: 300;
          }
        }
      }
      .func-box{
        position: absolute;
        bottom: 0;
        width: 100%;
        height: 80px;
        box-sizing: border-box;
        padding: 20px 0;
        .func-btn {
          height: 40px;
          float: left;
          background-color: #a8e0c6;
          border-radius: 3px;
          margin-left: 30px;
          text-align: center;
          line-height: 40px;
          cursor: pointer;
          transition: 0.2s ;
        }
        .func-btn:hover{
          background-color: #cfefe1;
        }
        .export-data{
          width: 100px;
        }
        .delete{
          width: 40px;
        }
      }
    }
    .update-info-box{
      height: 100%;
      width: 560px;
      float: left;
      //background-color: green;
    }
  }
  .jobs-info{
    height: auto;
    .job{
      width: 100%;
      height: 100px;
      background-color: #f8f8f8;
      border-bottom: 1px solid #9ce8d2;
      box-sizing: border-box;
      .job-title{
        height: 40px;
        width: 100%;
        display: flex;
        border-bottom: 1px solid #eeeeee;
        .title-box{
          text-align: center;
          line-height: 40px;
          font-size: 12px;
        }
        .job-id{
          flex: 1;
        }
        .frames{
          flex: 1;
        }
        .status{
          flex: 1;
        }
        .start-time{
          flex: 2;
        }
        .duration{
          flex: 1;
        }
        .assignee{
          flex: 2;
        }
      }
      .job-info{
        height: 60px;
        width: 100%;
        display: flex;
        .info-box{
          text-align: center;
          line-height: 60px;
          font-size: 14px;
        }
        .job-id{
          flex: 1;
        }
        .frames{
          flex: 1;
        }
        .status{
          flex: 1;
        }
        .start-time{
          flex: 2;
        }
        .duration{
          flex: 1;
        }
        .assignee{
          flex: 2;
          .select-box{
            width: 80%;
            margin: auto;
          }
        }
      }
    }
  }
}
</style>
