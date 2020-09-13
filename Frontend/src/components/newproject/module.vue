<template>
  <div class="module-box">
    <el-tabs type="border-card">
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
      <el-tab-pane label="任务分配">任务分配</el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  created() {
    //转到选择标签时先从store中加载一遍labels
    this.loadData()
  },
  data(){
    return{
      //图像压缩质量
      image_quality: 70,
      //所有标签列表
      labels: [

      ],
      //控制添加标签输入框的变量
      mainInputVisible: false,
      mainInputValue: ''
    }
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
      this.$nextTick(_ => {
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
    },
    //提交imagequality
    pushImageQuality(){
      this.$store.commit('addImageQuality', this.image_quality)
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
}
</style>
