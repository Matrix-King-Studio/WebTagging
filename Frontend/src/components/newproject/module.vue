<template>
  <div class="module-box">
    <el-tabs type="border-card" @tab-click="getAllUsersInfo">
      <el-tab-pane label="选择标签">
        <el-tabs active-name="raw" @tab-click="handleClick">
          <el-tab-pane class="raw-label-box" label="Row格式添加" name="raw">
            <textarea cols="30" rows="10" class="raw-label">

            </textarea>
          </el-tab-pane>
          <el-tab-pane label="手动添加" name="ac">
            <div class="label-box" v-for="tag in labels" :key="tag.name">
              <div class="tab-box">
                <el-tag
                  closable
                  :disable-transitions="false"
                  @close="handleClose(tag)"
                  class="tag"
                >
                  {{ tag.name }}
                </el-tag>
              </div>
              <div class="attribute-box">
                <!--          <el-tag-->
                <!--            v-for="attr in tag.attributes"-->
                <!--            :key="attr"-->
                <!--            closable-->
                <!--            :disable-transitions="false"-->
                <!--            @close="handleAttrClose(attr.name)"-->
                <!--          >-->
                <!--            {{ attr.name }}-->
                <!--          </el-tag>-->
                <!--          <el-input-->
                <!--            v-if="tag.attrInputVisible"-->
                <!--            v-model="tag.attrInputValue"-->
                <!--            ref="saveTagInput"-->
                <!--            class="input-new-tag"-->
                <!--            size="small"-->
                <!--            @keyup.enter.native="handleInputConfirm"-->
                <!--            @blur="handleInputConfirm"-->
                <!--          >-->
                <!--          </el-input>-->
                <el-button class="button-new-tag" size="small">+ 添加属性(之后支持)</el-button>
              </div>
            </div>
            <el-input
              v-if="mainInputVisible"
              v-model="mainInputValue"
              ref="mainSaveTagInput"
              class="input-new-tag"
              size="small"
              @keyup.enter.native="handleInputConfirm"
              @blur="handleInputConfirm"
            >
            </el-input>
            <el-button v-else class="button-new-tag" size="small" @click="showInput">+ 添加标签</el-button>
          </el-tab-pane>
        </el-tabs>
      </el-tab-pane>
      <el-tab-pane label="图像质量">
        <span class="image-quality-text">图片压缩质量({{image_quality}}%)</span>
        <el-slider
          v-model="image_quality"
          :step="5"
          show-stops
          class="slide-bar"
          :max="95"
          :min="5"
          :change="pushImageQuality()"
        >
        </el-slider>
      </el-tab-pane>
      <el-tab-pane label="任务分配">
