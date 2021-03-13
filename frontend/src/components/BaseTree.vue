<template>
  <div>
    <el-cascader v-if="facade=='cascader'"
                 :options="data"
                 :props="defaultProps"
                 v-model="modelValue"
                 :show-all-levels="false"
                 @change="handleNodeClick"></el-cascader>

    <el-tree v-else
             :data="data"
             :show-checkbox="showCheckbox"
             node-key="id"
             ref="tree"
             @check="handleCheck"
             @node-click="handleNodeClick"
             highlight-current :props="defaultProps">
    </el-tree>
  </div>
</template>

<script>
  export default {
    name: "BaseTree",
    // TODO 改成{}
    props: ['source', 'facade', 'keys', 'single','showCheckbox', 'activeValue'],// activeValue默认值
    data() {
      return {
        data: [],
        defaultProps: {
          children: 'children',
          label: 'name',
          value: 'id'
        },
      }
    },
    watch: {
      keys: {
        handler(newValue,oldValue) {
          this.$refs.tree.setCheckedKeys(newValue,true)
        },
        deep: true
      }
    },
    computed: {
      modelValue: { // 重新赋值，避免子组件修改activeValue
        get() {
          return [this.activeValue]
        },
        set() {

        }
      }
    },
    created() {
      this.load()
    },
    methods: {
      async load() {
        const res = await this.$findList({url: '/sys/tree', t: this.source})
        if (res.code == 0) {
          this.data = res.data
          if (this.keys) { this.$refs.tree.setCheckedKeys(this.keys,true) }
        }
      },
      handleCheck(data) { // checkbox choosed
        if (!this.single) {
          this.$emit('tree-check', this.$refs.tree.getCheckedKeys(true))
        } else {
          this.$refs.tree.setCheckedNodes([])
          this.$refs.tree.setCheckedNodes([data])
          this.$emit('tree-check', data)
        }
      },
      handleNodeClick(option) {
        this.$emit('tree-node-click', option, this.data)
      }
    }
  }
</script>

<style scoped>

</style>
