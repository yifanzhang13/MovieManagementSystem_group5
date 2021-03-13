import Vue from 'vue'
import Router from 'vue-router'
import {Storage} from '@/common/tool'

import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

Vue.use(Router)

NProgress.inc(0.2)
NProgress.configure({easing: 'ease', speed: 500, showSpinner: true})

const routes = [
  {path: '/', component: () => import('@/page/sys/login')},
  {path: '/register', component: () => import('@/page/sys/register')},

  {
    path: '/manage', name: '首页', component: () => import('@/page/sys/manage'),
    children:
      [
        // 懒加载，注释还是有必要的，打包后知道是哪个页面
        {path: '/user/center', name: '用户中心', component: () => import(/* webpackChunkName: "user-center" */ '@/page/sys/user-center')},
        {path: '/user', name: '用户管理', component: () => import(/* webpackChunkName: "user" */ '@/page/sys/user')},

        // business route start
        {path: '/tb_movie', name: '主页', component: r => require.ensure([], () => r(require('@/page/module/tb_movie')), 'module')},
        {path: '/tb_movie_detail', name: '电影介绍', component: r => require.ensure([], () => r(require('@/page/module/tb_movie_detail')), 'module')},
        {path: '/tb_movie_category', name: '分类', component: r => require.ensure([], () => r(require('@/page/module/tb_movie_category')), 'module')},
        // business route end
      ]
  }
]

const createRouter = () => new Router({
  mode: 'history', // or hash
  // base: process.env.BASE_URL,
  routes: routes,
  strict: process.env.NODE_ENV !== 'production'
})

const router = createRouter()

const whiteList = ['/f/', '/f_', '/front/', '/m/', '/static/', '/register', '/wanglei'] // 白名单
router.beforeEach((to, from, next) => {
  NProgress.start()

  let pass = false
  for (let i = 0; i < whiteList.length; i++) {
    if (to.path.indexOf(whiteList[i]) == 0) {
      pass = true
    }
  }

  if (pass) {
    // web front need not check
  } else {
    if (Storage.tokenValid()) {
      if (to.path === '/') {
        next('/manage')
        NProgress.done()
      }
    } else {
      if (to.path !== '/') {
        next('/')
        NProgress.done()
      }
    }
  }

  // console.log("store index.js", router.app.$route)
  next()
})

router.afterEach(() => {
  NProgress.done()
})

/* 由于Vue-router在3.1之后把$router.push()方法改为了Promise。所以假如没有回调函数，错误信息就会交给全局的路由错误处理。
vue-router先报了一个Uncaught(in promise)的错误(因为push没加回调) ，然后再点击路由的时候才会触发NavigationDuplicated的错误(路由出现的错误，全局错误处理打印了出来)。*/
// 禁止全局路由错误处理打印
const originalPush = Router.prototype.push;
Router.prototype.push = function push(location, onResolve, onReject) {
  if (onResolve || onReject) { return originalPush.call(this, location, onResolve, onReject) }
  return originalPush.call(this, location).catch(err => err)
}
export default router
