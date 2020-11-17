<template>
  <div class="module-box">
    <el-tabs type="border-card" @tab-click="getAllUsersInfo">
      <el-tab-pane label="选择标签">
        <el-tabs active-name="raw">
          <el-tab-pane class="raw-label-box" label="Raw格式添加" name="raw">
            <textarea v-model="labelValues" cols="30" rows="10" class="raw-label"></textarea>
            <JsonViewer
              :value="jsonData"
              :expand-depth=5
              copyable
              boxed></JsonViewer>
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
                    :key="attr.id"
                  >
                    <div class="attr-name">
                      <span>
                        {{ attr.name }}
                      </span>
                    </div>
                    <div class="attr-mod">
                      <span>
                        {{ attr.input_type }}
                      </span>
                    </div>
                    <div class="attr-value">
                      <span>
                        {{ attr.values }}
                      </span>
                    </div>
                    <div class="attr-edit-box">
                      <div class="attr-edit">
                        <i class="el-icon-edit" @click="editAttrInfo(tag,attr)"></i>
                      </div>
                      <div class="attr-delete">
                        <i class="el-icon-delete" @click="handleAttrClose(tag,attr)"></i>
                      </div>
                    </div>
                  </div>
                </div>
                <div
                  v-show="tag.attrInputVisible"
                  class="attr-input-box"
                >
                  <div class="input-box-tip">
                    <span>添加属性</span>
                    <i class="el-icon-close" @click="endAttrInput(tag)"></i>
                  </div>
                  <div class="input-box-content">
                    <div class="attr-name-input-box">
                      <div class="attr-name-input" ref="attr_name_input">
                        <el-input
                          v-model="newAttributeData.name"
                          placeholder="属性名"
                        ></el-input>
                      </div>
                    </div>
                    <div class="attr-mod-select-box">
                      <div class="attr-mod-select" ref="attr_mod_select">
                        <el-select v-model="newAttributeData.input_type" placeholder="请选择">
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
                      <div class="attr-value-input" ref="attr_value_input" @click="attrValInputFocus($event)">
                        <el-tag
                          :key="attrVal"
                          v-for="attrVal in newAttributeData.values"
                          class="attr-val-item"
                          closable
                          effect="plain"
                          type="success"
                          @close="handleAttrValClose(attrVal)">
                          {{ attrVal }}
                        </el-tag>
                        <div
                          contenteditable="true"
                          class="val-input"
                          @keydown.enter="inputBlur($event)"
                          @blur="handleAttrValInput($event)"
                        ></div>
                      </div>
                    </div>
                    <div class="attr-input-confirm-box">
                      <div class="attr-input-confirm">
                        <el-button type="success" plain icon="el-icon-check" size="small"
                                   @click="handleAttrConfirm(tag)"></el-button>
                      </div>
                    </div>
                  </div>
                </div>
                <el-button v-show="!tag.attrInputVisible" class="button-new-tag" size="small"
                           @click="showInput(2, tag)">+ 添加属性
                </el-button>
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
        <span class="image-quality-text">图片压缩质量({{ image_quality }}%)</span>
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
import 'vue-json-viewer/style.css'
import JsonViewer from 'vue-json-viewer'

