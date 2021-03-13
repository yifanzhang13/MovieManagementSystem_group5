<template>
  <div id="app" class="fillcontain">
    <transition name="fade" mode="out-in">
      <router-view></router-view>
    </transition>
  </div>
</template>

<script>
</script>

<style lang="less" scoped>
  // style中包含@import，会再发一次请求把@import指向的css文件引进来
  /* @import后的字符串会被 css-loader 视为绝对路径解析，因为并没有添加 css-loader 的 alias，所以会报找不到 @ 目录*/
  /* Webpack会将以 ~ 开头的路径视作依赖模块而去解析，这样@的 alias 配置就能生效了*/
  /*@import "~@/assets/icon/iconfont.css";*/
</style>
