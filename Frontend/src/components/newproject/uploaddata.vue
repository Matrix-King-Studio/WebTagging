<template>
  <el-tabs type="border-card" value="one" :before-leave="leaveTab" :stretch=true>
    <el-tab-pane
      label="上传数据集"
      name="one"
      :disabled="tabOneCannotSelect">
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
    </el-tab-pane>
    <el-tab-pane
      label="使用已经存在的数据集"
      name="two"
      :disabled="tabTwoCannotSelect">
      <el-tree
        :props="props"
        :load="loadNode"
        lazy
        show-checkbox
        :highlight-current="true"
        @node-click="handleNodeClick"
        @check-change="handleCheckChange">
      </el-tree>
    </el-tab-pane>
  </el-tabs>
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
      ],
      //控制选项卡是否能切换
      tabOneCannotSelect: false,
      tabTwoCannotSelect: false,
      //树形控件用到的
      url: 'v1/server/share?directory=/',
      //treeData映射到elementUI的树形结构里的参数，name映射为label,children映射为children
      //isLeaf是否叶子节点，true是叶子节点，不显示下拉框；false非叶子节点，显示下拉框
      props: {
        label: 'name',
        children: 'children',
        isLeaf: 'leaf'
      },
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
    /** 以后再解决上传文件重复的问题*/
    getFile(event){
      this.fileList.push(...event.target.files)
      console.log(this.fileList);
      this.$store.commit('saveFileList', this.fileList)
    },
    //拖拽上传
    dropFile(e){
      e.preventDefault()

      let files = [];
      [].forEach.call(e.dataTransfer.files, function(file) {
        files.push(file)
      },false)
      this.fileList.push(...files)
      this.$store.commit('saveFileList', this.fileList)
    },
    //获取store中的文件列表数据
    getFileData(){
      this.fileList = this.$store.state.allFileList
    },
    //删除文件列表中的数据
    deleteData:function(index){
      this.$delete(this.fileList, index);
      this.$store.commit('saveFileList', this.fileList)
    },
    //tab切换
    leaveTab(activeName, oldActiveName){
        if (this.fileList.length !== 0){
            this.tabTwoCannotSelect = true;
            let p = new Promise((resolve, reject) => {
                this.$confirm('【上传数据集】与【使用已经存在的数据集】只能选择一个，如需切换请先清空数据！', '提示', {
                    showConfirmButton: false,
                    cancelButtonText: '我已了解',
                    type: 'warning'
                }).catch(err => {
                    this.tabTwoCannotSelect = false;
                    reject(err)
                })
            })
            return p
        }
    },
    //树形控件用到的方法
    handleCheckChange(data, checked, indeterminate) {
      console.log(data, checked, indeterminate);
      console.log(JSON.stringify(this.treeData));
    },
    //节点被点击触发的方法
    handleNodeClick() {
        // console.log(data);
    },
    // //树形结构url拼接
    // urlAdd(s1,s2){
    //   return s1+s2+'/'
    // },
    // //初始化树形结构内容
    // initTreeData(){
    //   //先获得最外层内容
    //   this.$http.get(this.url).then((res)=>{
    //       console.log(res.data);
    //       for(let i = 0; i<res.data.length;i++){
    //         let obj = {
    //           name: res.data[i].name,
    //           type: res.data[i].type,
    //           children: []
    //         };
    //         this.treeData.push(obj);
    //       }
    //   });
    //   //进行深层内容获取
    //   setTimeout(()=>{
    //       this.getTreeData(this.url,this.treeData)
    //   },400)
    // },
    // //树形结构通过url获取内容
    // getTreeData(v_url,v_data){
    //   // console.log(v_data[0].type);
    //   for (let i = 0; i < v_data.length; i++) {
    //     // console.log(v_data[i])
    //     if (v_data[i].type === 'DIR') {
    //       let tUrl = this.urlAdd(v_url,v_data[i].name);
    //       console.log(tUrl); //输出当前url
    //       this.addData(tUrl,v_data[i].children);
    //       setTimeout(()=>{
    //           this.getTreeData(tUrl,v_data[i].children)
    //       },400)
    //     }
    //   }
    // },
    // //树形结构添加数据
    // addData(v_url,v_data){
    //   this.$http.get(v_url).then((res)=>{
    //     for(let i = 0; i<res.data.length;i++){
    //       let obj = {
    //           name: res.data[i].name,
    //           type: res.data[i].type,
    //           children: []
    //       };
    //       v_data.push(obj);
    //     }
    //   })
    // },

    //节点懒加载方法
    loadNode(node, resolve) {
      if (node.level === 0) {
        this.$http.get(this.url).then((res)=>{
          let treeNode = [];
          if (res.data.length === 0){
              node.data.disabled=true;
              console.log(node.data.name + "文件夹内没有文件，无法选中");
          }
          else {
            for (let i = 0; i < res.data.length; i++) {
              let obj;
              if (res.data[i].type === 'DIR') {
                obj = {
                    name: res.data[i].name,
                    type: res.data[i].type,
                    nextUrl: this.url + res.data[i].name + '/',
                    leaf: false,
                    children: []
                };
              } else {
                obj = {
                    name: res.data[i].name,
                    type: res.data[i].type,
                    nextUrl: this.url + res.data[i].name + '/',
                    leaf: true,
                    children: []
                };
              }
              treeNode.push(obj);
            }
          }
          return resolve(treeNode);
        }).catch((res)=>{
            console.log(this.url + '获取数据失败');
            resolve([]);
        });
      }

      if (node.data){
        let hasChild;
        if (node.data.type === 'DIR') {
            hasChild = true;
        } else{
            hasChild = false;
        }
        let tUrl = node.data.nextUrl;
        setTimeout(() => {
          if (hasChild) {
            this.$http.get(tUrl).then((res)=>{
              let treeNode = [];
              if (res.data.length === 0){
                node.data.disabled=true;
                console.log(node.data.name + "文件夹内没有文件，无法选中");
              }
              else {
                for(let i = 0; i<res.data.length;i++) {
                  let obj;
                  if (res.data[i].type === 'DIR'){
                    obj = {
                      name: res.data[i].name,
                      type: res.data[i].type,
                      nextUrl: tUrl + res.data[i].name + '/',
                      leaf: false,
                      children: []
                    };
                  }else {
                    obj = {
                      name: res.data[i].name,
                      type: res.data[i].type,
                      nextUrl: tUrl + res.data[i].name + '/',
                      leaf: true,
                      children: []
                    };
                  }

                  treeNode.push(obj);
                }
              }
              return resolve(treeNode);
            }).catch((res)=>{
              console.log(tUrl + '获取数据失败');
              resolve([]);
            });
          } else {
              console.log(node.data.name + "不是文件夹，没有子文件")
              resolve([]);
          }
        }, 400);
      } else{
        console.log('node.data不存在')
      }
    },
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
    width: 380px;
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
