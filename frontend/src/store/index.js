import Vue from 'vue'
import Vuex from 'vuex'
import {getList} from '@/api'
import {Storage} from '@/common/tool'

import user from './modules/user'
import shoppingCart from './modules/shoppingCart'

Vue.use(Vuex)

const state = {
  openTabPages: [], // 打开的tab页
  activeTabIndex: '',// 当前激活的tab页

  userInfoState: {},
  sysDescState: {}, // 系统信息
  headInfoState: [] // 导航的metadata
}

// 同步  this.$store.commit('clearUserMutation')
// https://www.jianshu.com/p/4450b63a27fe
const mutations = {
  clearUserMutation(state, payload) {
    state.userInfoState = {}
    state.sysDescState = {}
    state.activeTabIndex = ''
    state.openTabPages = []
  },
  userMutation(state, payload) {
    state.userInfoState = payload
  },
  sysDescMutation(state, payload) {
    state.sysDescState = payload
  },
  routeMutation(state, payload) {
    state.headInfoState = payload
    // payload.forEach(d => {
    //   state.headInfoState.set(d.path, d.meta)
    // })
  },

  // 设置当前激活的tab
  set_active_index_mutation(state, index) {
    this.state.activeTabIndex = index
  },
  // 添加tabs
  add_tab_mutation(state, data) {
    this.state.openTabPages.push(data)
  },
  // 删除tabs
  delete_tab_mutation(state, route) {
    let index = 0
    for (const openTabPage of state.openTabPages) {
      if (openTabPage.path === route) break
      index++;
    }
    this.state.openTabPages.splice(index, 1)
  },
}

// 面向用户的接口 异步 this.$store.dispatch('initRouteAction', args)
const actions = {
  async initRouteAction({commit, state}) {
    try {
      const res = await getList({url: '/sys/menu/router'})
      res.code == 0 && commit('routeMutation', res.data)
    } catch (err) {
      throw new Error(err)
    }
  },
  clearUserAction({commit, state}) { // before logout system
    try {
      Storage.remove("user_info")
      commit('clearUserMutation', {})
    } catch (err) {
      throw new Error(err)
    }
  },
  async initUserAction({commit, state}) {
    try {
      const userInfo = Storage.get("user_info")
      console.log("get userInfo from storage.")
      if (userInfo) { commit('userMutation', JSON.parse(userInfo)) }
    } catch (err) {
      throw new Error(err)
    }
  },
  async initSysDescAction({commit, state}) { // 初始化
    try {
      const res = await getList({url: '/sys/desc/list',type: 'system'})
      res.code == 0 && commit('sysDescMutation', res.data[0])
    } catch (err) {
      throw new Error(err)
    }
  },
}

export default new Vuex.Store({
  modules: {
    // app: import('./modules/app'),
    user,
    shoppingCart
  },
  state,
  actions,
  mutations
})
