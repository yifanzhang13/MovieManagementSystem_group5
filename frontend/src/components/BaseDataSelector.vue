<template>
  <div>
    <el-select v-model="val" @change="selectActivity" placeholder="请选择" :disabled="disabled">
      <el-option
        v-for="item in options"
        :key="item.id"
        :label="item[labelColumn]"
        :value="item.id">
        <span v-for="columnName in config.columns" :key="columnName">
          {{ item[columnName] }}
        </span>
      </el-option>
    </el-select>
  </div>
</template>

<script>
  import {getList} from '@/api'

  export default {
    name: 'BaseDataSelector',
    // TODO refact props
    props: ['value','conf','disabled'],
    data() {
      return {
        options: [],
        // 需要重新赋值，避免父组件值改变，子组件值无法render的问题  //https://www.jianshu.com/p/392145843afe
        config: this.conf,
        val: this.value,
        labelColumn: '' // option的label用哪个字段
      }
    },
    watch: {
      'value': function(newValue) {
        this.val = newValue
      }
    },
    methods: {
      selectActivity(val) {
        let selectOption = null
        this.options.forEach(x => {
          if (x.id == val) selectOption = x
        })
        this.$emit('vue-data-select', val, selectOption, this.options)
      },
      async init(param) { // for reload
        this.labelColumn = this.config.columns[0]
        const res = await getList(param || this.config.param)
        if (res.code == 0) { this.options = res.data }
      },
      reset() {
        this.options = []
      }
    },
    created() {
      this.init()
    },
  }
</script>

<style scoped>

</style>