<!--        <el-transfer-->
<!--          v-model="userValue"-->
<!--          filterable-->
<!--          :filter-method="searchMethod"-->
<!--          filter-placeholder="搜索"-->
<!--          :data="userData"-->
<!--          :titles="['所有人员', '参与人员']"-->
<!--          @change="saveUserInfo"-->
<!--        >-->
<!--        </el-transfer>-->
        <div class="segment-size-box">
          <div class="segment-size">
            <div class="minus-one" @click="changeSeg('minus')">
              <i class="el-icon-minus"></i>
            </div>
            <div class="segment-size-number" @change="changeSeg('modify')">
              <input type="text" v-model="segment_size">
            </div>
            <div class="plus-one" @click="changeSeg('plus')">
              <i class="el-icon-plus"></i>
            </div>
          </div>
          <div class="segment-tip">
            <span class="tips">一个job中图片的数量</span><br>
            <span>将项目中的图片分为若干份，每份有多少张图片,默认为所有图片数量，即不将项目进行分割</span>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  data(){
    return{

      //图像压缩质量
      image_quality: 70,
      //所有标签列表
      labels: [

      ],
      //控制添加标签输入框的变量
      mainInputVisible: false,
      mainInputValue: '',

      //任务分配数据
      userData: [],
      userValue: [],

      //
      segment_size: 1,

      //


    }
  },
  created() {
    //转到选择标签时先从store中加载一遍labels
    this.loadData()
  },
  methods: {
    //删除标签
    handleClose(tag) {
      this.labels.splice(this.labels.indexOf(tag), 1);
      this.$store.commit('addToStore', this.labels)
    },
    //开始添加标签
    showInput() {
      this.mainInputVisible = true;
      this.$nextTick(() => {
        this.$refs.mainSaveTagInput.$refs.input.focus();
      });
    },
    //添加标签结束
    handleInputConfirm() {
      let inputValue = this.mainInputValue;
      if (inputValue) {
        this.labels.push(
          {
            name: inputValue,
            attributes: [
              {
                "name": 'select',
                "mutable": false,
                "input_type": 'select',
                "default_value": 'select',
                "values": []
              }
            ]
          }
        );
      }
      this.mainInputVisible = false;
      this.mainInputValue = '';
      this.$store.commit('addToStore', this.labels)
    },
    //从仓库加载数据
    loadData(){
      this.labels = this.$store.state.projectInfo.labels
      this.image_quality = this.$store.state.image_quality
      this.userValue = this.$store.state.allUsers

      //加载人员的同时重新求job数量，保证segment_size至少为1
      if(this.userValue.length === 0){
        this.segment_size = 1
      } else {
        this.segment_size = this.userValue.length
      }
    },
    //提交imageQuality
    pushImageQuality(){
      this.$store.commit('addImageQuality', this.image_quality)
    },
    //获取人员信息
    getAllUsersInfo(event){
      if(event.label === "任务分配"){
        //清除原有数据
        this.userData = []
        //获取加载数据
        this.$http.get('v1/users?page_size=all').then((e)=>{
          e.data.results.forEach((user, index)=>{
            this.userData.push({
              label: user.username,
              key: index,
              id: user.id
            })
          })
        })
      }
    },
    //搜索策略 穿梭框使用
    searchMethod(query, item) {
      return item.label.indexOf(query) > -1;
    },
    //参与人员选定后保存到仓库
    saveUserInfo(){
      let allUsers = []
      //根据成员数改变job数
      this.changeSeg('users')

      for(let i = 0; i<this.userValue.length; i++){
        allUsers.push(this.userData[this.userValue[i]].key)
      }
      this.$store.commit('saveAllUsers',allUsers)
    },
    //修改segment
    //mod: 1.plus 点击+1 2.minus 点击-1 3.modify直接修改 4. 穿梭框变化时的修改
    changeSeg(mod){

      /**如果没有传图片先点这个会有undefined报错*/
      // console.log(this.$store.state.allFileList.length);
      // console.log(this.$store.state.allFileList[0].type.indexOf("zip"))
      //如果传图片最大值是图片个数,如果是压缩包，最大值是999(因为无法判断压缩包内的图片数量)
      let MAX = 999
      if(this.$store.state.allFileList.length === 0){
        this.$message({
          message: "请先添加图片数据",
          type: "error"
        })
        return //跳出函数不再继续执行
      } else if(this.$store.state.allFileList[0].type.indexOf("zip") === -1) {
        MAX = this.$store.state.allFileList.length
      }

      if(mod === 'plus'){
        if(this.segment_size < MAX){
          this.segment_size = parseInt(this.segment_size) + 1
        } else {
          this.$message({
            message: '不能超过图片数量',
            type: "warning"
          })
        }
      } else if(mod === 'minus'){
        if(this.segment_size > 1){
          this.segment_size = parseInt(this.segment_size) - 1
        }
      } else if(mod === 'modify'){
        if(this.segment_size < 1 || this.segment_size > MAX){
          this.$message({
            message: '非法数值，请重新输入',
            type: "warning"
          })
          //警告结束后改为默认值
          if(this.userValue.length === 0){
            this.segment_size = 1
          } else{
            this.segment_size = this.userValue.length
          }
        }
      } else if(mod === 'users'){
        if(this.userValue.length === 0){//如果没有指定人员
          this.segment_size = 1
        } else if(this.userValue.length > MAX){
          this.$message({
            message: '人员数量超过图片数量',
            type: "error"
          })
        } else {//jog数量等于人员数量
          this.segment_size = this.userValue.length
        }
      }

      this.$store.commit('saveSeg', this.segment_size)
    }
  }
}
</script>
<style lang="less" scoped>
.module-box{
  width: 100%;
  .el-tabs--border-card {
    border: 1px solid #6fcdb2;
    border-radius: 10px;
    box-shadow: none !important;
    overflow: hidden;
  }
  .label-box{
    border: 1px solid #318B71;
    border-radius: 8px;
    margin: 10px 0;
    display: inline-block;
    width: 868px;
    .tab-box{
      width: 200px;
      .tag{
        display: block !important;
        border-radius: 0;
        border: 0;
        border-bottom: 1px solid #6fcdb2;
        background-color: transparent;
        color: #318B71;
      }
    }
    .attribute-box{
      width: 700px;
      float: left;
      .attribute{
        height: 32px;
        border-bottom: 1px solid #d9ecff;
      }
    }
  }
  .raw-label-box{
    width: 100%;
    .raw-label{
      width: 100%;
      resize: vertical;
      outline: none;
      overflow: auto;
      border-radius: 5px;
      border:1px solid #318B71;
      box-sizing: border-box;
    }
  }
  .slide-bar{
    width: 600px;
  }
  .image-quality-text{
    font-size: 16px;
    color: #55664e;
  }
  .button-new-tag{
    margin: 10px;
  }
  .input-new-tag{
    width: 868px;
    margin: 10px 0;
  }
  .segment-size-box{
    margin-top: 20px;
    height: 100px;
    width: 100%;
    .segment-size{
      height: 40px;
      width: 160px;
      margin: auto;
      border: 1px solid #c2e8cc;
      border-radius: 3px;
      line-height: 40px;
      text-align: center;
      display: flex;
      .minus-one{
        height: 100%;
        width: 40px;
      }
      .segment-size-number{
        height: 100%;
        width: 80px;
        background-color: lightblue;
        input{
          overflow: hidden;
          text-align: center;
          display: block;
          padding: 0;
          margin: 0;
          outline: none;
          height: 100%;
          width: 100%;
          border: 0;
        }
      }
      .plus-one{
        height: 100%;
        width: 40px;
      }
    }
    .segment-tip{
      height: 60px;
      width: 600px;
      margin: 10px auto 0 auto;
      overflow: hidden;
      text-align: center;
      .tips{
        color: #666666;
        font-size: 14px;
      }
      span{
        font-size: 6px;
        color: #999999;
      }
    }
  }
}
/deep/ .el-transfer-panel__filter{
  margin: 0;
}
/deep/ .el-input__inner{
  border-radius: 0;
}
/deep/ .el-transfer{
  width: 590px;
  margin: auto;
}
</style>
