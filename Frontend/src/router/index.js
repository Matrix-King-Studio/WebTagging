import Vue from 'vue'
import VueRouter from 'vue-router'

const LoginPage = () => import(/* webpackChunkName: "loginPage" */ '../views/LoginPage.vue')

const Home = () => import(/* webpackChunkName: "home" */ '../views/Home.vue')
const Project = () => import(/* webpackChunkName: "home" */ '../components/allproject/project.vue')
const Manage = () => import(/* webpackChunkName: "home" */ '../components/management/setting.vue')
const Usercenter = () => import(/* webpackChunkName: "home" */ '../components/usercenter/user.vue')
const NewProject = () => import(/* webpackChunkName: "home" */ '../components/newproject/newproject.vue')
// import Home from '../views/Home.vue'
// import Project from '../components/allproject/project.vue'
// import Manage from '../components/management/setting.vue'
// import Usercenter from '../components/usercenter/user.vue'
// import NewProject from '../components/newproject/newproject.vue'

const WorkBench = () => import(/* webpackChunkName: "workBench" */ '../views/workbench.vue')
const DrawPage = () => import(/* webpackChunkName: "workBench" */ '../components/workbench/drawPage.vue')
const Setting = () => import(/* webpackChunkName: "workBench" */ '../components/workbench/setting.vue')
// import Workbench from '../views/workbench.vue'

Vue.use(VueRouter)

//路由匹配规则
const routes = [
  { path: '/', redirect: 'login' },
  { path: '/login', component: LoginPage },
  {
    path: '/home',
    redirect: '/home/project',
    component: Home,
    children: [
      { path: 'project', component: Project },
      { path: 'management', component: Manage },
      { path: 'user', component: Usercenter },
      { path: 'newproject', component: NewProject }
    ]
  },
  {
    path: '/workbench',
    component: WorkBench,
    children: [
      { path: 'task/:index', component: DrawPage },
      { path: 'setting', component: Setting }
    ]
  }
]

//路由对象
const router = new VueRouter({
  routes
})

//挂载路由导航守卫
router.beforeEach((to, from, next) => {
  //to: 将要访问的路径， from：从哪个路径跳转来， next： 放行路径, next('url'):强制跳转
  if(to.path === '/login') return next()
  const tokenStr = window.sessionStorage.getItem('token')
  if(!tokenStr) return next('/login')
  next()
})

export default router
