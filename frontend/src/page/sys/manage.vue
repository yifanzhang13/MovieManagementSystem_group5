<template>
  <div class="manage_page fillcontain">
    <el-container>
      <el-header>
        <head-top @on_collapse_event="onCollapse"></head-top>
      </el-header>
      <el-main>
        <div class="content-wrap">
          <router-view/>
        </div>

        <div v-if="isManagePage" class="main-area">
          <div style="font-size: 32px; letter-spacing: 8px;margin-top: 100px;">欢迎使用{{sysDescState.name}}</div>
        </div>

        <!--<div class="el-main-footer">
          © 2019~2020
          All Rights Reserved
        </div>-->
      </el-main>
    </el-container>
  </div>
</template>

<script>
  import {oscarMixin} from '@/config/mixins'
  import {option_line1,option_map} from '@/config/echart.option'
  import {mapState} from 'vuex'
  import HeadTop from './components/HeadTop'

  export default {
    mixins: [oscarMixin],
    components: {
      HeadTop
    },
    created() {
    },
    mounted() {
      this.addTabPage(this.$route)
      this.showBookDiv = true
    },
    data() {
      return {
        isCollapse: false,
        showBookDiv: false,
        menus: [],
        isManagePage: true, // 是否为首页
        stat: {},
        option: {},
        optionMap: {},
        noticePopupSet: new Set() // 已经展示过的通知ID集合
      }
    },
    computed: {
      ...mapState(['sysDescState']),
      defaultActive: function() {
        return this.$route.path
      },
      openTabPages() { // tab打开的url列表
        return this.$store.state.openTabPages
      },
      activeTabIndex: { // 当前打开的页面
        get() {
          return this.$store.state.activeTabIndex
        },
        set(val) {
          this.$store.commit('set_active_index_mutation', val)
        }
      },
    },
    watch: {
      '$route'(to) { // 监听router变化
        this.addTabPage(to)
      }
    },
    methods: {
      async loopNotification() { // 轮训通知
        const res = await this.$findList({url: '/tb/cms/notice/list'})
        if (res.code === 0 && res.data.length > 0) {
          const id = res.data[0].id
          if (!this.noticePopupSet.has(id)) {
            this.noticePopupSet.add(id)
            this.$notify({
              title: res.data[0].name,
              message: res.data[0].remarks,
              position: 'bottom-right'
            })
          }
        }
      },
      addTabPage(to) {
        this.isManagePage = (to.path === '/manage')

        console.log(this.isManagePage)
        if (this.isManagePage) {
          to = {
            path: to.path,
            name: '首页'
          }
        }

        let isTabOpened = false // tab页是否已经存在了
        for (const openPage of this.openTabPages) {
          if (openPage.path === to.path) {
            isTabOpened = true
            this.$store.commit('set_active_index_mutation', to.path)
            break
          }
        }
        if (!isTabOpened) {
          this.$store.commit('add_tab_mutation', to)
          this.$store.commit('set_active_index_mutation', to.path)
        }
      },
      async getMenus() {
        const _data = await this.$findList({url: '/sys/menu/list'})
        if (_data.code === 0) { this.menus = _data.data }
      },
      async configInit() {
        // 查询统计数据，用户数，模块数，访问量
        const stat = await this.$findList({url: '/sys/main/stat'})
        if (stat.code === 0) this.stat = stat.data

        this.option = option_line1()
        this.optionMap = option_map()
      },
      onCollapse(value) {
        this.isCollapse = value
      },
      // tab切换时，动态的切换路由
      tabClick() {
        let path = this.activeTabIndex;
        // 用户详情页，对应了二级路由，需要拼接添加第二级路由，暂时未用
        if (this.activeTabIndex === '/userInfo') {
          path = this.activeTabIndex + '/' + this.$store.state.userInfo.name;
        }
        this.$router.push({path: path});
      },
      tabRemove(routePath) {
        // 首页不可删除
        if (routePath === '/manage') {
          return
        }

        this.$store.commit('delete_tab_mutation', routePath);
        if (this.activeTabIndex === routePath) {
          // 设置当前激活的路由
          if (this.openTabPages && this.openTabPages.length >= 1) {
            this.$store.commit('set_active_index_mutation', this.openTabPages[this.openTabPages.length - 1].path);
            this.$router.push({path: this.activeTabIndex})
          } else {
            this.$router.push({path: '/manage'})
          }
        }
      },
      tabCloseCurrentHandle() {
        this.tabRemove(this.activeTabIndex)
      },
      tabCloseOtherHandle() {
        const currentIndex = this.activeTabIndex, that = this
        this.openTabPages.filter(item => item.path !== currentIndex)
            .forEach(p => {
              that.tabRemove(p.path)
            })
      },
      tabCloseAllHandle() {
        const commit = this.$store.commit
        this.openTabPages.map(x => x.path).forEach(path => {
          commit('delete_tab_mutation', path)
        })
        this.$router.push({path: '/manage'})
      }
    }
  }
</script>

<style lang="less" scoped>
  .icon{
    font-size: 150px;
  }
  //过度动画
  .right-trans-enter-active, .right-trans-leave-active{
    transition: all 1.8s ease-out;
  }
  .right-trans-enter{
    transform: translateX(100px);
    opacity: 0;
  }
  .stat-trans1-enter-active, .stat-trans1-leave-active{
    transition: all .8s ease-out;
  }
  .stat-trans2-enter-active, .stat-trans2-leave-active{
    transition: all 1.2s ease-out;
  }
  .stat-trans3-enter-active, .stat-trans3-leave-active{
    transition: all 1.6s ease-out;
  }
  .stat-trans1-enter,.stat-trans2-enter,.stat-trans3-enter{
    transform: translateY(-500px);
    opacity: 0;
  }

  .el-menu {
    background-color: @header-background-color;
  }

  .manage_page {
    display: flex;
  }

  .el-header {
    padding: 0;
  }

  .el-main {
    padding: 0 0 0 0;
  }

  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }

  .logo-text {
    color: white;
    font-size: 20px;
    top: -28px;
    margin-right: 10px;
    position: relative;
  }

  .div-logo {
    padding: 6px;
    height: 84px;
    width: 100%;
    min-width: 160px;
  }

  .div-logo img {
    width: 64px;
  }

  .site-tabs__tools {
    position: fixed;
    top: 60px;
    right: -27px;
    padding: 0 12px;
    font-size: 16px;
    line-height: 40px;
    background-color: #f1f4f5;
    cursor: pointer;
    .el-icon--right {
      margin-left: 0;
    }
  }

  .chart-area {
    padding: 10px;
    position: relative;
  }

  .chart-area /deep/ .el-card__body {
    height: 69px;
    text-align: center;
  }
  .el-row-1 /deep/ .el-card:hover{
    background: @theme-bg-color;
    cursor: pointer;
  }

  .echart-card1 /deep/ .el-card__body {
    height: 280px;
  }

  .echart-card2 /deep/ .el-card__body {
    height: 200px;
  }

  .echart-card-col /deep/ .el-card__body {
    padding: 0;
    height: 240px !important;
  }

  .el-main-footer {
    padding: 6px 6px 6px 480px;
    height: 20px;
    font-size: 12px;
    color: #fff;
    letter-spacing: 0.8px;
    z-index: 99;
    position: fixed;
    bottom: 0;
    width: 100%;
    background-color: @header-background-color;
  }
  .main-area{
    text-align: center;
    /*background: -webkit-linear-gradient(left, #ffe789, #ece64825);*/
    height: calc(100% - 56px);
  }
</style>
