<template>
  <div class="setting-page">
    <div class="task-info">
      <div class="basic-info-box">
        <div
          v-if="taskInformation.results"
          class="task-name"
        >
          <span>项目名：{{ taskInformation.results[0].name }}</span>
        </div>
        <div
          v-if="taskInformation.results"
          class="basic-info"
        >
          <div class="info">
            <div>图像质量：{{ taskInformation.results[0].image_quality }}</div>
          </div>
          <div class="info">
            <div>图片数量：{{ taskInformation.results[0].size }}</div>
          </div>
          <div class="info">
            <div>创建时间：{{ taskInformation.results[0].created_date }}</div>
          </div>
          <div class="info">
            <div>更新时间：{{ taskInformation.results[0].updated_date }}</div>
          </div>
        </div>
        <div class="func-box">
          <div
            class="export-data func-btn"
            @click="exportTaggingDialogVisible = true"
          >
            <span>导出数据</span>
          </div>
          <div
            class="delete func-btn"
            @click="deleteTask"
          >
            <span>删除</span>
          </div>
        </div>
      </div>
      <div class="update-info-box">
        <div class="labels-box"/>
      </div>
    </div>
    <div class="jobs-info">
      <div
        v-for="item in jobsInfo"
        :key="item.jobs[0].id"
        class="job"
      >
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
        <div class="job-info">
          <div class="job-id info-box">
            <span v-text="item.jobs[0].id"/>
          </div>
          <div class="frames info-box">
            <span v-text="item.start_frame + '-' + item.stop_frame"/>
          </div>
          <div class="status info-box">
            <span v-text="whichStatus(item.jobs[0].status)"/>
          </div>
          <div class="start-time info-box">
            <span>无</span>
          </div>
          <div class="duration info-box">
            <span>无</span>
          </div>
          <div class="assignee info-box">
            <div class="select-box">
              <el-select
                  v-model="item.jobs[0].assignee.id"
                  filterable
                  size="mini"
                  placeholder="请选择"
                  @change="modifyJobAssign(item.index, item.jobs[0].assignee.id)"
              >
                <el-option
                    v-for="i in usersInfo"
                    :key="i.id"
                    :label="i.label"
                    :value="i.id"
                />
              </el-select>
            </div>
          </div>
        </div>
      </div>
    </div>
    <el-dialog
      title="提示"
      :visible.sync="exportTaggingDialogVisible"
      width="30%"
    >
      <span>
        <el-button
          v-for="item in exportTaggingFormat"
          :key="item.name"
          type="success"
          plain
          @click="updateData(item)"
        >{{ item.name }}</el-button>
      </span>
      <span
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          @click="exportTaggingDialogVisible = false"
        >取 消</el-button>
      </span>
    </el-dialog>
    <a href="" id="downloadAnchor"></a>
  </div>
</template>

