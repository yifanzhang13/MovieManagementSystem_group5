<template>
  <div>

    <el-checkbox-group v-model="value" v-if="facade == 'checkbox'">
      <el-checkbox
          v-for="item in options"
          :label="item.value"
          :key="item.value"
          @change="onCheck">{{item.label}}
      </el-checkbox>
    </el-checkbox-group>

    <el-radio-group v-model="value" size="small" v-else-if="facade == 'radio'">
      <el-radio
          border
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
          @change="selectActivity"></el-radio>
    </el-radio-group>

    <el-select v-model="value" v-else @change="selectActivity">
      <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"></el-option>
    </el-select>
  </div>
</template>

<script>

  export default {
    name: 'BaseDict',
    props: {
      dictType: {
        type: String,
        required: true,
        // validator(value) {}
      },
      facade: {
        type: String,
        default: 'selector'
      },
      defaultValue: {
        type: String,
      }
    },
    data() {
      return {
        options: [],
        // 需要重新赋值，避免父组件值改变，子组件值无法render的问题
        value: this.defaultValue, // https://www.jianshu.com/p/392145843afe
      }
    },
    watch: {
      defaultValue(newValue, oldValue) {
        this.value = newValue
      }
    },
    methods: {
      onCheck() {
        this.selectActivity(this.value)
      },
      selectActivity(val) {
        this.$emit('vue-select', val)
      },
      async load() {
        const _data = await this.$findList({url: '/sys/dict/list', type: this.dictType})
        if (_data.code === 0) {
          this.options = _data.data.filter(x => x.value !== '')
        }
      }
    },
    created() {
      this.load()
    }
  }
</script>

<style scoped>

</style>
