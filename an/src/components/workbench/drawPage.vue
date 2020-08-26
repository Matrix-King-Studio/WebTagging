<template>
	<div class="main-box">
		<div class="sidebar">
			<el-tooltip
				:class="['item','tools',{'tool-active':flag === 'cursor'}]"
				effect="dark"
				content="鼠标"
				placement="right">
				<el-button @click="initDrawTools('cursor')">
					<span class="iconfont">&#xe6c7;</span>
				</el-button>
			</el-tooltip>
			<span class="line"></span>
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
		<div class="object-bar" ref="objBar">
			<div class="drawer" ref="drawer" @click="showBar()">
				<i :class="[{'el-icon-right':flag2},{'el-icon-back':!flag2}]"></i>
			</div>
			<div class="label-obj-box">
				<div class="label-obj">
					<div class="label-info">
						<span>info</span>
						<div class="change-label">
							<el-select
								v-model="value"
								placeholder="请选择"
								size="mini"
							>
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
					<div class="label-func">
						<div class="func lock">
							<i :class="[{'el-icon-lock':lock},{'el-icon-unlock':!lock}]"></i>
						</div>
						<div class="func visible">
							<span class="iconfont">&#xe9c1;</span>
						</div>
						<div class="func delete">
							<i class="el-icon-delete"></i>
						</div>
					</div>
				</div>
			</div>
			<div class="main-btn-box">
				<div class="images">
					<el-pagination
						small
						background
						layout="prev, pager, next"
						:total="200"
						:pager-count="5"
					>
					</el-pagination>
				</div>
				<div class="main-func">
					<div class="main-btn commit">
						<span>提交</span>
					</div>
					<div class="main-btn skip">
						<span>废弃</span>
					</div>
				</div>
			</div>
		</div>
		<div class="paint-box">
			<canvas width="500px" height="400px" id="myCanvas"></canvas>
		</div>
	</div>
</template>

<script>
    import { DrawTools } from '@/assets/js/DrawTools'
    import JSZip from '@/assets/js/jszip'

    export default {
        created() {
            this.getImagesInfo()
            this.getImages()
        },
        mounted() {
            this.initCanvas()
        },
        data() {
            return {
                //哪一个工具
                flag: 'cursor',
                //项目栏是否展开
                flag2: true,
                //要改到每一个元素的身上
                lock: false,

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
                value: '',

                //画笔相关
                drawUtil: {},
                tempStrokeStyle: 'blue',
                tempLineWidth: 1,
                imgPath: require('../../assets/image/1.png'),

            }
        },
        methods: {
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
            getImagesInfo() {
                this.$http.get('v1/tasks/' + this.$route.params.index + '/data/meta').then(e => {
                    // console.log(e);
                })
            },
            getImages() {
                // serverProxy.frames.getData(this.$route.params.index, 0).then(res => {
                //     console.log(res)
				// })
                this.$http.get('v1/tasks/' + this.$route.params.index + '/data', {
                    params: {
                        type: 'chunk',
                        number: 0,
                        quality: 'compressed'
                    },
                    responseType: 'arraybuffer',
                }).then(e => {
                    console.log(e)
                    const zip = new JSZip()
                    if (e.data) {
                        zip.loadAsync(e.data).then((_zip) => {
                            console.log(_zip)
                        })
                    }
                }).catch(err => {
                    console.log(err)
				})
            },
            initCanvas() {
                //加载画笔工具
                this.drawUtil = new DrawTools()
                //初始化
                this.drawUtil.init({
                    'canvasId': 'myCanvas',
                })
                //赋值给全局对象？？？
                window.drawUtil = this.drawUtil
                //设置样式
                this.drawUtil.setStyle({
                    lineWidth: this.tempLineWidth,//线条宽度
                    strokeStyle: this.tempStrokeStyle,//画笔颜色
                    fillStyle: 'red',//填充色
                    lineJoin: 'round',//线条交脚样式
                    lineCap: 'round'//线条结束样式
                })
                //打印canvas大小
                this.drawUtil.resizeCanvas()
                //加载图片
                this.drawUtil.setBgPic(this.imgPath)
            },
            initDrawTools(attr) {
                //处于相应的工具状态
                this.flag = attr
                //选择画笔
                this.drawUtil.begin(attr)
                //结束的回调函数
                this.drawUtil.callback({
                    end: function (points, radius, realPoints) {
                        //points,radius屏幕显示的坐标,圈选的半径；realPoint图片实际大小的对应坐标(服务端实际裁剪可使用)
                        //realRadiusObj图片实际半轴对象，虽然视野中画的是圈选，但是实际中可能是椭圆a,b轴(服务端实际裁剪可使用),
                        for (let i in points) {
                            //points屏幕显示的坐标
                            console.log('x坐标：' + points[i].getX() + ' y坐标：' + points[i].getY())
                            //realPoint图片实际大小的对应坐标(服务端实际裁剪可使用)
                            console.log('x坐标realPoints：' + realPoints[i].getX() + ' y坐标realPoints：' + realPoints[i].getY())
                        }
                    }
                })
            },
            unzipImages(start, end, block) {
                let zip = new JSZip()
                zip.loadAsync(block).then((zip) => { // 读取zip
                    let index = start
                    zip.forEach((relativePath) => {
                        const fileIndex = index++
                        if (fileIndex <= end) {
                            zip.file(relativePath).async('blob').then((fileData) => {
                                console.log(fileData)
                            })
                        }
                    })
                })

                // JSZip.loadAsync(images,{ base64:true })

                // zipJS.createReader( new zipJS.Data64URIReader('base64'), reader=>{
                //
                // })
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

			.label-obj {
				height: 80px;
				width: 100%;
				border-bottom: 1px solid #cae7dc;

				.label-info {
					width: 100%;
					height: 30px;

					span {
						display: block;
						float: left;
						margin-left: 20px;
						font-size: 14px;
						line-height: 30px;
						width: 100px;
						overflow: hidden;
					}

					.change-label {
						float: right;
						height: 100%;
						width: 140px;
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
						margin: 10px 30px;
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
		}

		.main-func {
			width: 290px;
			height: 80px;
			margin: 5px;
			padding: 0 15px;
			box-sizing: border-box;

			.main-btn {
				width: 90px;
				height: 40px;
				float: left;
				margin: 10px 20px;
				border-radius: 10px;
				background-color: #bbe6d6;
				line-height: 40px;
				text-align: center;
				letter-spacing: 4px;
				font-size: 16px;
				transition: all 0.2s;
			}

			.main-btn:hover {
				background-color: #b1eed8;
			}
		}
	}

	.paint-box {
		margin: 35px 0 0 46px;
		box-sizing: border-box;
		width: 100%;
		height: 100%;
		background-color: #eeeeee;

	}
</style>
