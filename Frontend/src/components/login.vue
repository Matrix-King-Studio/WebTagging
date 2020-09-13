<template>
  <div class="login-comp-box">
    <div class="title">
      安软标记平台
    </div>
    <form :model="loginForm">
      <input
        v-show=" whichmode === 'login' || whichmode === 'register' "
        id="uname"
        v-model="loginForm.username"
        type="text"
        placeholder="账户名"
      >
      <input
        v-show="whichmode === 'register' || whichmode === 'forget'"
        id="email"
        ref="email"
        v-model="loginForm.email"
        type="email"
        placeholder="邮箱"
        @keyup="correctEmail"
      >
      <input
        v-show="whichmode === 'login'"
        id="passwd"
        v-model="loginForm.password"
        type="password"
        placeholder="账户密码"
      >
      <input
        v-show="whichmode === 'register'"
        id="passwd1"
        ref="passwd1"
        v-model="loginForm.password1"
        type="password"
        placeholder="设置密码"
        @keyup="correctpasswd()"
      >
      <input
        v-show="whichmode === 'register'"
        id="passwd2"
        ref="passwd2"
        v-model="loginForm.password2"
        type="password"
        placeholder="重复密码"
        @keyup="isSame()"
      >
      <div class="err-box">
        <!--        我太笨了，这块写的太辣鸡了，又想不到好的解决方案，只能重复好几遍这样子，才能满足得了需求 -->
        <div class="err-info">
          {{ err1 }}
        </div>
        <div class="err-info">
          {{ err2 }}
        </div>
        <div class="err-info">
          {{ err3 }}
        </div>
        <div class="err-info">
          {{ err4 }}
        </div>
      </div>
    </form>
    <div class="login-btn-box">
      <input
        class="login-btn"
        type="button"
        :value="text1"
        @click="whichMod"
        @keydown.enter="whichMod"
      >
      <div
        ref="errbtn"
        class="login-status"
      >
        error
      </div>
    </div>
    <div class="btnbox">
      <input
        class="regis-btn"
        type="button"
        :value="text2"
        @click="changeMod(1)"
      >
      <input
        class="forget-btn"
        type="button"
        :value="text3"
        @click="changeMod(2)"
      >
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      // 表单数据
      loginForm: {
        username: '',
        email: '',
        password: '',
        password1: '',
        password2: ''
      },

      // 按钮文字
      text1: '登录',
      text2: '注册',
      text3: '忘记密码',

      // 防止重复点击
      flag: 1,

      // 是否处于注册状态
      whichmode: 'login',

      // 所填数据是否都合法
      rightEmail: 0,
      rightPassword: 0,
      isReady: 0,

      // 填写错误信息
      err1: '',
      err2: '',
      err3: '',
      err4: ''
    }
  },
  methods: {
    // 点击按钮后先判断处于登录注册哪个状态，再调用相应的方法
    whichMod () {
      if (this.whichmode === 'login') this.login()
      else if (this.whichmode === 'register') this.register()
      else if (this.whichmode === 'forget')this.forget()
    },
    // 登陆的数据传输
    login () {
      if (this.flag) {
        // 点击登录2秒后才能再次点击
        this.flag = 0
        let e = this // 闭包
        setTimeout(function () { e.flag = 1 }, 2000)
        this.$http.post('v1/auth/login', this.loginForm).then(e => {
          if (e.data.key) { // 登录成功(有key值)(e.data.key)
            console.log(e.data.key)
            window.sessionStorage.setItem('token', e.data.key)
            this.showSucLoginBtn()
            let t = this
            setTimeout(function () {
              t.$router.push('/home')
            }, 800)
          } else { // 登录失败
            var errinfo
            if (!this.loginForm.username || !this.loginForm.password) {
              errinfo = '请填写用户名或密码'
            } else {
              errinfo = '用户名或密码错误'
            }
            this.showErrLoginBtn(errinfo)
          }
        })
      }
    },
    // 注册的数据传输
    register () {
      console.log(1)
      if (this.rightEmail && this.rightPassword && this.flag) {
        this.flag = 0
        console.log(this.flag)
        var e = this // 闭包
        setTimeout(function () { e.flag = 1 }, 2000)
        this.$http.post('v1/auth/register', this.loginForm).then(e => {
          console.log(e.data)
          this.changeMod(1)
        })
      }
    },
    // 忘记密码的数据传输
    forget () {
      console.log(2)
    },
    // 登录成功或失败后按钮显示效果
    showSucLoginBtn () {
      var e = this.$refs.errbtn.style
      e.top = '0px'
      e.backgroundColor = '#75ff88'
      this.$refs.errbtn.innerText = '登录成功'
      setTimeout(function () {
        e.top = '30px'
      }, 1500)
    },
    showErrLoginBtn (errinfo) {
      var e = this.$refs.errbtn.style
      e.top = '0px'
      e.backgroundColor = '#ff5f5f'
      this.$refs.errbtn.innerText = errinfo
      setTimeout(function () {
        e.top = '30px'
      }, 1500)
    },
    // 转换登录注册和忘记密码状态
    changeMod (n) {
      // 1 是点击左下的按钮
      if (n === 1) {
        if(this.whichmode === 'login' || this.whichmode === 'forget'){
          this.whichmode = 'register'
          this.text1 = '注册'
          this.text2 = '登录'
          this.text3 = '忘记密码'
        } else if (this.whichmode === 'register'){
          this.whichmode = 'login'
          this.text1 = '登录'
          this.text2 = '注册'
          this.text3 = '忘记密码'
        }
      } else if (n === 2){//2 是点击右下角的按钮
        if(this.whichmode === 'login' || this.whichmode === 'register'){
          this.whichmode = 'forget'
          this.text1 = '发送邮件'
          this.text2 = '注册'
          this.text3 = '登录'
        } else if (this.whichmode === 'forget'){
          this.whichmode = 'login'
          this.text1 = '登录'
          this.text2 = '注册'
          this.text3 = '忘记密码'
        }
      }
      this.clearErr()
    },
    //判断密码质量
    correctpasswd () {
      var passwdReg = /^(?=.*[0-9])(?=.*[a-zA-Z])(.{8,20})$/
      if (passwdReg.test(this.loginForm.password1)) {
        this.$refs.passwd1.style.border = '2px solid #75ff88'
        this.err3 = ''
      } else {
        this.$refs.passwd1.style.border = '2px solid #ff5f5f'
        this.err3 = '必须是8位数字与字母组合'
      }
    },
    // 判断两次输入的密码是否相同
    isSame () {
      if (this.loginForm.password1 !== this.loginForm.password2) {
        this.$refs.passwd2.style.border = '2px solid #ff5f5f'
        this.err4 = '两次密码不相同'
        this.rightPassword = 0
      } else {
        this.$refs.passwd2.style.border = '2px solid #75ff88'
        this.err4 = ''
        this.rightPassword = 1
      }
    },
    // 邮箱正则验证
    correctEmail () {
      var reg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if (reg.test(this.loginForm.email)) {
        this.$refs.email.style.border = '2px solid #75ff88'
        this.err2 = ''
        this.rightEmail = 1
      } else {
        this.$refs.email.style.border = '2px solid #ff5f5f'
        this.err2 = '邮箱格式错误'
        this.rightEmail = 0
      }
    },
    //转换模式时清除报错信息
    clearErr(){
      this.err1 = ''
      this.err2 = ''
      this.err3 = ''
      this.err4 = ''
    }
  }
}
</script>

