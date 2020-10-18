<template>
  <div class="module-box">
    <el-tabs type="border-card" @tab-click="getAllUsersInfo">
      <el-tab-pane label="选择标签">
        <el-tabs active-name="raw">
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
                  @close="handleLabelClose(tag)"
                  class="tag"
                >
                  {{ tag.name }}
                </el-tag>
              </div>
              <div class="attribute-box">
                <div
                  v-show="!tag.attrInputVisible"
                  class="attr-item-box"
                >
                  <div
                    class="attribute-item"
                    v-for="attr in tag.attributes"
                    :key="attr.name"
                  >
                    <div class="attr-name">
                      <span></span>
                      <el-tag
                        closable
                        :disable-transitions="false"
                        :type="'success'"
                        @close="handleAttrClose(tag,attr)"
                      >
                        {{ attr.name }}
                      </el-tag>
                    </div>
                    <div class="attr-mod">

                    </div>
                    <div class="attr-value">

                    </div>
                    <div class="attr-delete">

                    </div>
                  </div>
                </div>
                <div
                  v-show="tag.attrInputVisible"
                  class="attr-input-box"
                >
                  <div class="input-box-tip">
                      <span>添加属性</span>
                  </div>
                  <div class="input-box-content">
                    <div class="attr-name-input-box">
                      <div class="attr-name-input">
                        <el-input
                          v-model="tag.attrInputValue"
                          placeholder="属性名"
                        ></el-input>
                      </div>
                    </div>
                    <div class="attr-mod-select-box">
                      <div class="attr-mod-select">
                        <el-select v-model="attrOption" placeholder="请选择">
                          <el-option
                            v-for="item in options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                          >
                          </el-option>
                        </el-select>
                      </div>
                    </div>
                    <div class="attr-value-input-box">
                      <div class="attr-value-input" @click="attrValInputFocus($event)">
                        <el-tag
                          :key="attrVal"
                          v-for="attrVal in newAttributeData.values"
                          class="attr-val-item"
                          closable
                          effect="plain"
                          type="success"
                          :disable-transitions="false"
                          @close="handleClose(attrVal)">
                          {{ attrVal }}
                        </el-tag>
                        <div contenteditable="true" class="val-input"></div>
                      </div>
                    </div>
                    <div class="attr-input-confirm-box">
                      <div class="attr-input-confirm">
                        <el-button type="success" plain icon="el-icon-check" size="small"></el-button>
                      </div>
                    </div>
                  </div>
                </div>
                <el-button v-show="!tag.attrInputVisible" class="button-new-tag" size="small" @click="showInput(2, tag)">+ 添加属性</el-button>
              </div>
            </div>
            <el-input
              v-if="mainInputVisible"
              v-model="mainInputValue"
              ref="mainSaveTagInput"
              class="input-new-tag"
              size="small"
              @keyup.enter.native="inputBlur($event)"
              @blur="handleInputConfirm()"
            >
            </el-input>
            <el-button v-else class="button-new-tag" size="small" @click="showInput(1)">+ 添加标签</el-button>
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

      //标签的序号
      labelIndex: 1,

      //新建属性中选择属性标注模式的选项
      options: [{
        value: '选项1',
        label: '黄金糕'
      }, {
        value: '选项2',
        label: '双皮奶'
      }, {
        value: '选项3',
        label: '蚵仔煎'
      }, {
        value: '选项4',
        label: '龙须面'
      }, {
        value: '选项5',
        label: '北京烤鸭'
      }],
      attrOption: '',
      attrValue: '',
      //新建属性
      newAttributeData: {
        id: 0,
        name: '',
        input_type: '',
        mutable: false,
        values: [
          "123",
          "12",
          "1",
          "143",
          "345",
          "567245",
        ],
      },
    }
  },
  created() {
    //转到选择标签时先从store中加载一遍labels
    this.loadData()
  },
  methods: {
    //删除标签
    handleLabelClose(tag) {
      this.labels.splice(this.labels.indexOf(tag), 1);
      this.$store.commit('addToStore', this.labels)
    },
    handleAttrClose(tag,attr){
      console.log(tag);
      console.log(attr);
      this.labels[this.labels.indexOf(tag)].attributes.splice(this.labels[this.labels.indexOf(tag)].attributes.indexOf(attr), 1)
    },
    //开始添加 标签：1/属性：2
    showInput(mod, tag) {
      if(mod === 1){
        this.mainInputVisible = true;
        this.$nextTick(() => {
          this.$refs.mainSaveTagInput.$refs.input.focus()
        })
      } else if(mod === 2){
        tag.attrInputVisible = true
      }
    },
    //回车失去焦点以触发
    inputBlur(e){
      e.srcElement.blur()
    },
    //点击添加属性里的属性值方框对其中的input进行聚焦
    attrValInputFocus(e){
      e.target.children[e.target.children.length - 1].focus()
    },
    //添加标签结束
    handleInputConfirm() {
      let inputValue = this.mainInputValue
      let labelIndex = this.labelIndex
      if (inputValue) {
        this.labels.push(
          {
            labelIndex: labelIndex,
            name: inputValue,
            attributes: [
            ],
            attrInputValue: '',
            attrInputVisible: false,
          }
        );
      }
      this.mainInputVisible = false;
      this.mainInputValue = '';
      console.log(this.labels);
      this.$store.commit('addToStore', this.labels)
    },
    //添加属性结束
    handleAttrConfirm(tag){
      if(tag.attrInputValue){
        this.labels[this.labels.indexOf(tag)].attributes.push({
          "name": tag.attrInputValue,
          "mutable": false,
          "input_type": 'select',
          "default_value": 'select',
          "values": []
        })
      }
      this.labels[this.labels.indexOf(tag)].attrInputVisible = false
      this.labels[this.labels.indexOf(tag)].attrInputValue = ''
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
    box-sizing: border-box;
    border: 1px solid #318B71;
    border-radius: 8px;
    margin: 10px 0;
    display: inline-block;
    width: 868px;
    overflow: hidden;
    .tab-box{
      width: 200px;
      .tag{
        display: block !important;
        border-radius: 0;
        border: 0;
        border-bottom: 1px solid #6fcdb2;
        background-color: transparent;
        color: #318B71;
        font-size: 16px;
      }
    }
    .attribute-box{
      width: 100%;
      box-sizing: border-box;
      .attribute-item{
        min-height: 46px;
        padding-top: 6px;
        box-sizing: border-box;
        display: flex;
        .attr-name{
          flex: 3;
        }
        .attr-value{
          flex: 5;
        }
        .attr-mod{
          flex: 1;
        }
        .attr-delete{
          flex: 1;
        }
      }
      .attr-input-box{
        min-height: 46px;
        border-radius: 3px;
        box-sizing: border-box;
        background-color: #edf8f3;
        .input-box-tip{
          width: 100%;
          height: 18px;
          padding: 4px 0 0 6px;
          line-height: 14px;
          span{
            font-size: 14px;
            color: #999;
          }
        }
        .input-box-content{
          display: flex;
          .attr-name-input-box{
            flex: 3;
            .attr-name-input{
              margin: 8px;
              height: 40px;
            }
          }
          .attr-mod-select-box{
            flex: 3;
            .attr-mod-select{
              margin: 8px;
              height: 40px;
            }
          }
          .attr-value-input-box{
            flex: 5;
            padding: 8px;
            max-width: 40%;
            cursor: text;
            .attr-value-input{
              min-height: 40px;
              background-color: #fff;
              border: 1px solid #dcdfe6;
              box-sizing: border-box;
              display: flex;
              flex-wrap: wrap;
              transition: border .2s ease;
              .attr-val-item{
                margin: 4px 0 0 4px;
              }
              .val-input{
                display: inline-block;
                outline: none;
                margin: 4px;
                height: 32px;
                padding: 0;
                line-height: 32px;
                min-width: 1em;
                max-width: 100%;
                overflow: hidden;
                white-space: nowrap;
              }
            }
            .attr-value-input:hover{
              border: 1px solid #c2c3c6;
            }
          }
          .attr-input-confirm-box{
            flex: 1;
            .attr-input-confirm{
              margin: 12px;
              height: 40px;
            }
          }
        }
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
    width: 90%;
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
