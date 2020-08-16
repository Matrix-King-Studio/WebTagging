<template>
  <div class="module-box">
    <span class="title-box">选择标签</span>
    <div class="main-box">
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
    </div>
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
      labels: [

      ],
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

    loadData(){
      this.labels = this.$store.state.projectInfo.labels
    }
  }
}
</script>
<style lang="less" scoped>
.module-box{
  width: 100%;
  .title-box{
    display: block;
    box-sizing: border-box;
    height: 40px;
    width: 120px;
    border-radius: 10px 10px 0 0;
    border: 1px solid #6fcdb2;
    border-bottom: 0;
    background-color: #e5f8f4;
    text-align: center;
    line-height: 40px;
    font-size: 16px;
  }
  .main-box{
    min-height: 200px;
    background-color: #e5f8f4;
    border-radius: 0 12px 12px 12px;
    border: 1px solid #6fcdb2;
    .label-box{
      margin: 10px 10px 0 10px;
      border: 1px solid #318B71;
      border-radius: 8px;
      display: inline-block;
      width: 880px;
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
    .button-new-tag{
      margin: 10px;
    }
    .input-new-tag{
      width: 880px;
      margin: 10px;
    }
  }
}
</style>
