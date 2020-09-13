import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
// 导入全局样式表
import './assets/css/global.css'
// 导入字体图标
import './assets/font/iconfont.css'
// 导入axios
import axios from 'axios'
//导入element ui
import './plugins/element.js'

// 配置请求根路径
axios.defaults.baseURL = 'http://alexking.site:8080/api/'
// axios.defaults.timeout = 3000 //超时时间

// 请求拦截器添加请求头
axios.interceptors.request.use(config => {
  if(window.sessionStorage.getItem('token')){
    config.headers.Authorization = "Token " + window.sessionStorage.getItem('token')
  }
  return config
})

Vue.prototype.$http = axios

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App),

})
