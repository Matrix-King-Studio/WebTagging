<template>
  <div class="main-box">
    <div class="sidebar">
      <el-tooltip
        :class="['item','tools',{'tool-active':flag === 'cursor'}]"
        effect="dark"
        content="鼠标"
        placement="right"
      >
        <el-button @click="initDrawTools('cursor')">
          <span class="iconfont">&#xe6c7;</span>
        </el-button>
      </el-tooltip>
      <span class="line" />
      <el-tooltip
        :class="['item','tools',{'tool-active':flag === 'rectangle'}]"
        effect="dark"
        content="矩形标记"
        placement="right"
      >
        <el-button @click="initDrawTools('rectangle')">
          <span class="iconfont">&#xe88e;</span>
        </el-button>
      </el-tooltip>
    </div>
    <div ref="objBar" class="object-bar">
      <div
        ref="drawer"
        class="drawer"
        @click="showBar()"
      >
        <i :class="[{'el-icon-right':flag2},{'el-icon-back':!flag2}]" />
      </div>

      <!--右边的用来选择标签的框的box-->
      <div class="label-obj-box" >
        <!--右边的用来选择标签的框，每一项-->
        <div
          v-for="item in shapes.rectangles"
          :key="item.index"
          :id="'style_'+(item.index)"
          class="label-obj"
          @mouseenter="showRecObj(item.index),showLabObj(item.index)"
          @mouseleave="hideRecObj(item.index),hideLabObj(item.index)"
        >
          <!--右边的用来选择标签的框，上半部分，显示序号和标签下拉选择-->
          <div class="label-info">
            <span>{{ item.index }}</span>
            <div class="change-label">
              <el-select
                v-model="shapes.rectangles[item.index-1].label_id"
                placeholder="请选择"
                size="mini"
              >
                <el-option
                  v-for="i in options"
                  :key="i.value"
                  :label="i.label"
                  :value="i.value"
                />
              </el-select>
            </div>
          </div>
          <!--右边的用来选择标签的框，下半部分，显示一些按钮-->
          <div class="label-func">
            <div
              class="func lock"
              @click="lockRecObj(item.index)"
            >
              <i :class="[{'el-icon-lock':shapes.rectangles[item.index-1].isLock},{'el-icon-unlock':!shapes.rectangles[item.index-1].isLock}]" />
            </div>
            <div
              class="func visible"
              @click="invisibleRecObj(item.index)"
            >
              <span
                v-show="!shapes.rectangles[item.index-1].isInvisible"
                class="iconfont"
              >&#xe9c1;</span>
              <span
                v-show="shapes.rectangles[item.index-1].isInvisible"
                class="iconfont"
              >&#xe6fe;</span>
            </div>
            <div
              class="func delete"
              @click="deleteRecObj(item.index)"
            >
              <i class="el-icon-delete" />
            </div>
          </div>
        </div>
      </div>
      <div class="main-btn-box">
        <div class="images">
          <div
            class="img-btn to-start"
            @click="changeImg('start')"
          >
            <i class="el-icon-d-arrow-left" />
          </div>
          <div
            class="img-btn back"
            @click="changeImg('back')"
          >
            <i class="el-icon-arrow-left" />
          </div>
          <div class="img-btn this">
            <span>{{ imageIndex + 1 }}</span>
          </div>
          <div
            class="img-btn next"
            @click="changeImg('next')"
          >
            <i class="el-icon-arrow-right" />
          </div>
          <div
            class="img-btn to-end"
            @click="changeImg('end')"
          >
            <i class="el-icon-d-arrow-right" />
          </div>
        </div>
        <div class="main-func">
          <div
            class="main-btn submit"
            @click="isPrepare"
          >
            <i class="el-icon-upload" />
            <span>提交所有</span>
          </div>
          <div class="main-btn abandon">
            <span>废弃</span>
          </div>
        </div>
      </div>
    </div>
    <div ref="paintBox" class="paint-box">
      <canvas
        id="myCanvas"
        ref="myCanvas"
        width="500px"
        height="400px"
      />
      <div
        v-if="flag==='rectangle'"
        ref="vl"
        class="vertical-line"
      />
      <div
        v-if="flag==='rectangle'"
        ref="ll"
        class="level-line"
      ></div>
      <!--用来放标记的矩形框-->
      <div class="rec-box" ref="recBox"></div>
      <div class="tips-box" ref="tipsBox">
        <span>正在加载</span>
      </div>
    </div>
  </div>
