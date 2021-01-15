<template>
  <div class="main-box">
    <!-- 左边的工具栏 -->
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
    <!-- 右边的工具栏 -->
    <div ref="objBar" class="object-bar">
      <!-- 展示/隐藏右边栏的按钮 -->
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
          v-for="item in shapes"
          :key="item.index"
          :id="'style_'+(item.index)"
          class="label-obj"
          @mouseenter="showRecObj(item.index), showLabObj(item.index)"
          @mouseleave="hideRecObj(item.index), hideLabObj(item.index)"
        >
          <!--右边的用来选择标签的框，上半部分，显示序号和标签下拉选择-->
          <div class="label-info">
            <span class="item-index">{{ item.index }}</span>
            <div class="change-label">
              <el-select
                v-model="item.label_id"
                placeholder="请选择"
                size="mini"
                @change="changeTagInfo(item)"
              >
                <el-option
                  v-for="i in options"
                  :key="i.value"
                  :label="i.label"
                  :value="i.value"
                />
              </el-select>
            </div>
            <div class="more-function">
              <el-dropdown>
                <span class="el-dropdown-link">
                  <i class="el-icon-more"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item icon="el-icon-plus">更多功能生在开发</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </div>
          </div>
          <!--右边的用来选择标签的框，下半部分，显示一些按钮-->
          <div class="label-func">
            <div
              class="func lock"
              @click="lockRecObj(item.index)"
            >
              <i :class="[{'el-icon-lock':item.isLock},{'el-icon-unlock':!item.isLock}]" />
            </div>
            <div
              class="func visible"
              @click="invisibleRecObj(item.index)"
            >
              <span
                v-show="!item.isInvisible"
                class="iconfont"
              >&#xe9c1;</span>
              <span
                v-show="item.isInvisible"
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
          <div class="label-add-attr">
            <i class="el-icon-caret-bottom"></i>

          </div>
        </div>
      </div>
      <!-- 所有的功能按钮 -->
      <div class="main-btn-box">
        <div class="switch-images">
          <div class="back">
            <span @click="changeImg(1)">-</span>
          </div>
          <div class="slider">
            <el-slider
              v-model="slideBarImageIndex"
              @change="changeImg(3)"
              :min="1"
              :max="imagesSize"
            >
            </el-slider>
          </div>
          <div class="next">
            <span @click="changeImg(2)">+</span>
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
          <div
            class="main-btn abandon"
            @click="getAllTags()"
          >
            <span>废弃</span>
          </div>
        </div>
      </div>
    </div>
    <!-- 进行标注的地方 -->
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
import {Tag} from "element-ui";

