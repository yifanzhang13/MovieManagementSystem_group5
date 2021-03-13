// mixins.js or
// single import {BaseDict} from '@/dex'
// components: {BaseCaptcha}

import {save, removeById,remove, getList} from '@/api'
import dayjs from 'dayjs'

import BaseMenu from '@/components/BaseMenu'
import BaseLoading from '@/components/BaseLoading'
import BaseTable from '@/components/BaseTable'
import BaseTree from '@/components/BaseTree'
import BaseUploader from '@/components/BaseUploader'
import BaseDict from '@/components/BaseDict'
import BaseDataSelector from '@/components/BaseDataSelector'
import BaseSelector from '@/components/BaseSelector'
import BaseEChart from '@/components/BaseEChart'


export {
  BaseTable, BaseTree, BaseUploader,BaseEChart,BaseMenu, BaseDict,
  BaseDataSelector,BaseSelector,BaseLoading
}

export default {
  install(Vue, options) {
    Vue.prototype.$baseUrl = process.env.VUE_APP_BASE_API

    Vue.prototype.$dateFmt = (row, col, cellValue) => {
      const dateValue = cellValue || row
      return dayjs(dateValue).format('YYYY-MM-DD')
    }
    Vue.prototype.$datetimeFmt = (row, col, cellValue) => {
      const dateValue = cellValue || row
      return dayjs(dateValue).format('YYYY-MM-DD HH:mm:ss')
    }
    Vue.prototype.$utils = {
    }

    Vue.prototype.$msg = function(res, callback) {
      this.$message(res)
      callback && callback()
    }

    Vue.prototype.$success = function(message) {
      this.$message({
        message, type: 'success'
      })
    }

    Vue.prototype.$save = async(data) => {
      const res = await save(data)
      return res
    }
    Vue.prototype.$findList = async(data) => {
      const res = await getList(data)
      return res
    }
    Vue.prototype.$removeById = async(url, id) => {
      const res = await removeById(url, id)
      return res
    }
    Vue.prototype.$remove = async(data) => {
      const res = await remove(data)
      return res
    }

    Vue.prototype.$clone = obj => {
      return Object.assign({}, {}, obj)
    }

    Vue.prototype.$formInvalid = function() {
      this.$notify.error({
        title: '错误',
        message: '请检查输入是否正确',
        offset: 100
      })
      return false
    }
  }
}