<script>
export default {
  data() {
    return {
      /* Alex Start */
      exportTaggingDialogVisible: false,   // 是否显示导出标注数据 dialog
      exportTaggingFormat: [
        {name: 'COCO', format: 'COCO%201.0'},
        {name: 'YOLO', format: 'YOLO%201.1'},
        {name: 'PASCAL VOC', format: "PASCAL%20VOC%201.1"},
      ],
      taskInformation: {},
      /* Alex End */

      jobsInfo: [],
      usersInfo: []
    }
  },
  created() {
    this.getTaskInfo()
    this.getUsersInfo()
  },
  methods: {
    //job状态翻译函数
    /** 这个函数在projectitem中也有一个的，但是不会跨组件复用，只能再复制一个了*/
    whichStatus(status){
      if(status === 'annotation'){
        return '正在标注'
      } else if(status === 'validation'){
        return '正在质检'
      } else if(status === 'completed'){
        return '标注完成'
      }
    },
    //两个用于下载标注数据
    //两个用于下载标注数据
    updateData(item) {
      this.$http.get('v1/tasks/' + this.$route.params.index
          + '/annotations?format=' + item.format, {
        headers: {
          "Accept": "application/json, text/plain, */*",
          "Accept-Encoding": "gzip, deflate",
          "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        }
      }).then((e) => {
        console.log(e);
        if (e.status === 202) {
          this.updateData(item)
        } else if (e.status === 201) {
          return new Promise((resolve)=>{
            resolve(item)
          })
        }
      }).then(()=>{
        const downloadAnchor = window.document.getElementById('downloadAnchor');
        downloadAnchor.href = "http://47.102.205.231:8080/api/v1/tasks/" + this.$route.params.index + "/annotations?action=download&format=" + item.format;
        downloadAnchor.click();
        this.exportTaggingDialogVisible = false
      }).catch((err)=>{
        console.log(err);
      })
    },
    //删除项目
    deleteTask() {
      this.$confirm('确认删除该项目?', '注意', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$http.delete('v1/tasks/' + this.taskInformation.results[0].id).then((e)=>{
          console.log(e)
        })
        this.$message({
          type: 'success',
          message: '删除成功'
        })
        this.$router.push('/home')
      }).catch(() => {
        console.log('取消删除');
      });
    },

    // 获取 task 数据，用于 job 配置
    getTaskInfo() {
      this.$http.get('v1/tasks', {
        params: {

          /** 这个分页器的参数好像可以不填 */
          // page_size: 10,

          id: this.$route.params.index
        }
      }).then((e) => {
        this.taskInformation = e.data
        console.log('当前项目信息', this.taskInformation);
        this.jobsInfo = e.data.results[0].segments.map((job)=>{
          if(job.jobs[0].assignee === null){
            job.jobs[0].assignee = {id: null}
          }
          return job
        })
        console.log('当前所有job信息', this.jobsInfo);
        // this.$store.commit('saveAllJobs', this.jobsInfo)
        for (let i = 0; i < this.jobsInfo.length; i++) {
          this.jobsInfo[i]["index"] = i
        }
      })
    },
    //拿所有人员的数据用于分配任务
    getUsersInfo() {
      this.$http.get('v1/users?page_size=all').then((e) => {
        e.data.results.forEach((user, index) => {
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
    modifyJobAssign(index, id) {
      console.log(this.jobsInfo);
      console.log(index, id);
      this.$http.patch('v1/jobs/' + this.jobsInfo[index].jobs[0].id, {
        "assignee_id": id
      }).then((e) => {
        if (e.status === 200) {
          this.$message({
            message: "分配成功",
            type: "success"
          })
        }
      }).catch((e)=>{
        console.log('修改标注员失败', e);
      })
    }
  }
}
</script>

<style lang="less" scoped>
.setting-page {
  width: 100%;
  height: 100%;
  background-color: #e4f5ef;
  overflow: auto;

  .task-info, .jobs-info {
    width: 800px;
    height: 300px;
    margin: 30px auto;
    background-color: #f8f8f8;
    border-radius: 5px;
    border: 1px solid #9ce8d2;
    overflow: hidden;
  }

  .task-info {
    overflow: hidden;

    .basic-info-box {
      height: 100%;
      width: 300px;
      float: left;
      position: relative;

      .task-name {
        width: 100%;
        height: 60px;
        padding: 0 16px;
        overflow: hidden;

        span {
          font-size: 22px;
          line-height: 60px;
        }
      }

      .basic-info {
        width: 100%;
        height: 120px;
        box-sizing: border-box;
        padding-left: 16px;

        .info {
          width: 300px;
          height: 30px;
          float: left;

          div {
            width: 100%;
            height: 30px;
            line-height: 30px;
            font-size: 16px;
            font-weight: 500;
          }

          span {
            font-size: 14px;
            font-weight: 300;
          }
        }
      }

      .func-box {
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
          transition: 0.2s;
        }

        .func-btn:hover {
          background-color: #cfefe1;
        }

        .export-data {
          width: 100px;
        }

        .delete {
          width: 60px;
        }
      }
    }

    .update-info-box {
      height: 100%;
      width: 500px;
      float: right;
      //background-color: green;
    }
  }

  .jobs-info {
    height: auto;

    .job {
      width: 100%;
      height: 100px;
      background-color: #f8f8f8;
      border-bottom: 1px solid #9ce8d2;
      box-sizing: border-box;

      .job-title {
        height: 40px;
        width: 100%;
        display: flex;
        border-bottom: 1px solid #eeeeee;

        .title-box {
          text-align: center;
          line-height: 40px;
          font-size: 12px;
        }

        .job-id {
          flex: 1;
        }

        .frames {
          flex: 1;
        }

        .status {
          flex: 1;
        }

        .start-time {
          flex: 2;
        }

        .duration {
          flex: 1;
        }

        .assignee {
          flex: 2;
        }
      }

      .job-info {
        height: 60px;
        width: 100%;
        display: flex;

        .info-box {
          text-align: center;
          line-height: 60px;
          font-size: 14px;
        }

        .job-id {
          flex: 1;
        }

        .frames {
          flex: 1;
        }

        .status {
          flex: 1;
        }

        .start-time {
          flex: 2;
        }

        .duration {
          flex: 1;
        }

        .assignee {
          flex: 2;

          .select-box {
            width: 80%;
            margin: auto;
          }
        }
      }
    }
  }
}
</style>