export default {
  data() {
    return {
      //哪一个工具
      flag: 'cursor',
      //项目栏是否展开
      flag2: true,
      //是否是第一次打开， 用于删除“正在加载字样”
      /** 后续会替代 */
      isFirst: true,
      //是否第一次加载矩形框
      /** 暂时用来解决刚进入job矩形框不加载的问题, 后续想更优雅的解决方法*/
      isFirstDrawRec: true,

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
      imagesData: '',
      //imagesSize原来为0，这里我改成了1，最小值应该为1吧
      imagesSize: 1,
      imageIndex: 1,
      slideBarImageIndex: 1,
      imageIndexFrom1: 1,
      imageInfo: {},
      imageScale: 1,//图片缩放比例 ：缩放后/缩放前

      //标注对象
      shapes: [

      ],
      rectangleIndex: 1,
      recTop: 0,
      recLeft: 0,

      //job信息
      jobId: [],
      //提交到服务器的版本号
      updateVersion: 0,

      //控制页面改变大小时刷新的变量
      isResizing: '',

      // 设置 job 的起始 frame 和终止 frame
      start_frame: 0,
      stop_frame: 0,

      //是否正在切换图片
      isChangingImage: false,

      //标注遮挡单选框
      // radio: 0,

      timeout: {},
    }
  },
  created() {
    //获取task信息
    this.getTaskInfo()
  },
  mounted() {
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
    //清除页面和仓库暂存的标注数据
    this.shapes = []
    this.$store.commit('cleanTagsInfo')
    //TODO: 在矩形框标注的状态下退出标注页面删除鼠标移动的监听器，就是控制横竖直线的监听器
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
    //获取task信息
    getTaskInfo() {
      /** job数量大于20时 这个pagesize会产生bug */
      this.$http.get('v1/tasks?', {
        params: {
          id: this.$route.params.index,
          page: 1,
          page_size: 20
        }
      }).then((e) => {
        //先获取task中的标签信息
        console.log('当前task信息', e.data)
        for (let item in e.data.results[0].labels) {
          let label = {
            value: e.data.results[0].labels[item].id,
            label: e.data.results[0].labels[item].name
          }
          this.options.push(label)
        }
        console.log('标签列表', this.options);

        //这个if是之后要添加的项目拥有者(创建者)浏览全部图片的接口
        //检查是否是管理员(要改) 并且 url中不带jobId
        if(this.$store.state.userInfo.ifAdmin && !this.$route.params.jobIndex){
          /** 这个条件暂时无法进入， 后期会添加管理员浏览整个Task情况时开放，所以先输出error*/
          console.log('error');
          //拿到对应task下所有的jobid 用于获取标注数据
          let jobsId = []
          for(let item of e.data.results[0].segments){
            jobsId.push(item.jobs[0].id)
          }
          this.jobId = jobsId

          //获取task所有图片列表
          this.$http.get('v1/tasks/' + this.$route.params.index + '/data/meta').then(e => {
            console.log('task' + this.$route.params.index + '所有image信息',e.data)
            console.log('图片范围', e.data.start_frame, e.data.stop_frame)
            this.start_frame = e.data.start_frame
            this.stop_frame = e.data.stop_frame
            this.imagesSize = e.data.size
          })
          //否则先将路径中的jobid与进入项目时获取的id比较，拦截非法跳转
        } else if (this.$route.params.jobIndex === this.$store.state.jobInfo.jobId+''){
          this.jobId = this.$route.params.jobIndex
          //再遍历task的job列表 寻找被分配的job 或者是否是创建者(Owner) 初始化开始结束图片和数量 如果没有找到拦截非法跳转
          if(e.data.results[0].segments.some((item)=>{
            //查看 jobId与仓库对应的job 的 标注员信息 是否与当前用户相同
            if(item.jobs[0].id === this.$store.state.jobInfo.jobId && ((item.jobs[0].assignee === this.$store.state.userInfo.id) || this.$store.state.userInfo.ifOwner)) {
              //相同就设置图片开始结束标记
              console.log('图片范围', item.start_frame, item.stop_frame)
              this.start_frame = item.start_frame
              this.stop_frame = item.stop_frame
              this.imagesSize = item.stop_frame - item.start_frame + 1
              return true
            }
          })){
            /** 我的代码结构有问题 if下面必须有句话 又没啥可以写的，就随便输出了个ok 之后再优化吧 */
            console.log('ok');
          } else {
            //没有找到当前用户对应的job信息
            alert('没有被分配的任务，请返回主页')
            this.$router.push('/home')
          }
        } else {
          alert('路径错误，请重新进入项目')
          this.$router.push('/home')
          /** 记得清除数据*/
        }
      }).then(()=>{
        this.initCanvas()
        this.getShapes()
      })
    },
    //获取标注数据
    getShapes(){
      this.$http.get('v1/jobs/'+ this.jobId +'/annotations').then((e)=>{
        console.log('从服务器获取标注数据', e.data);
        for(let item of e.data.shapes){
          this.$store.commit('saveTagsInfo', item)
        }
        console.log('将从服务器获取标注数据保存到仓库完成', this.$store.state.imageTags.shapes);
        this.updateVersion = e.data.version
        //加载后 用切换图片的模式 渲染第1张图片的标记信息
        this.reDrawTags(1, 1, e.data.shapes)
      }).catch((err)=>{
        console.log('获取标注数据失败', err);
      })
    },
    //获取图片压缩包并解压，将 base64 代码保存到 imagesData 里
    /** 不能直接用 url 中的 id 去拿图片，如果暴力改变 url 需要回到 home 要用路由守卫*/
    getImages() {
      //请求图片数据
      console.log("1.开始请求第" + (this.imageIndex) + "张图片的数据数据")
      this.$http.get('v1/tasks/' + this.$route.params.index + '/data', {
        params: {
          type: 'chunk',
          number: this.imageIndex - 1 + this.start_frame,
          quality: 'compressed'
        },
        // 请求数据的格式
        responseType: 'arraybuffer',
      }).then(e => {
        console.log("2.图片获取完成")
        // 使用JSZip解压数据
        const zip = new JSZip()
        if (e.data) {
          zip.loadAsync(e.data).then((imgData) => {
            // 获取图片base64格式信息
            for (let key in imgData.files) {
              let base = imgData.file(zip.files[key].name).async('base64')
              base.then(res => {
                this.imagesData = res
              })
            }
            console.log("3.图片解压完成")
            this.isGotImg = true
          }).then(()=>{
            this.drawImages()
          })
        }
      }).catch(err => {
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

      console.log("0.画布初始化完成")
      //获取图片
      this.getImages()
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
      //清除画布
      this.ctx.clearRect(0, 0, this.myCanvas.width, this.myCanvas.height)
      setTimeout(() => {
        img.src = "data:image/png;base64," + this.imagesData
        console.log("4.base64数据嵌入完成");
        img.onload = ()=>{
          // console.log('图片原始尺寸' + img.width, img.height);
          //图片比窗口高，则上下填充满
          if (img.width / img.height < (this.myCanvas.width - 300) / this.myCanvas.height) {
            this.imageInfo = {
              left: (this.myCanvas.width - 300 - this.myCanvas.height * img.width / img.height) / 2 + 5,
              top: 5,
              width: this.myCanvas.height * img.width / img.height - 10,
              height: this.myCanvas.height - 10
            }
          } else {//图片比窗口长，左右填满
            this.imageInfo = {
              left: 5,
              top: (this.myCanvas.height - (this.myCanvas.width - 300) * img.height / img.width) / 2 + 5,
              width: this.myCanvas.width - 310,
              height: (this.myCanvas.width - 300) * img.height / img.width - 10
            }
          }

          // console.log('图片缩放后的尺寸' + this.imageInfo.width, this.imageInfo.height);
          this.imageScale = img.width / this.imageInfo.width
          console.log("5.图片尺寸数据处理完成，图片缩放比例：" + this.imageScale);
          //将图片绘制到canvas上，这里的drawImage是canvas里的函数
          this.ctx.drawImage(img, this.imageInfo.left, this.imageInfo.top, this.imageInfo.width, this.imageInfo.height)
          console.log("6.图片绘制完成");

          //加载完成后删除正在加载
          if (this.isFirst) {
            this.$refs.tipsBox.parentNode.removeChild(this.$refs.tipsBox)
            this.isFirst = false
          }

          this.isChangingImage = false
        }
      }, 100)
    },
    //切换图片
    //mod: 1.上一张  2. 下一张  3. 根据滑块改变
    changeImg(mod) {
      clearTimeout(this.timeout)
      //如果图片加载完
      if(!this.isChangingImage){
        //这个变量在drawImages中变为false
        this.isChangingImage = true
        if(mod === 1){
          //如果在第一张禁止后退
          if(this.imageIndex === 1) {
            this.isChangingImage = false
            return
          }
          this.imageIndex -= 1
          this.slideBarImageIndex -= 1
        }
        else if(mod === 2){
          //如果在最后一张禁止后退
          if(this.imageIndex === this.imagesSize) {
            this.isChangingImage = false
            return
          }
          this.imageIndex += 1
          this.slideBarImageIndex += 1
        }
        else if(mod === 3){
          this.imageIndex = this.slideBarImageIndex
        }
        this.getImages()
        this.removeRec('all')
        this.timeout = setTimeout(()=>{
          this.reDrawTags(1, this.imageIndex)
          console.log('重新绘制矩形框');
        }, 200)
      } else {
        //如果该张图片没有加载完 让 sliderBar跳回去
        this.slideBarImageIndex = this.imageIndex
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
    //创建矩形元素
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
            //转换绘制状态 到正在绘制
            this.isDrawing = true
            //创建元素
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
            //设置元素的左上角位置
            this.recTop = mPos.top
            this.recLeft = mPos.left
            //向矩形框数组添加对象
            let r = {
              //类型
              type: "rectangle",
              //不知道
              occluded: false,
              //z轴层级关系
              z_order: 0,
              //本地渲染使用 不需要提交服务器
              index: this.rectangleIndex,//矩形框序号
              //本地使用
              el: rec,//矩形框DOM元素
              //所在图片序号
              frame: this.imageIndex + this.start_frame,
              //一级标签默认选择第一个
              label_id: this.options[0].value,
              //不知道
              group: 0,
              //下面三个本地渲染使用
              isLock: false, //锁住
              isInvisible: false, //隐藏
              isCover: 0, //0表示未被遮挡，1表示被遮挡
              //属性
              attributes: [],
              //左上 右下 两点数据
              points: [],
            }
            this.rectangleIndex++
            //TODO: 删掉了shapes后面的rectangle
            this.shapes.push(r)
            //渲染到页面上
            this.$refs.recBox.appendChild(rec)
            //根据鼠标位置调整矩形框的大小
            document.body.addEventListener('mousemove', this.resizeRec, false)
          } else {
            this.isDrawing = false
            document.body.removeEventListener('mousemove', this.resizeRec, false)
            //记录矩形框左上，右下两个点的x1,y1,x2,y2坐标在 !原图! 上的坐标
            this.shapes[this.shapes.length - 1].points = [
              (parseInt(this.shapes[this.shapes.length - 1].el.style.left.replace('px', '')) - (parseInt(this.imageInfo.left) + 46)) * this.imageScale,
              (parseInt(this.shapes[this.shapes.length - 1].el.style.top.replace('px', '')) - (parseInt(this.imageInfo.top) + 35)) * this.imageScale,
              (parseInt(this.shapes[this.shapes.length - 1].el.style.width.replace('px', '')) + parseInt(this.shapes[this.shapes.length - 1].el.style.left.replace('px', '')) - (parseInt(this.imageInfo.left) + 46)) * this.imageScale,
              (parseInt(this.shapes[this.shapes.length - 1].el.style.height.replace('px', '')) + parseInt(this.shapes[this.shapes.length - 1].el.style.top.replace('px', '')) - (parseInt(this.imageInfo.top) + 35)) * this.imageScale,
            ]
            console.log('矩形框两点数据', this.shapes[this.shapes.length - 1].points);
            //画完自动保存
            /** 直接调接口*/
            this.saveTagsToStore(this.shapes[this.shapes.length - 1])
            //完成一个标记,切换回鼠标模式
            // this.initDrawTools('cursor')
            this.addTagsToServer( this.shapes[this.shapes.length - 1])
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
      this.shapes[this.shapes.length - 1].el.style.left = left + 'px'
      this.shapes[this.shapes.length - 1].el.style.top = top + 'px'
      this.shapes[this.shapes.length - 1].el.style.width = right - left + 'px'
      this.shapes[this.shapes.length - 1].el.style.height = bottom - top + 'px'
    },
    //清除屏幕上的标记元素 用于切换图片
    removeRec(mod) {
      if (mod === 'all') {
        this.$refs.recBox.innerHTML = ''
        this.shapes = []
        this.rectangleIndex = 1
      }
    },
    //将标注信息存储到store中
    saveTagsToStore(shape) {
      this.$store.commit('saveTagsInfo', shape)
      this.$message({
        message: '自动保存成功',
        type: "success"
      })
    },
    //将标注信息的更改存储到服务器中
    addTagsToServer(shapeInfo){
      let shapes = [shapeInfo]
      this.$http.patch('v1/jobs/' + this.jobId + '/annotations?action=create', {
        shapes: shapes,
        tracks: [],
        tags: [],
        version: this.updateVersion
      }).then((e) => {
        this.updateVersion += 1
        //把服务器分配的id赋值给shapes中
        shapeInfo.id = e.data.shapes[0].id
      }).catch((err) => {
        console.log('标注信息上传错误', err)
      })
    },
    delTagFromServer(shapeIndex){
      this.$http.patch('v1/jobs/' + this.jobId + '/annotations?action=delete', {
        shapes: [this.shapes[shapeIndex]],
        tracks: [],
        tags: [],
        version: this.updateVersion
      }).then((e) => {
        this.updateVersion++
        console.log('删除标注信息返回值', e);
      }).catch((err) => {
        console.log('标注信息删除错误', err);
      })
    },
    //提交前询问
    // TODO: 这里的按钮要大改
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
      //切换到了第几张图片, 这里的index是this.imageindex 也就是从1开始的数字
      let imgIndex = index
      let TagsInfo = []
      let that = this
      if (mod === 1) {
        //从store获取所有的标注信息
        TagsInfo = that.$store.state.imageTags.shapes
      } else if (mod === 2) {
        TagsInfo = that.shapes
        this.removeRec('all')
      }
      //清洗出当前图片的标注信息
      for (let item of TagsInfo) {
        if (item.frame === imgIndex + this.start_frame) {
          // console.log('矩形框在页面上的位置', item.points);
          //创建矩形框
          //TODO: 这里的创建矩形框建议和上面的creatRec中的拿出来做成单独的函数
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
          if(this.isFirstDrawRec){
            setTimeout(() => {
              rec.style.left = parseInt(item.points[0]) / this.imageScale + parseInt(this.imageInfo.left) + 46 + 'px'
              rec.style.top = parseInt(item.points[1]) / this.imageScale + parseInt(this.imageInfo.top) + 35 + 'px'
              rec.style.width = (parseInt(item.points[2]) - parseInt(item.points[0])) / this.imageScale + 'px'
              rec.style.height = (parseInt(item.points[3]) - parseInt(item.points[1])) / this.imageScale + 'px'
              rec.style.cursor = 'default'
              this.$refs.recBox.appendChild(rec)
            }, 100)
            this.isFirstDrawRec = false
          } else {
            rec.style.left = parseInt(item.points[0]) / this.imageScale + parseInt(this.imageInfo.left) + 46 + 'px'
            rec.style.top = parseInt(item.points[1]) / this.imageScale + parseInt(this.imageInfo.top) + 35 + 'px'
            rec.style.width = (parseInt(item.points[2]) - parseInt(item.points[0])) / this.imageScale + 'px'
            rec.style.height = (parseInt(item.points[3]) - parseInt(item.points[1])) / this.imageScale + 'px'
            rec.style.cursor = 'default'
            this.$refs.recBox.appendChild(rec)
          }

          // console.log('标记的真实数据', item)

          //添加数据
          this.shapes.push({
            type: item.type,
            occluded: item.occluded,
            z_order: item.z_order,
            index: this.rectangleIndex,
            el: rec,
            id: item.id,
            frame: item.frame,
            label_id: item.label_id,
            group: item.group,
            //这三个如果时本地有标注数据 就直接用 如果是从服务器获取的就没有数据 默认赋值false
            isLock: item.isLock || false,
            isInvisible: item.isInvisible || false,
            isCover: item.isCover || false,
            attributes: item.attributes,
            points: item.points,
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
      this.shapes[index - 1].el.style.backgroundColor = 'rgba(255,255,255,0.4)'
    },
    hideRecObj(index){
      this.shapes[index-1].el.style.backgroundColor = 'transparent'
    },
    //鼠标放到矩形框高亮右侧信息栏
    //TODO: 删除矩形框后这里会产生错误 切换图片后再切回来就恢复正常
    showLabObj(index){
      let styleid = "style_"+index;
      let object = document.getElementById(styleid);
      object.style.background = '#fcffe1'
    },
    hideLabObj(index){
      let styleid = "style_"+index;
      let object = document.getElementById(styleid);
      object.style.background = 'rgb(255,255,255)'
    },
    //信息栏中的功能
    //更新矩形框(标注对象)标签
    //TODO: 后续的更改标签直接改成选择默认标签 不用每次标注后再更改标签信息
    changeTagInfo(item){
      //更新页面数据： 不用更新，点选的时候是直接绑定的
      //更新仓库数据
      this.$store.commit('changeTagInfo', item)
      //向服务器提交更新
      let shapes = [item]
      this.$http.patch('v1/jobs/' + this.jobId + '/annotations?action=update', {
        shapes: shapes,
        tracks: [],
        tags: [],
        version: this.updateVersion
      }).then(() => {
        this.$message({
          message: "修改已保存",
          type: "success"
        })
      }).catch((err) => {
        console.log('标注信息更新错误', err)
      })
    },
    //锁定
    lockRecObj(index) {
      this.shapes[index - 1].isLock = !this.shapes[index - 1].isLock
      if (this.shapes[index - 1].isLock) {
        this.shapes[index - 1].el.classList.add('rec-obj-lock')
      } else {
        this.shapes[index - 1].el.classList.remove('rec-obj-lock')
      }
    },
    //不可见
    invisibleRecObj(index) {
      if (this.shapes[index - 1].isInvisible) {
        this.shapes[index - 1].el.style.display = 'block'
      } else {
        this.shapes[index - 1].el.style.display = 'none'
      }
      this.shapes[index - 1].isInvisible = !this.shapes[index - 1].isInvisible
    },
    //删除
    deleteRecObj(index) {
      //index是从 1 开始的计数变量
      // console.log(this.shapes, index);
      //在页面上删除元素
      this.shapes[index - 1].el.parentNode.removeChild(this.shapes[index - 1].el)
      //向服务器提交删除请求
      this.delTagFromServer( index-1)
      //向仓库(store)提交删除
      this.$store.commit('delTagInfo', this.shapes[index - 1].id)
      console.log('仓库中信息删除');
      //之后每个元素的序号往前挪
      for (let i = index; i < this.shapes.length; i++) {
        // console.log(this.shapes[i]);
        this.shapes[i].index -= 1
      }
      console.log('本地数据更新后', this.shapes)
      //在本地删除数据
      this.shapes.splice(index - 1, 1)
      //计数变量-1
      this.rectangleIndex--
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
      width: 100%;
      border-bottom: 1px solid #cae7dc;
      .label-info {
        width: 100%;
        height: 30px;
        display: flex;
        .item-index {
          display: block;
          flex: 1;
          padding-left: 20px;
          box-sizing: border-box;
          font-size: 14px;
          line-height: 30px;
          width: 30%;
          overflow: hidden;
        }
        .change-label {
          flex: 4;
          height: 100%;
          box-sizing: border-box;
          padding: 2px;
        }
        .more-function {
          flex: 1;
          height: 100%;

          text-align: center;
          line-height: 30px;
          .el-dropdown-link{
            cursor: pointer;
            color: #333;
          }
          .el-icon-more{
            font-size: 14px;
          }
        }
      }

      .label-func {
        width: 100%;
        height: 50px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        .func {
          width: 30px;
          height: 30px;
          border-radius: 6px;
          transition: background-color 0.2s;
          text-align: center;
          line-height: 30px;
        }
        .func:hover {
          background-color: #b9d4ca;
        }
      }
      .label-add-attr{
        width: 100%;
        height: 20px;
      }
    }
  }
  .switch-images {
    width: 290px;
    height: 40px;
    margin: 5px;
    display: flex;
    .back, .next{
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      span{
        display: block;
        width: 26px;
        height: 26px;
        border-radius: 4px;
        cursor: pointer;
        transition: 0.3s;

        font-size: 26px;
        line-height: 22px;
        text-align: center;
      }
      span:hover{
        background-color: #bbe6d6;
      }
    }
    .slider{
      flex: 5;
      padding: 0 5px;
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
