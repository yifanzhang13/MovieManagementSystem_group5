<template>
  <div>
    <label v-for="menu in menus">
      <el-submenu v-if="menu.children && menu.children.length>0 " :index="menu.index">
        <template slot="title">
          <i :class="menu.icon"></i>
          <span class="menu-title"> {{menu.name}}</span>
        </template>
        <base-menu :menus="menu.children"></base-menu>
      </el-submenu>

      <el-menu-item v-else :index="menu.index">
        <i :class="menu.icon"></i>
        <span slot="title">{{menu.name}}</span>
      </el-menu-item>
    </label>
  </div>
</template>

<script>
  export default {
    name: 'BaseMenu',
    props: {
      menus: {
        type: Array,
        default: () => []
      }
    },
    data() {
      return {}
    },
    methods: {}
  }
</script>

<style scoped>
  .el-menu--collapse .el-submenu .menu-title {
    height: 0;
    width: 0;
    overflow: hidden;
    visibility: hidden;
    display:inline-block;
  }
</style>
