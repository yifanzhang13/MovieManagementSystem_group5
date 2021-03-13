import {mapActions, mapState} from 'vuex'
import * as DEX from '@/dex'
import dayjs from 'dayjs'

// 组件A应用了mixin，两者的属性如methods,components和directives，将被混合为同一个对象
// 如果methods,components和directives中有同名的属性，则mixin中的将会被忽略
// 同名钩子函数会组成数组并都会被调用，并且mixin的钩子函数会比组件的钩子函数先被调用
// 方法和参数在各组件中不共享
export const oscarMixin = {
  data() {
    return {
      key: 123,
      dayjs
    }
  },
  created() {
    this.initUserAction()
  },
  computed: {
    ...mapState(['userInfoState']),
  },
  components: DEX,
  methods: {
    ...mapActions(['initUserAction']),
  },
}
