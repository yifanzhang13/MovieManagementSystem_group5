<template>
  <div>
    <el-form-item :label="item.title" v-for="item in data" :key="item.field">
      <el-button size="small" @click="handleAll(item.field)">全部</el-button>
      <el-button size="small" v-for="option in item.options" :key="option.name" @click="handleSelect(item.field, option.name)">
        {{option.name}}
        <span v-if="option.value" class="inner-badge" :style="option.style">{{option.value}}</span>
      </el-button>
    </el-form-item>

    <el-form-item label="过滤条件" v-if="tags.length > 0 " >
      <el-tag v-for="tag in tags" :key="tag" closable size="medium" @close="handleClose(tag)">
        {{tag}}
      </el-tag>
    </el-form-item>

  </div>
</template>

<script>
  export default {
    name: "BaseSelector",
    props: {
      data: {
        type: Array,
        required: true
      }
    },
    data() {
      return {
        tags: [],
        fields: [], // 查询条件字段
      }
    },
    methods: {
      handleAll(field) { // 选择全部，清除对应的条件
        const v_tags = [],v_fields = []
        for (let i = 0; i < this.fields.length; i++) {
          if (this.fields[i] !== field) {
            v_fields.push(this.fields[i])
            v_tags.push(this.tags[i])
          }
        }
        this.tags = v_tags
        this.fields = v_fields
      },
      handleSelect(field, tag) {
        this.tags.push(tag)
        this.fields.push(field)
      },
      handleClose(tag) {
        const idx = this.tags.indexOf(tag)
        this.tags.splice(idx, 1)
        this.fields.splice(idx, 1)
      },
      getChoose() {
        return [this.fields, this.tags]
      }
    }
  }
</script>

<style lang="less" scoped>
  .el-tag + .el-tag {
    margin-left: 10px;
  }

  .inner-badge {
    background-color: #eee;
    padding: 1px 3px;
    margin-left: 10px;
    border-radius: 2px;
  }
</style>
