<template>
  <div class="module-box">
    <el-tabs type="border-card" @tab-click="getAllUsersInfo">
      <el-tab-pane label="选择标签">
        <!--      每一个label-box包着一个标签及其属性-->
        <div class="label-box" v-for="tag in labels" :key="tag.name">
          <!--        tab-box包着一级标签的名字-->
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
          <!--        attributes-box包着属性及其创建-->
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
        <el-transfer
          v-model="userValue"
          filterable
          :filter-method="searchMethod"
          filter-placeholder="搜索"
          :data="userData"
          :titles="['所有人员', '参与人员']"
          @change="saveUserInfo"
        >
        </el-transfer>
        <div class="segment-size-box">
          <div class="segment-size">
            <div class="minus-one">
              <i class="el-icon-minus"></i>
            </div>
            <div class="segment-size-number">
              <input type="text" v-model="segment_size">
            </div>
            <div class="plus-one">
              <i class="el-icon-plus"></i>
            </div>
          </div>
          <div class="segment-tip">
            <span class="tips">job数量</span><br>
            <span>将项目中的图片分为几份,后期可更改,默认等于参与人员数量,自定义时需要大于人员数量,小于图片数量</span>
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
            })
          })
        })
      }
    },
    //搜索策略
    searchMethod(query, item) {
      return item.label.indexOf(query) > -1;
    },
    //选定后保存到仓库
    saveUserInfo(){
      let allUsers = []
      for(let i = 0; i<this.userValue.length; i++){
        allUsers.push(this.userData[this.userValue[i]].key)
      }
      this.$store.commit('saveAllUsers',allUsers)
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
      margin: auto;
      overflow: hidden;
      text-align: center;
      .tips{
        font-size: 12px;
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
