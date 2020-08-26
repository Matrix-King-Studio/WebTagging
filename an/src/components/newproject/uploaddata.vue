<template>
  <div class="upload-box">
    <input type="file" ref="getfile" class="choose" @change="getFile($event)" multiple="multiple">
    <div class="to-choose" ref="dropBox" @click="toGetFile" @drop="dropFile">
      <span>拖拽或点击上传</span>
      <span class="note">支持图片或者zip压缩包</span>
      <div class="choose-progress"></div>
    </div>
    <div class="chosen-files">
      <div class="header">
        <span class="name">文件名</span>
        <span class="type">文件类型</span>
        <span class="size">文件大小</span>
      </div>
      <div class="file-info" v-for="(item, index) in fileList" :key="item.name">
        <span class="file-name">{{ item.name }}</span>
        <span class="file-type">{{ item.type | typeFormat }}</span>
        <span class="file-size">{{ item.size | sizeFormat }}</span>
        <div class="delete" @click="deleteData(index)">
          <i class="el-icon-delete"></i>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  filters: {
    //判断文件类型
    typeFormat(msg){
      if(msg.search('zip') !== -1){
        return 'zip'
      } else if(msg.search('jpg') !== -1 || msg.search('jpeg') !== -1){
        return 'jpg'
      } else if(msg.search('png') !== -1){
        return 'png'
      } else {
        return '未知'
      }
    },
    //判断文件大小
    sizeFormat(msg){
      if(msg < 1000000){
        return (msg/1000).toFixed(1) + 'KB'
      } else if(msg > 1000000){
        return (msg/1000000).toFixed(1) + 'MB'
      }
    }
  },
  data () {
    return{
      fileList: [
      ]
    }
  },
  created() {
    //下面两个是阻止浏览器默认打开拖拽进来的图片
    document.addEventListener('drop', function (e) {
      e.preventDefault()
    }, false)
    document.addEventListener('dragover', function (e) {
      e.preventDefault()
    }, false)
    //每次转到这个页面都从store中加载一次数据
    this.getFileData()
  },
  methods: {
    //用另一个点击去触发input:file按钮的点击效果
    toGetFile(){
      this.$refs.getfile.dispatchEvent(new MouseEvent('click'))
    },
    //获取文件信息
    getFile(event){
      this.fileList.push(...event.target.files)

      //以后再解决上传文件重复的问题吧

      this.$store.commit('saveFileList', this.fileList)
    },
    //拖拽上传
    dropFile(e){
      e.preventDefault()

      let files = [];
      [].forEach.call(e.dataTransfer.files, function(file) {
        files.push(file);
      },false);
      this.fileList.push(...files)
      this.$store.commit('saveFileList', this.fileList)
    },
    //获取store中的文件列表数据
    getFileData(){
      this.fileList = this.$store.state.allFileList
    },
    //删除文件列表中的数据
    deleteData:function(index){
      this.$delete(this.fileList, index)
      this.$store.commit('saveFileList', this.fileList)
    }
  },
}
</script>
<style lang="less" scoped>
.upload-box{
  width: 100%;
  height: 460px;
  position: relative;
  .choose{
    display: none;
  }
  .to-choose{
    position: absolute;
    left: 0;
    width: 400px;
    height: 100%;
    border: 2px dashed #aceedb;
    box-sizing: border-box;
    border-radius: 30px;
    background-color: #ecf5f3;
    text-align: center;
    line-height: 440px;
    font-size: 28px;
    color: #7c8786;
    .choose-progress{
      position: absolute;
      bottom: 0;
      width: 100%;
      height: 100%;
      border-radius: 30px;
      background-color: rgba(172,238,219,0.5);
    }
    .note{
      width: 100%;
      height: 30px;
      position: absolute;
      bottom: 50px;
      left: 50%;
      transform: translateX(-50%);
      line-height: 30px;
      font-size: 14px;
    }
  }
  .to-choose:hover{
    border: 2px dashed #6fcdb2;
  }
  .chosen-files{
    position: absolute;
    border: 2px solid #aceedb;
    background-color: #ecf5f3;
    box-sizing: border-box;
    border-radius: 20px;
    height: 100%;
    width: 480px;
    right: 0;
    overflow: auto;
    .header{
      width: 100%;
      height: 30px;
      background-color: rgba(0,0,0,0.1);
      span{
        float: left;
        text-align: center;
        line-height: 30px;
      }
      .name{
        width: 216px;
      }
      .type{
        width: 105px;
      }
      .size{
        width: 105px;
      }
    }
    .file-info{
      height: 30px;
      width: 100%;
      transition: 0.2s;
      span{
        height: 30px;
        float: left;
        text-align: center;
        line-height: 30px;
        overflow: hidden;
      }
      .file-name{
        width: 216px;
        font-size: 14px;
      }
      .file-type{
        width: 105px;
      }
      .file-size{
        width: 105px;
      }
      .delete{
        float: left;
        height: 30px;
        width: 30px;
        color: rgba(0,0,0,0.3);
        transition: color 0.2s;
        text-align: center;
        line-height: 30px;
      }
      .delete:hover{
        color: rgba(0,0,0,0.9);
      }
    }
    .file-info:hover{
      background-color: rgba(0,0,0,0.1);
    }
  }

}
</style>
