<template>
  <div style="height: 100%;padding: 10px;">

    <!-- 查询开始-->
    <el-card class="filter-container" shadow="never">
      <header class="el-icon-search" style="margin-bottom: 20px;"><span class="scroll-line" style="margin-left: 5px;">筛选搜索</span></header>
      <el-row>
        <el-form :model="tableData" ref="searchForm" inline size="mini" class="search" label-width="100px">
          <el-form-item label="菜单名称">
            <el-input v-model="tableData.search.name" placeholder="请输入关键字"></el-input>
          </el-form-item>

          <el-form-item label="">
            <el-button size="mini" type="primary" icon="el-icon-search" @click="search()">查 询</el-button>
            <el-button v-if="tableData.btn.add !='hide'" size="mini" type="success"
                       @click="onTableEdit('add')" icon="el-icon-circle-plus-outline">添 加
            </el-button>
          </el-form-item>
        </el-form>
      </el-row>
    </el-card>
    <!-- 查询结束-->

    <el-card class="operate-container" shadow="never" style="margin-top: 15px;">
      <i class="el-icon-tickets"></i>
      <span class="scroll-line">数据列表</span>
    </el-card>

    <base-table ref="tbl1" :tbl="tableData" @tbl_edit_event="onTableEdit"/>

    <!-- item的prop一定要写 -->
    <el-dialog title="菜单表单" :visible.sync="dialogFormVisible" width="40%" @close="resetForm('formData')">
      <el-form :model="formData" :rules="rules" ref="formData" label-width="100px">

        <el-form-item label="菜单编号" prop="id">
          <el-input v-model="formData.id" style="width:220px;"></el-input>
        </el-form-item>
        <el-form-item label="菜单名称" prop="name">
          <el-input v-model="formData.name" style="width:220px;"></el-input>
        </el-form-item>
        <el-form-item label="路由" prop="href">
          <el-input v-model="formData.href" style="width:220px;"></el-input>
        </el-form-item>
        <el-form-item label="图标" prop="icon">
          <el-input v-model="formData.icon" style="width:220px;"></el-input>
        </el-form-item>
        <el-form-item label="是否有效" prop="switcher">
          <el-switch v-model="formData.switcher"></el-switch>
        </el-form-item>

      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">关闭</el-button>
        <el-button type="primary" @click="submitForm('formData')">提交</el-button>
      </div>

    </el-dialog>

  </div>
</template>

<script>
  import {oscarMixin} from '@/config/mixins'

  export default {
    mixins: [oscarMixin],
    data() {
      return {
        tableData: {
          url: '/sys/menu/page',
          search: {
            name: null
          },
          cols: [
            {col: 'id', label: '菜单编号', width: 40},
            {col: 'href', label: '路由', width: 50},
            {col: 'icon', label: '图标', width: 50},
          ],
          imgCols: [],
          icons: [
            {col: 'icon', label: '菜单'},
          ],
          tagCols: [
            {col: 'enabled', label: '状态', width: 18},
          ],
          btn: {
            width: 30,
            add: '', delete: '', update: '', detail: 'hide',width: 100,
            userDefined: [
              {type: 'success', icon: 'el-icon-circle-plus-outline', text: '添加下级菜单'}
            ]
          }
        },
        formData: {
          url: '/sys/menu',
          id: null,
          parentId: 0,
          name: null,
          sort: null,
          href: null,
          component: null,
          target: null,
          icon: 'el-icon-document',
          switcher: true,
          enabled: null,
        },
        rules: {
          id: [{required: true, message: '请填写编号'}],
          name: [{required: true, message: '请填写名称'}],
          icon: [{required: true, message: '请填写图标'}],
        },
        dialogFormVisible: false,
        operation: '',
        userInfo: {},
      }
    },
    computed: {},
    created() {
      this.userInfo = this.$store.state.userInfoState
      // this.formData.userId = this.userInfo.id
    },
    methods: {
      async onTableEdit(action, idx, row, col_title) { // 表格操作
        this.operation = action
        if (action == 'add') {
          this.dialogFormVisible = true
        } else if (action == 'detail') {
          this.$router.push({
            path: '/sys_menu_detail',
            query: row
          })
        } else if (action == 'delete') {
          this.formData.url = "/sys/menu"
          this.$confirm('确定删除数据吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.removeConfirm(row.id)
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '取消删除操作！'
            })
          })
        } else if (action == 'edit') {
          this.dialogFormVisible = true
          Object.assign(this.formData, row)
          this.$refs.img_ref && this.$refs.img_ref.preview(this.formData.imgUrl)
          this.$refs.video_ref && this.$refs.video_ref.preview(this.formData.videoUrl)
          this.formData.url = "/sys/menu"
        } else if (action == 'user_defined_添加下级菜单') {
          this.dialogFormVisible = true
          this.formData.parentId = row.id
          const res = await this.$findList({url: '/sys/menu/children', parentId: row.id})
          if (res.code == 0) {
            if (res.data.length > 0) { // 该节点下存在children
              this.formData.id = res.data[res.data.length - 1].id + 1
            } else {
              this.formData.id = row.id * 10
            }
          }

          this.formData.url = "/sys/menu/insert"
        } else if (action == 'btn_col') {
          console.log(col_title)
        }
      },
      submitForm(formName) { // 提交Form表单
        this.$refs[formName].validate(async(valid) => {
          if (valid) {
            this.formData.enabled = this.formData.switcher ? "on" : "off"
            const res = await this.$save(this.formData)
            this.$msg(res, this.refresh)
            this.dialogFormVisible = false
            // this.$router.push('/user/center')
          } else {
            return this.$formInvalid()
          }
        })
      },
      async removeConfirm(id) { // 删除
        const res = await this.$remove({url: this.formData.url, id})
        this.$msg(res, this.refresh)
      },
      resetForm(formName) {
        this.$nextTick(() => {
          this.$refs[formName].resetFields()
        })
      },
      refresh() {
        this.$refs.tbl1.load()
      },
      search() {
        this.refresh()
      },

    }
  }
</script>

<style lang="less">

</style>
