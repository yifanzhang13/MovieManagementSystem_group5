import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI)

// 全局函数及变量插件install
import Global from './global'
Vue.use(Global)

import Vant from 'vant'
import 'vant/lib/index.css'
Vue.use(Vant) // 插件

import dex from '@/dex'
Vue.use(dex)

import JsonViewer from '../node_modules/vue-json-viewer'
Vue.use(JsonViewer)

// bmob sdk start     -> npm install hydrogen-js-sdk
import Bmob from "hydrogen-js-sdk"
Bmob.initialize("62b086557287e938", "A3211B")
Vue.prototype.Bmob = Bmob
Bmob.debug(true)
// bmob sdk end

// 全局注册
import './assets/icon' // icon
// Vue.component('icon-svg', IconSvg)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