export default {
  components: {
    JsonViewer
  },
  computed: {
    //使用raw格式获取仓库中的数据，更改仓库中的数据
    labelValues: {
      get() {
        return JSON.stringify(this.$store.state.projectInfo.labels)
      },
      set(val) {
        this.$store.commit("updateLabels", val)
        // this.loadData()
      }
    }
  },
  data() {
    return {
      jsonData: {
        total: 25,
        limit: 10,
        skip: 0,
        links: {
          previous: undefined,
          next: function () {},
        },
        data: [
          {
            id: '5968fcad629fa84ab65a5247',
            firstname: 'Ada',
            lastname: 'Lovelace',
            awards: null,
            known: [
              'mathematics',
              'computing'
            ],
            position: {
              lat: 44.563836,
              lng: 6.495139
            },
            description: `Augusta Ada King, Countess of Lovelace (née Byron; 10 December 1815 – 27 November 1852) was an English mathematician and writer,
            chiefly known for her work on Charles Babbage's proposed mechanical general-purpose computer,
            the Analytical Engine. She was the first to recognise that the machine had applications beyond pure calculation,
            and published the first algorithm intended to be carried out by such a machine.
            As a result, she is sometimes regarded as the first to recognise the full potential of a "computing machine" and the first computer programmer.`,
            bornAt: '1815-12-10T00:00:00.000Z',
            diedAt: '1852-11-27T00:00:00.000Z'
          }, {
            id: '5968fcad629fa84ab65a5246',
            firstname: 'Grace',
            lastname: 'Hopper',
            awards: [
              'Defense Distinguished Service Medal',
              'Legion of Merit',
              'Meritorious Service Medal',
              'American Campaign Medal',
              'World War II Victory Medal',
              'National Defense Service Medal',
              'Armed Forces Reserve Medal',
              'Naval Reserve Medal',
              'Presidential Medal of Freedom'
            ],
            known: null,
            position: {
              lat: 43.614624,
              lng: 3.879995
            },
            description: `Grace Brewster Murray Hopper (née Murray; December 9, 1906 – January 1, 1992)
            was an American computer scientist and United States Navy rear admiral.
            One of the first programmers of the Harvard Mark I computer,
            she was a pioneer of computer programming who invented one of the first compiler related tools.
            She popularized the idea of machine-independent programming languages, which led to the development of COBOL,
            an early high-level programming language still in use today.`,
            bornAt: '1815-12-10T00:00:00.000Z',
            diedAt: '1852-11-27T00:00:00.000Z'
          }
        ]
      },

      //图像压缩质量
      image_quality: 70,
      //所有标签列表
      labels: [],
      //控制添加标签输入框的变量
      mainInputVisible: false,
      mainInputValue: '',

      //任务分配数据
      userData: [],
      userValue: [],

      //分配任务
      segment_size: 1,
      //
      labelIndex: 1,
      //编辑标签中的属性
      isEditAttr: false,
      beingEditAttrIndex: -1,

      //新建属性中选择属性标注模式的选项
      options: [{
        value: 'select',
        label: '下拉框选择'
      }, {
        value: 'checkbox',
        label: '选择是否有该值'
      }, {
        value: 'text',
        label: '手动输入文本'
      }, {
        value: 'number',
        label: '手动输入数字'
      }],
      attrOption: '',
      attrValue: '',

      attrIndex: 1,

      //新建属性
      newAttributeData: {
        "id": 0,
        "name": '',
        "input_type": '',
        "mutable": false,
        "values": [],
      },

    }
  },
  created() {
    //转到选择标签时先从store中加载一遍labels
    this.loadData()
  },
  methods: {
    //
    updateLabels(e) {
      this.$store.commit('updateLabels', e.target.value)
    },
    /** 记得解决重复值问题*/
    //删除 标签/属性/属性值
    handleLabelClose(tag) {
      this.labels.splice(this.labels.indexOf(tag), 1);
      this.$store.commit('addToStore', this.labels)
    },
    handleAttrClose(tag, attr) {
      this.labels[this.labels.indexOf(tag)].attributes.splice(this.labels[this.labels.indexOf(tag)].attributes.indexOf(attr), 1)
    },
    handleAttrValClose(attrVal) {
      this.newAttributeData.values.splice(this.newAttributeData.values.indexOf(attrVal), 1)
    },
    //开始添加 标签：1/属性：2
    showInput(mod, tag) {
      if (mod === 1) {
        this.mainInputVisible = true;
        this.$nextTick(() => {
          this.$refs.mainSaveTagInput.$refs.input.focus()
        })
      } else if (mod === 2) {
        for (let i = 0; i < this.labels.length; i++) {
          this.labels[i].attrInputVisible = false
        }
        console.log("开始添加属性", tag);
        tag.attrInputVisible = true
      }
    },
    //回车失去焦点以触发添加方法
    inputBlur(e) {
      e.srcElement.blur()
      e.preventDefault()
    },
    //添加标签结束
    handleInputConfirm() {
      let inputValue = this.mainInputValue
      if (inputValue) {
        this.labels.push(
          {
            name: inputValue,
            id: this.labelIndex,
            attributes: [],
            attrInputVisible: false,
          }
        );
      }
      this.mainInputVisible = false;
      this.mainInputValue = '';
      console.log("添加标签成功", this.labels);
      this.$store.commit('addToStore', this.labels)
    },
    //点击添加属性里的属性值方框对其中的input进行聚焦
    attrValInputFocus(e) {
      //如果点到的不是输入框本身，再进行主动聚焦
      if (e.target.children.length !== 0) {
        e.target.children[e.target.children.length - 1].focus()
      }
    },
    //检查新建属性输入的信息是否完善，否则给出提示
    ifAttrReady() {
      let isReady = true
      if (this.newAttributeData.name === '') {
        console.log(this.$refs.attr_name_input);
        this.$refs.attr_name_input[0].style.border = "1px solid #F56C6C"
        isReady = false
      }
      if (this.newAttributeData.input_type === '') {
        console.log(this.$refs.attr_mod_select);
        this.$refs.attr_mod_select[0].style.border = "1px solid #F56C6C"
        isReady = false
      }
      if (this.newAttributeData.values.length === 0) {
        console.log(this.$refs.attr_value_input);
        this.$refs.attr_value_input[0].style.border = "1px solid #F56C6C"
        isReady = false
      }
      setTimeout(() => {
        this.$refs.attr_name_input[0].removeAttribute("style")
        this.$refs.attr_mod_select[0].removeAttribute("style")
        this.$refs.attr_value_input[0].removeAttribute("style")
      }, 1600)
      return isReady
    },
    //添加属性结束
    /** 提交创建项目后记得重置 attrIndex */
    handleAttrConfirm(tag) {
      if (this.ifAttrReady()) {
        //如果是在编辑标签，提交修改之前先把原属性删除
        if (this.isEditAttr) {
          tag.attributes.splice(this.beingEditAttrIndex, 1)
          this.beingEditAttrIndex = -1
          this.isEditAttr = false
        }
        this.newAttributeData.id = this.attrIndex
        this.labels[this.labels.indexOf(tag)].attributes.push(this.newAttributeData)
        this.attrIndex += 1
        this.labels[this.labels.indexOf(tag)].attrInputVisible = false
        this.newAttributeData = {
          "id": 0,
          "name": '',
          "input_type": '',
          "mutable": false,
          "values": [],
        }
        this.$store.commit('addToStore', this.labels)
      } else {
        this.$message({
          message: '请填写必要的参数',
          type: 'warning'
        })
      }
    },
    //终止添加属性值
    endAttrInput(tag) {
      this.labels[this.labels.indexOf(tag)].attrInputVisible = false
      this.newAttributeData = {
        "id": 0,
        "name": '',
        "input_type": '',
        "mutable": false,
        "values": [],
      }
    },
    //添加属性值结束
    /** 属性值过长的时候会跑到框外面*/
    handleAttrValInput(e) {
      if (e.target.innerText !== '') {
        this.newAttributeData.values.push(e.target.innerText)
        e.target.innerText = ''
        e.target.focus()
      }
    },
    //修改属性
    editAttrInfo(tag, attr) {
      this.isEditAttr = true
      this.beingEditAttrIndex = tag.attributes.indexOf(attr)
      this.newAttributeData = attr
      tag.attrInputVisible = true
    },
    //从仓库加载数据
    /** 加载人员数据可能不会再用到了，记得删掉*/
    loadData() {
      let labData = this.$store.state.projectInfo.labels
      console.log('开始从仓库加载数据', labData);
      for (let i = 0; i < labData.length; i++) {
        let item = {}
        item.name = labData[i].name
        item.id = labData[i].id
        item.attributes = labData[i].attributes
        item.attrInputVisible = false
        this.labels.push(item)

        // labData[i].attrInputVisible = false
        // this.labels.push(labData[i])
      }
      // this.labels = this.$store.state.projectInfo.labels
      console.log("从仓库重新加载数据完成", this.labels);


      this.image_quality = this.$store.state.image_quality
      this.userValue = this.$store.state.allUsers

      //加载人员的同时重新求job数量，保证segment_size至少为1
      if (this.userValue.length === 0) {
        this.segment_size = 1
      } else {
        this.segment_size = this.userValue.length
      }
    },
    //提交imageQuality
    pushImageQuality() {
      this.$store.commit('addImageQuality', this.image_quality)
    },
    //获取人员信息
    getAllUsersInfo(event) {
      if (event.label === "任务分配") {
        //清除原有数据
        this.userData = []
        //获取加载数据
        this.$http.get('v1/users?page_size=all').then((e) => {
          e.data.results.forEach((user, index) => {
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
    saveUserInfo() {
      let allUsers = []
      //根据成员数改变job数
      this.changeSeg('users')

      for (let i = 0; i < this.userValue.length; i++) {
        allUsers.push(this.userData[this.userValue[i]].key)
      }
      this.$store.commit('saveAllUsers', allUsers)
    },
    //修改segment
    //mod: 1.plus 点击+1 2.minus 点击-1 3.modify直接修改 4. 穿梭框变化时的修改
    changeSeg(mod) {

      /**如果没有传图片先点这个会有undefined报错*/
        // console.log(this.$store.state.allFileList.length);
        // console.log(this.$store.state.allFileList[0].type.indexOf("zip"))
        //如果传图片最大值是图片个数,如果是压缩包，最大值是999(因为无法判断压缩包内的图片数量)
      let MAX = 999
      if (this.$store.state.allFileList.length === 0) {
        this.$message({
          message: "请先添加图片数据",
          type: "error"
        })
        return //跳出函数不再继续执行
      } else if (this.$store.state.allFileList[0].type.indexOf("zip") === -1) {
        MAX = this.$store.state.allFileList.length
      }

      if (mod === 'plus') {
        if (this.segment_size < MAX) {
          this.segment_size = parseInt(this.segment_size) + 1
        } else {
          this.$message({
            message: '不能超过图片数量',
            type: "warning"
          })
        }
      } else if (mod === 'minus') {
        if (this.segment_size > 1) {
          this.segment_size = parseInt(this.segment_size) - 1
        }
      } else if (mod === 'modify') {
        if (this.segment_size < 1 || this.segment_size > MAX) {
          this.$message({
            message: '非法数值，请重新输入',
            type: "warning"
          })
          //警告结束后改为默认值
          if (this.userValue.length === 0) {
            this.segment_size = 1
          } else {
            this.segment_size = this.userValue.length
          }
        }
      } else if (mod === 'users') {
        if (this.userValue.length === 0) {//如果没有指定人员
          this.segment_size = 1
        } else if (this.userValue.length > MAX) {
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
.module-box {
  width: 100%;

  .el-tabs--border-card {
    border: 1px solid #6fcdb2;
    border-radius: 10px;
    box-shadow: none !important;
    overflow: hidden;
  }

  .label-box {
    box-sizing: border-box;
    border: 1px solid #318B71;
    border-radius: 8px;
    margin: 10px 0;
    display: inline-block;
    width: 868px;
    overflow: hidden;

    .tab-box {
      width: 200px;

      .tag {
        display: block !important;
        border-radius: 0;
        border: 0;
        border-bottom: 1px solid #6fcdb2;
        background-color: transparent;
        color: #318B71;
        font-size: 16px;
      }
    }

    .attribute-box {
      width: 100%;
      box-sizing: border-box;

      .attribute-item {
        min-height: 46px;
        padding-top: 3px;
        box-sizing: border-box;
        display: flex;
        border-bottom: 1px solid #f7fff9;

        .attr-name {
          flex: 3;
          text-align: center;
        }

        .attr-mod {
          flex: 3;
          text-align: center;
        }

        .attr-value {
          flex: 5;
        }

        .attr-name, .attr-mod, .attr-value {
          padding-left: 10px;
          line-height: 40px;
          overflow: hidden;
        }

        .attr-edit-box {
          flex: 1;
          display: flex;

          .attr-edit {
            flex: 1;
            text-align: center;
            line-height: 40px;

            i {
              display: block;
              padding: 10px;
              cursor: pointer;
              border-radius: 3px;
              margin: 2px;
            }

            i:hover {
              background-color: #c9e3d6;
            }
          }

          .attr-delete {
            text-align: center;
            line-height: 40px;
            flex: 1;

            i {
              display: block;
              padding: 10px;
              cursor: pointer;
              border-radius: 3px;
              margin: 2px;
            }

            i:hover {
              background-color: #c9e3d6;
            }
          }
        }
      }

      .attribute-item:hover {
        background-color: #f7fff9;
      }

      .attr-input-box {
        min-height: 46px;
        border-radius: 3px;
        box-sizing: border-box;
        background-color: #edf8f3;

        .input-box-tip {
          width: 100%;
          height: 24px;
          padding: 8px 0 0 10px;
          box-sizing: border-box;
          line-height: 14px;
          display: flex;
          justify-content: space-between;
          color: #999;

          span {
            font-size: 14px;
          }

          i {
            margin-right: 6px;
            cursor: pointer;
          }

          i:hover {
            background-color: #ccc;
          }
        }

        .input-box-content {
          display: flex;

          .attr-name-input-box {
            flex: 3;

            .attr-name-input {
              margin: 8px;
              height: 40px;
              overflow: hidden;
              box-sizing: border-box;
              transition: border .2s ease;
            }
          }

          .attr-mod-select-box {
            flex: 3;

            .attr-mod-select {
              margin: 8px;
              height: 40px;
              overflow: hidden;
              box-sizing: border-box;
              transition: border .2s ease;
            }
          }

          .attr-value-input-box {
            flex: 5;
            padding: 8px;
            max-width: 40%;
            cursor: text;

            .attr-value-input {
              min-height: 38px;
              background-color: #fff;
              box-sizing: border-box;
              border: 1px solid #dcdfe6;
              display: flex;
              flex-wrap: wrap;
              transition: border .2s ease;

              .attr-val-item {
                margin: 3px 0 0 3px;
              }

              .val-input {
                display: inline-block;
                outline: none;
                margin: 3px;
                height: 32px;
                padding: 0;
                line-height: 32px;
                min-width: 1em;
                max-width: 100%;
                overflow: hidden;
                white-space: nowrap;
              }
            }

            .attr-value-input:hover {
              border: 1px solid #c2c3c6;
            }
          }

          .attr-input-confirm-box {
            flex: 1;

            .attr-input-confirm {
              margin: 12px;
              height: 40px;
            }
          }
        }
      }
    }
  }

  .raw-label-box {
    width: 100%;

    .raw-label {
      width: 100%;
      resize: vertical;
      outline: none;
      overflow: auto;
      border-radius: 5px;
      border: 1px solid #318B71;
      box-sizing: border-box;
    }
  }

  .slide-bar {
    width: 600px;
  }

  .image-quality-text {
    font-size: 16px;
    color: #55664e;
  }

  .button-new-tag {
    margin: 10px;
  }

  .input-new-tag {
    width: 90%;
    margin: 10px 0;
  }

  .segment-size-box {
    margin-top: 20px;
    height: 100px;
    width: 100%;

    .segment-size {
      height: 40px;
      width: 160px;
      margin: auto;
      border: 1px solid #c2e8cc;
      border-radius: 3px;
      line-height: 40px;
      text-align: center;
      display: flex;

      .minus-one {
        height: 100%;
        width: 40px;
      }

      .segment-size-number {
        height: 100%;
        width: 80px;
        background-color: lightblue;

        input {
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

      .plus-one {
        height: 100%;
        width: 40px;
      }
    }

    .segment-tip {
      height: 60px;
      width: 600px;
      margin: 10px auto 0 auto;
      overflow: hidden;
      text-align: center;

      .tips {
        color: #666666;
        font-size: 14px;
      }

      span {
        font-size: 6px;
        color: #999999;
      }
    }
  }
}

/deep/ .el-transfer-panel__filter {
  margin: 0;
}

/deep/ .el-input__inner {
  border-radius: 0;
}

/deep/ .el-transfer {
  width: 590px;
  margin: auto;
}
</style>
