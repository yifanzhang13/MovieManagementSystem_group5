exports.install = function(Vue) {
  Vue.prototype.notifySucceed = function(msg) {
    this.$notify({
      title: "成功",
      message: msg,
      type: "success",
      offset: 100
    })
  }
  Vue.prototype.notifyError = function(msg) {
    this.$notify.error({
      title: "错误",
      message: msg,
      offset: 100
    })
  }
}
