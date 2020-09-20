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

    </div>
  </div>
</template>

<script>
export default {
  data(){
    return{

    }
  },
  created() {

  },
  methods: {
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
    deleteTask(){
      console.log('delete');
    }
  }
}
</script>

<style lang="less" scoped>
.setting-page{
  width: 100%;
  height: 100%;
  background-color: #e4f5ef;
  overflow: hidden;
  .task-info,.jobs-info{
    width: 800px;
    height: 300px;
    margin: 30px auto;
    background-color: #f8f8f8;
    border-radius: 5px;
    border: 1px solid #9ce8d2;
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
}
</style>
