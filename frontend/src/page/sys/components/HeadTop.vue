<template>
  <div class="header-container">

    <div class="headbar">
      <div>
        <el-link type="primary" href="/tb_movie">MovieStar</el-link>
        <el-divider direction="vertical"></el-divider>
        <el-link type="primary" href="/tb_movie_category">Rating</el-link>
      </div>
      <el-dropdown @command="handleCommand">
        <div class="top-welcome">
          <img src="/static/img/ic_dog.png" class="avator">
          <i>Welcome！</i>
          <span style="font-weight: bold;">{{ userInfoState.cnName }}</span>
<!--          <span style="color: #ffeb3b;">({{ userInfoState.roleName }})</span>-->
        </div>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item class="el-icon-user-solid" command="userCenter">
            User Center
          </el-dropdown-item>
          <el-dropdown-item command="logout">
            <svg-icon icon-class="exit"></svg-icon>Exit
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
  import {logout} from '@/api'
  import {mapActions, mapState} from 'vuex'
  import {Storage} from '@/common/tool'

  export default {
    data() {
      return {
        collapseIcon: 'el-icon-caret-left arrow-collapse',
        isCollapse: false,
      }
    },
    created() {
      if (!Storage.get("user_info")) {
        this.$router.push('/')
        return
      }
      if (this.headInfoState.length === 0) { // f5 refresh
        // this.initRouteAction()
      }
      this.initUserAction()
    },
    computed: {
      ...mapState(['userInfoState', 'headInfoState']), // mapState通过扩展运算符将store.state.userInfoState 映射到vue对象上
      headMeta: vm => {
        // console.log(this.headInfoState)
        // console.log(vm.$store.state.headInfoState)
        // console.log(vm.$route.path)
        const my = vm.$store.state.headInfoState.filter(item => {
          return item.path === vm.$route.path
        })
        return my.length > 0 ? my[0].meta : []
      }
    },
    methods: {
      ...mapActions(['initRouteAction', 'initSysDescAction', 'initUserAction', 'clearUserAction']),
      async handleCommand(command) {
        if (command === 'userCenter') {
          this.$router.push('/user/center')
        } else if (command === 'logout') {
          // const res = await logout()
          const res = {
            "code": 0,
            "type": "success",
            "message": "Success"
          }
          this.$msg(res, () => {
            Storage.removeToken()
            this.clearUserAction()
            this.$router.push('/')
          })
        }
      },
    }
  }
</script>

<style lang="less">
  .headbar {
    .el-dropdown, .el-breadcrumb__inner {
      color: @header-font-color;
    }
  }

  .header-container {
    //background-color: #324157;
    background-color: @header-background-color;
    height: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-left: 20px;
  }

  .headbar {
    display: flex;
    justify-content: space-between;
    width: 100%;
    align-items: center;
  }

  .el-dropdown {
    margin-right: 30px;
  }

  .arrow-collapse {
    margin-right: 10px;
    cursor: pointer;
    transition: all 0.5s ease-in-out;
  }

  .arrow-collapse:hover {
    transform: rotate(360deg);
  }
  .top-welcome{
    cursor: pointer;
    .avator {
      .wh(26px, 26px);
      border-radius: 50%;
      vertical-align: middle;
      transition: all 0.9s ease 0s;
    }
    i{
      transition: all 0.9s ease 0s;
    }
  }

  .top-welcome:hover{ //hover下的img
    img,i{
      transform: scale(1.5) translateX(-5px);
      box-shadow: 0 0 0 2px #f7f5ec;
    }
  }

</style>