</template>

<script>
import JSZip from '@/assets/js/jszip'

export default {
  data() {
    return {
      //哪一个工具
      flag: 'cursor',
      //项目栏是否展开
      flag2: true,
      //是否是第一次打开
      isFirst: true,

      //保存所有Tag选项
      options: [],
      // value: '',

      //画布对象
      myCanvas: {},
      //画笔对象
      ctx: {},
      isDrawing: false,

      //图片相关
      isGotImg: false,
      imagesData: [],
      imagesSize: 0,
      imageIndex: 0,
      imageInfo: {},
      imageScale: 1,//图片缩放比例 ：缩放后/缩放前

      //矩形对象
      shapes: {
        rectangles: [],
      },
      rectangleIndex: 1,
      recTop: 0,
      recLeft: 0,

      //job信息
      jobId: 0,

      //控制页面改变大小时刷新的变量
      isResizing: '',

      // 设置 job 的起始 frame 和终止 frame
      start_frame: 0,
      stop_frame: 0,
    }
  },
  created() {
    //获取图片信息
    this.getImagesInfo()
    //获取job信息
    this.getJobInfo()
  },
  mounted() {
    this.getImages()
    //停止改变窗口大小后0.3秒重新绘制图片
    window.onresize = () => {
      if (this.isResizing) {
        clearTimeout(this.isResizing)
      }
      this.isResizing = setTimeout(() => {
        this.resizeCanvas()
      }, 300)
    }
  },
  destroyed() {
    //页面切换清除改变大小监听器
    window.onresize = () => {
    }
  },
  methods: {
    //右侧信息栏
    showBar() {
      if (this.flag2) {
        this.$refs.objBar.style.right = '-300px'
        this.$refs.drawer.style.left = '-35px'
        this.flag2 = false
      } else {
        this.$refs.objBar.style.right = '0px'
        this.$refs.drawer.style.left = '0px'
        this.flag2 = true
      }
    },
    //获取images信息列表
    getImagesInfo() {
      this.$http.get('v1/tasks/' + this.$route.params.index + '/data/meta').then(e => {
        console.log(e.data);
        this.imagesSize = e.data.size
        this.start_frame = e.data.start_frame
        this.stop_frame = e.data.stop_frame
      })
    },
    //获取图片压缩包并解压，将 base64 代码保存到 imagesData 里
    /** 不能直接用 url 中的 id 去拿图片，如果暴力改变 url 需要回到 home 要用路由守卫*/
    getImages() {
      //请求图片数据
      console.log("0.开始请求数据");
      this.$http.get('v1/tasks/' + this.$route.params.index + '/data', {
        params: {
          type: 'chunk',
          //数字0是加载图片，2是禁止加载
          number: 0,
          quality: 'compressed'
        },
        // 请求数据的格式
        responseType: 'arraybuffer',
      }).then(e => {
        console.log("1.图片获取完成")
        // 使用JSZip解压数据
        const zip = new JSZip()
        if (e.data) {
          zip.loadAsync(e.data).then((imgData) => {
            // 获取图片base64格式信息
            for (let key in imgData.files) {
              let base = imgData.file(zip.files[key].name).async('base64')
              base.then(res => {
                this.imagesData.push(res)
              })
            }
            console.log("2.图片解压完成")
            this.isGotImg = true
          })
        }
      }).then(() => {
            this.initCanvas()
          }
      ).catch(err => {
        console.log(err);
      })
    },
    //初始化画布
    initCanvas() {
      //获取元素
      this.myCanvas = this.$refs.myCanvas
      //加载画笔工具
      this.ctx = this.myCanvas.getContext('2d')
      //根据屏幕设置canvas大小
      this.myCanvas.width = document.body.clientWidth - 46
      this.myCanvas.height = document.body.clientHeight - 35

      console.log("3.画布初始化完成")
      //绘制图片
      this.drawImages()
      //设置鼠标样式
      document.getElementById('myCanvas').style.cursor = 'default'
    },
    //改变画布大小
    resizeCanvas() {
      this.myCanvas.width = document.body.clientWidth - 46
      this.myCanvas.height = document.body.clientHeight - 35
      console.log('3.1重置画布大小完成')
      this.drawImages()
      this.reDrawTags(2, this.imageIndex)
    },
    //绘制图片
    drawImages() {
      //将解压出的文件以base64格式放到图片对象中
      let img = new Image()

      console.log("4.图片对象初始化完成");
      //清除画布
      this.ctx.clearRect(0, 0, this.myCanvas.width, this.myCanvas.height)
      setTimeout(() => {
        img.src = "data:image/png;base64," + this.imagesData[this.imageIndex]
        console.log("5.base64数据嵌入完成");
      }, 100)

      setTimeout(() => {
        // console.log('图片原始尺寸' + img.width, img.height);
        //图片比窗口长，则上下填充满
        if (img.width / img.height < (this.myCanvas.width - 300) / this.myCanvas.height) {
          this.imageInfo = {
            left: (this.myCanvas.width - 300 - this.myCanvas.height * img.width / img.height) / 2 + 5,
            top: 5,
            width: this.myCanvas.height * img.width / img.height - 10,
            height: this.myCanvas.height - 10
          }
        } else {//窗口比图片长，左右填满
          this.imageInfo = {
            left: 5,
            top: (this.myCanvas.height - (this.myCanvas.width - 300) * img.height / img.width) / 2 + 5,
            width: this.myCanvas.width - 310,
            height: (this.myCanvas.width - 300) * img.height / img.width - 10
          }
        }

        // console.log('图片缩放后的尺寸' + this.imageInfo.width, this.imageInfo.height);
        this.imageScale = img.width / this.imageInfo.width
        console.log("6.图片尺寸数据处理完成，图片缩放比例：" + this.imageScale);
        //将图片绘制到canvas上
        this.ctx.drawImage(img, this.imageInfo.left, this.imageInfo.top, this.imageInfo.width, this.imageInfo.height)
        console.log("7.图片绘制完成");

        //加载完成后删除
        if (this.isFirst) {
          this.$refs.tipsBox.parentNode.removeChild(this.$refs.tipsBox)
          this.isFirst = false
        }
      }, 200)
    },

    //切换图片
    changeImg(mod) {
      if (mod === 'start') {
        if (this.imageIndex !== 0) {
          this.imageIndex = 0
          this.drawImages()
          this.removeRec('all')
          this.reDrawTags(1, this.imageIndex)
        }
      } else if (mod === 'back') {
        if (this.imageIndex !== 0) {
          this.imageIndex -= 1
          this.drawImages()
          this.removeRec('all')
          this.reDrawTags(1, this.imageIndex)
        }
      } else if (mod === 'next') {
        if (this.imageIndex !== (this.imagesSize - 1)) {
          this.imageIndex += 1
          this.drawImages()
          this.removeRec('all')
          this.reDrawTags(1, this.imageIndex)
        }
        /* Alex Start */
        this.$http.get('v1/tasks/' + this.$route.params.index + '/data', {
          params: {
            type: 'chunk',
            //数字0是加载图片，2是禁止加载
            number: this.imageIndex,
            quality: 'compressed'
          },
          // 请求数据的格式
          responseType: 'arraybuffer',
        }).then(e => {
          console.log("1.图片获取完成")
          // 使用 JSZip 解压数据
          const zip = new JSZip()
          if (e.data) {
            zip.loadAsync(e.data).then((imgData) => {
              // 获取图片base64格式信息
              for (let key in imgData.files) {
                let base = imgData.file(zip.files[key].name).async('base64')
                base.then(res => {
                  this.imagesData.push(res)
                })
              }
              console.log("2.图片解压完成")
              this.isGotImg = true
            })
          }
        })
        /* Alex End */
      } else if (mod === 'end') {
        if (this.imageIndex !== (this.imagesSize - 1)) {
          this.imageIndex = this.imagesSize - 1
          this.drawImages()
          this.removeRec('all')
          this.reDrawTags(1, this.imageIndex)
        }
      }

    },
    //切换工具
    initDrawTools(attr) {
      //处于相应的工具状态
      this.flag = attr
      //跟手基准线
      //选择画笔
      if (attr === 'rectangle') {
        this.setToLine()
        this.createRec()
      } else if (attr === 'cursor') {
        this.setToCursor()
      }
    },
    //切换成鼠标的样式
    setToCursor() {
      //恢复鼠标样式
      this.$refs.myCanvas.style.cursor = 'default'
      document.getElementsByClassName('rec-obj').forEach((item) => {
        item.style.cursor = 'default'
      })
      //移除跟随鼠标
      document.body.removeEventListener('mousemove', this.followMouse, false)
      //如果没有完成矩形的绘制
      if (this.isDrawing) {
        document.body.removeEventListener('mousemove', this.resizeRec, false)
        this.isDrawing = !this.isDrawing
      }
      //移除click创建元素
      document.body.removeEventListener('mousedown', this.createRec, true)
    },
    //切换成矩形标记的样式
    setToLine() {
      //隐藏鼠标
      this.$refs.myCanvas.style.cursor = 'none'
      document.getElementsByClassName('rec-obj').forEach((item) => {
        item.style.cursor = 'none'
      })
      //跟随鼠标
      document.body.addEventListener('mousemove', this.followMouse, false)
      //创建矩形框
      document.body.addEventListener('mousedown', this.createRec, true)
    },
    //跟随鼠标的基准线
    followMouse(e) {
      let mPos = this.getMousePos(e)
      this.$refs.vl.style.left = mPos.left + 'px'
      this.$refs.ll.style.top = mPos.top + 'px'
    },
    //获取鼠标位置
    getMousePos(event) {
      return {
        top: event.clientY,
        left: event.clientX
      }
    },
    //画矩形
    createRec(e) {
      if (e) {
        //获取点击的坐标
        let mPos = this.getMousePos(e)
        //获取图片相对页面的位置
        let leftBorder = parseInt(this.imageInfo.left) + 46//加上了左侧工具栏的宽度 46px
        let topBorder = parseInt(this.imageInfo.top) + 35//加上了顶部头的高度 35px
        let rightBorder = leftBorder + parseInt(this.imageInfo.width)
        let bottomBorder = topBorder + parseInt(this.imageInfo.height)
        //如果在图片上点击
        if (mPos.top >= topBorder && mPos.top <= bottomBorder && mPos.left >= leftBorder && mPos.left <= rightBorder) {
          if (!this.isDrawing) {
            //转换绘制状态
            this.isDrawing = !this.isDrawing
            //创建元素并设置元素的左上角位置
            let rec = document.createElement('div')
            rec.className += 'rec-obj'
            //id用来标记是第几个div
            rec.id = this.rectangleIndex
            rec.style.top = mPos.top + 'px'
            rec.style.left = mPos.left + 'px'
            //添加鼠标移入，右侧对应标签栏高亮事件
            rec.onmouseenter = (e) => {
              this.showLabObj(e.target.id)
            }
            //添加鼠标移出，右侧对应标签栏高亮事件
            rec.onmouseleave = (e) => {
              this.hideLabObj(e.target.id)
            }
            this.recTop = mPos.top
            this.recLeft = mPos.left
            //向矩形框数组添加对象
            let r = {
              type: "rectangle",
              occluded: false,
              z_order: 0,
              index: this.rectangleIndex,//矩形框序号
              el: rec,//矩形框DOM元素
              // id:5,
              frame: this.imageIndex + 1,//第几张图片，从1开始
              label_id: this.options[0].value,//一级标签默认选择第一个
              group: 0,
              isLock: false,
              isInvisible: false,
              attributes: [],
              points: [],//记录矩形框位置
            }
            this.rectangleIndex++
            this.shapes.rectangles.push(r)
            //渲染到页面上
            this.$refs.recBox.appendChild(rec)
            //根据鼠标位置调整矩形框的大小
            document.body.addEventListener('mousemove', this.resizeRec, false)
          } else {
            this.isDrawing = !this.isDrawing
            document.body.removeEventListener('mousemove', this.resizeRec, false)
            //记录矩形框左上，右下两个点的x1,y1,x2,y2坐标在 !原图! 上的坐标
            this.shapes.rectangles[this.shapes.rectangles.length - 1].points = [
              (parseInt(this.shapes.rectangles[this.shapes.rectangles.length - 1].el.style.left.replace('px', '')) - (parseInt(this.imageInfo.left) + 46)) * this.imageScale,
              (parseInt(this.shapes.rectangles[this.shapes.rectangles.length - 1].el.style.top.replace('px', '')) - (parseInt(this.imageInfo.top) + 35)) * this.imageScale,
              (parseInt(this.shapes.rectangles[this.shapes.rectangles.length - 1].el.style.width.replace('px', '')) + parseInt(this.shapes.rectangles[this.shapes.rectangles.length - 1].el.style.left.replace('px', '')) - (parseInt(this.imageInfo.left) + 46)) * this.imageScale,
              (parseInt(this.shapes.rectangles[this.shapes.rectangles.length - 1].el.style.height.replace('px', '')) + parseInt(this.shapes.rectangles[this.shapes.rectangles.length - 1].el.style.top.replace('px', '')) - (parseInt(this.imageInfo.top) + 35)) * this.imageScale,
            ]
            console.log('矩形框两点数据', this.shapes.rectangles[this.shapes.rectangles.length - 1].points);
            //画完自动保存
            this.saveTagsToStore()
            //完成一个标记,切换回鼠标模式
            // this.initDrawTools('cursor')
          }
        }
      }
    },
    //鼠标移动控制矩形框大小
    resizeRec(e) {
      let mPos = this.getMousePos(e)
      if (mPos.left >= this.recLeft && mPos.top >= this.recTop) {
        //鼠标在右下
        this.drawRec(this.recTop, mPos.left + 1, mPos.top + 1, this.recLeft)
      } else if (mPos.left >= this.recLeft && mPos.top <= this.recTop) {
        //右上
        this.drawRec(mPos.top, mPos.left + 1, this.recTop, this.recLeft)
      } else if (mPos.left <= this.recLeft && mPos.top <= this.recTop) {
        //左上
        this.drawRec(mPos.top, this.recLeft, this.recTop, mPos.left)
      } else if (mPos.left <= this.recLeft && mPos.top >= this.recTop) {
        //左下
        this.drawRec(this.recTop, this.recLeft, mPos.top + 1, mPos.left)
      }
    },
    //绘制矩形框
    drawRec(top, right, bottom, left) {
      this.shapes.rectangles[this.shapes.rectangles.length - 1].el.style.left = left + 'px'
      this.shapes.rectangles[this.shapes.rectangles.length - 1].el.style.top = top + 'px'
      this.shapes.rectangles[this.shapes.rectangles.length - 1].el.style.width = right - left + 'px'
      this.shapes.rectangles[this.shapes.rectangles.length - 1].el.style.height = bottom - top + 'px'
    },
    //删除元素
    removeRec(mod) {
      if (mod === 'all') {
        this.$refs.recBox.innerHTML = ''
        this.shapes.rectangles = []
        this.rectangleIndex = 1
      }
    },
    //获取job信息
    getJobInfo() {
      this.$http.get('v1/tasks?', {
        params: {
          id: this.$route.params.index,
          page: 1,
          page_size: 10
        }
      }).then((e) => {
        this.jobId = e.data.results[0].segments[0].jobs[0].id
        // console.log(e)
        for (let item in e.data.results[0].labels) {
          let label = {
            value: e.data.results[0].labels[item].id,
            label: e.data.results[0].labels[item].name
          }
          this.options.push(label)
        }
        console.log('标签列表', this.options);
      })
    },
    //将标注信息存储到store中
    saveTagsToStore() {
      this.$store.commit('cleanTagsInfo', this.imageIndex)
      this.$store.commit('saveTagsInfo', this.shapes)
      this.$message({
        message: '自动保存成功',
        type: "success"
      })
    },
    //提交前询问
    isPrepare() {
      this.$confirm('提交后无法修改, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.submitTags()
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消提交'
        });
      });
    },
    //提交标注信息
    /** 提交成功后的逻辑还需进一步改进 暂时改成不能再次进入*/
    submitTags() {
      let TagsInfo = this.$store.state.imageTags
      console.log(TagsInfo)
      this.$http.patch('v1/jobs/' + this.jobId + '/annotations?action=create', TagsInfo).then((e) => {
        console.log(e)
        this.$message({
          message: "提交成功",
          type: "success"
        })
        this.$router.push('/home')
      }).catch((err) => {
        console.log(err);
      })
    },
    //切换图片接收信息重新绘制Tag
    //或者窗口大小改变时重新绘制Tag
    //mod:  1：切换图片  2：改变窗口大小
    /**   切换图片后矩形框内的鼠标样式有问题
     * 是否锁定的参数没有保存回传*/
    reDrawTags(mod, index) {
      //切换到了第几张图片
      let imgIndex = index + 1
      let TagsInfo = {}
      let that = this
      if (mod === 1) {
        //从store获取所有的标注信息
        TagsInfo = that.$store.state.imageTags.shapes
      } else if (mod === 2) {
        TagsInfo = that.shapes.rectangles
        this.removeRec('all')
      }
      //清洗出这张图片的标注信息
      console.log(TagsInfo);
      for (let item in TagsInfo) {
        if (TagsInfo[item].frame === imgIndex) {

          console.log('矩形框在页面上的位置', TagsInfo[item].points);

          //创建矩形框
          let rec = document.createElement('div')
          rec.className += 'rec-obj'
          //id用来标记是第几个div
          rec.id = this.rectangleIndex
          //添加鼠标移入，右侧对应标签栏高亮事件
          rec.onmouseenter = (e) => {
              this.showLabObj(e.target.id)
          }
          //添加鼠标移出，右侧对应标签栏高亮事件
          rec.onmouseleave = (e) => {
              this.hideLabObj(e.target.id)
          }

          setTimeout(() => {
            // console.log(parseInt(TagsInfo[item].points[0]) / this.imageScale);
            // console.log(parseInt(this.imageInfo.left));
            // console.log(parseInt(TagsInfo[item].points[1]) / this.imageScale);
            // console.log(parseInt(this.imageInfo.top));
            rec.style.left = parseInt(TagsInfo[item].points[0]) / this.imageScale + parseInt(this.imageInfo.left) + 46 + 'px'
            rec.style.top = parseInt(TagsInfo[item].points[1]) / this.imageScale + parseInt(this.imageInfo.top) + 35 + 'px'
            rec.style.width = (parseInt(TagsInfo[item].points[2]) - parseInt(TagsInfo[item].points[0])) / this.imageScale + 'px'
            rec.style.height = (parseInt(TagsInfo[item].points[3]) - parseInt(TagsInfo[item].points[1])) / this.imageScale + 'px'
            rec.style.cursor = 'default'
            this.$refs.recBox.appendChild(rec)
          }, 300)

          // console.log('标记的真实数据', TagsInfo[item])

          //添加数据
          this.shapes.rectangles.push({
            type: TagsInfo[item].type,
            occluded: TagsInfo[item].occluded,
            z_order: TagsInfo[item].z_order,
            index: this.rectangleIndex,
            el: rec,
            // id:5,
            frame: TagsInfo[item].frame,
            label_id: TagsInfo[item].label_id,
            group: TagsInfo[item].group,
            isLock: false,
            isInvisible: false,
            attributes: TagsInfo[item].attributes,
            points: TagsInfo[item].points,
          })
          this.rectangleIndex++
        }
      }
      //恢复鼠标样式
      this.initDrawTools('cursor')
      /** 鼠标样式无法更改*/
      document.getElementsByClassName('rec-obj').forEach((item) => {
        item.style.cursor = 'default'
      })
    },
    //鼠标放到右侧信息栏高亮对应矩形框
    showRecObj(index) {
      this.shapes.rectangles[index - 1].el.style.backgroundColor = 'rgba(255,255,255,0.4)'
    },
    //鼠标放到矩形框高亮右侧信息栏
    showLabObj(index){
      console.log("鼠标移入第" + index + "个标记框");
      let styleid = "style_"+index;
      let object = document.getElementById(styleid);
      object.style.background = 'rgb(255,241,142)'
    },
    hideRecObj(index){
      this.shapes.rectangles[index-1].el.style.backgroundColor = 'transparent'
    },
    //鼠标移出颜色消失
    hideLabObj(index){
      console.log("鼠标移出第" + index + "个标记框");
      let styleid = "style_"+index;
      let object = document.getElementById(styleid);
      object.style.background = 'rgb(255,255,255)'
    },
    //信息栏中的功能
    //锁定
    lockRecObj(index) {
      this.shapes.rectangles[index - 1].isLock = !this.shapes.rectangles[index - 1].isLock
      if (this.shapes.rectangles[index - 1].isLock) {
        this.shapes.rectangles[index - 1].el.classList.add('rec-obj-lock')
      } else {
        this.shapes.rectangles[index - 1].el.classList.remove('rec-obj-lock')
      }
    },
    //不可见
    invisibleRecObj(index) {
      if (this.shapes.rectangles[index - 1].isInvisible) {
        this.shapes.rectangles[index - 1].el.style.display = 'block'
      } else {
        this.shapes.rectangles[index - 1].el.style.display = 'none'
      }
      this.shapes.rectangles[index - 1].isInvisible = !this.shapes.rectangles[index - 1].isInvisible
    },
    //删除
    deleteRecObj(index) {

      // console.log(this.shapes.rectangles[index-1].el);
      //删除元素
      this.shapes.rectangles[index - 1].el.parentNode.removeChild(this.shapes.rectangles[index - 1].el)
      //
      for (let i = index; i < this.shapes.rectangles.length; i++) {
        // console.log(this.shapes.rectangles[i]);
        this.shapes.rectangles[i].index -= 1
      }
      //删除数据
      this.shapes.rectangles.splice(index - 1, 1)

      // console.log(this.shapes.rectangles);

      this.rectangleIndex--

      this.$store.commit('cleanTagsInfo', this.imageIndex)
      this.$store.commit('saveTagsInfo', this.shapes)

      this.$message({
        message: "元素成功移除",
        type: "success"
      })
    }
  }
}
</script>