<style lang="less" scoped>
.login-comp-box{
  width: 100%;
  height: 100%;
  background-color: transparent;
  .title{
    text-align: center;
    color: white;
    font-size: 24px;
    letter-spacing: 3px;

    -moz-user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }
  form{
    margin-top: 100px;
    position: relative;
    input{
      display: block;
      border: 1px solid #eeeeee;
      height: 30px;
      width: 300px;
      margin: 8px auto;
      outline: none;
      border-radius: 6px;
      padding-left: 10px;
      box-sizing: border-box;
    }
    .err-box{
      width: 200px;
      height: 144px;
      position: absolute;
      top: 0;
      right: -55px;
      .err-info{
        height: 30px;
        width: 100%;
        margin: 0 auto 8px auto;
        color: #ff5f5f;
        font-size: 14px;
        line-height: 40px;
      }
    }
  }
  .login-btn-box{
    width: 300px;
    height: 30px;
    margin: 8px auto;
    overflow: hidden;
    border-radius: 6px;
    position: relative;
    .login-btn{
      display: block;
      border: 0;
      height: 30px;
      width: 300px;
      outline: none;
      background-color: #51b5ff;
      color: #eeeeee;
      font-size: 14px;
      letter-spacing: 3px;
      cursor: pointer;
    }
    .login-status{
      height: 30px;
      width: 300px;
      background-color: #ff5f5f;
      position: absolute;
      transition: top .2s ease;
      top: 30px;
      color: #ffffff;
      text-align: center;
      line-height: 30px;

      -moz-user-select: none;
      -webkit-user-select: none;
      -ms-user-select: none;
      user-select: none;
    }
  }
  .btnbox{
    width: 300px;
    margin: 8px auto;
    .regis-btn,.forget-btn{
      width: 150px;
      background-color: transparent;
      border: 0;
      outline: none;
      color: white;
      cursor: pointer;
    }
  }
}
</style>