<style lang="less" scoped>
.main-box {
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  overflow: hidden;
}

.sidebar {
  position: absolute;
  z-index: 3;
  left: 0;
  top: 0;
  height: 100%;
  width: 46px;
  padding-top: 65px;
  box-sizing: border-box;
  background-color: #bbe6d6;

  .tools {
    height: 36px !important;
    width: 36px !important;
    padding: 0 !important;
    border: 0 !important;
    background-color: #bbe6d6;
    margin: 5px;
    line-height: 36px;
    border-radius: 5px;
    transition: background-color 0.2s;
    text-align: center;

    span {
      font-size: 24px;
      color: #222222 !important;
    }
  }

  .tools:hover {
    background-color: #99baae;
  }

  .tool-active {
    background-color: #a6c7bb;
  }

  .line {
    display: block;
    width: 100%;
    height: 1px;
    background-color: #b3d9cb;
  }
}

.object-bar {
  position: absolute;
  z-index: 3;
  top: 0;
  right: 0px;
  width: 300px;
  height: 100%;
  padding-top: 65px;
  box-sizing: border-box;
  background-color: #e4f5ef;
  box-shadow: -1px 0 6px 2px #c1d4cd;
  transition: all 0.4s ease;

  .drawer {
    position: absolute;
    top: 35px;
    left: 0px;
    width: 30px;
    height: 30px;
    background-color: rgba(0, 0, 0, 0);
    transition: background-color 0.3s, left 0.4s ease;

    i {
      font-size: 30px;
      line-height: 30px;
      text-align: center;
    }
  }

  .drawer:hover {
    background-color: rgba(0, 0, 0, 0.1);
  }

  .label-obj-box {
    width: 280px;
    height: 550px;
    margin: 20px auto;
    border: 2px solid #b3d9cb;
    border-radius: 12px;
    overflow: auto;
    background-color: #fafbfc;
    .label-obj{
      height: 80px;
      width: 100%;
      border-bottom: 1px solid #cae7dc;

      .label-info {
        width: 100%;
        height: 30px;

        span {
          display: block;
          float: left;
          padding-left: 20px;
          box-sizing: border-box;
          font-size: 14px;
          line-height: 30px;
          width: 30%;
          overflow: hidden;
        }

        .change-label {
          float: right;
          height: 100%;
          width: 60%;
          box-sizing: border-box;
          margin-right: 20px;
          padding: 2px;
        }
      }

      .label-func {
        width: 100%;
        height: 50px;

        .func {
          width: 30px;
          height: 30px;
          margin: 10px 20px;
          float: left;
          border-radius: 6px;
          transition: background-color 0.2s;
          text-align: center;
          line-height: 30px;
        }

        .func:hover {
          background-color: #b9d4ca;
        }
      }
    }
  }

  .images {
    width: 290px;
    height: 40px;
    margin: 5px;

    .img-btn {
      height: 30px;
      width: 36px;
      background-color: #def1ea;
      margin: 5px 11px;
      float: left;
      border-radius: 5px;
      text-align: center;
      line-height: 30px;
      transition: all 0.2s;
      font-size: 18px;
    }

    .img-btn:hover {
      background-color: #bbe6d6 !important;;
    }

    .this {
      font-size: 14px;
    }

    .this:hover {
      background-color: #def1ea;
    }
  }

  .main-func {
    position: absolute;
    bottom: 0;
    width: 290px;
    height: 80px;
    margin: 5px;
    padding: 0 15px;
    box-sizing: border-box;

    .main-btn {
      width: 90px;
      height: 36px;
      float: left;
      margin: 10px 2px;
      border-radius: 5px;
      background-color: #d6efe6;
      line-height: 36px;
      text-align: center;
      letter-spacing: 3px;
      font-size: 14px;
      transition: all 0.2s;

      i {
        font-size: 18px;
      }
    }

    .abandon {
      width: 46px;
      height: 26px;
      font-size: 10px;
      line-height: 26px;
      letter-spacing: 1px;
      margin-top: 20px;
      border-radius: 2px;
    }

    .submit {
      width: 200px;
      letter-spacing: 2px;
    }

    .main-btn:hover {
      background-color: #bbe6d6;
    }
  }
}

.paint-box {
  margin: 35px 0 0 46px;
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  background-color: #eeeeee;
  cursor: none;

  .vertical-line {
    position: absolute;
    z-index: 2;
    top: 0;
    left: 0;
    height: 100%;
    width: 1px;
    background-color: rgba(255, 0, 0, 0.4);
  }

  .level-line {
    position: absolute;
    z-index: 2;
    top: 0;
    left: 0;
    height: 1px;
    width: 100%;
    background-color: rgba(255, 0, 0, 0.4);
  }

  .tips-box {
    position: absolute;
    top: 0;
    height: 100%;
    width: 100%;
    text-align: left;
    padding: 400px 0 0 360px;
    font-size: 24px;
  }
}

/deep/ .rec-obj {
  position: absolute;
  width: 0;
  height: 0;
  background-color: transparent;
  cursor: none;
  box-sizing: border-box;
  border: 1px solid #333333;
  transition: background-color 0.1s;
}

/deep/ .rec-obj-lock {
  background-color: transparent !important;
}

/deep/ .rec-obj:hover {
  border: 2px solid #555555;
  background-color: rgba(228, 254, 239, 0.3) !important;
}
</style>
