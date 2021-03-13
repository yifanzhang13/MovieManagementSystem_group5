<template>
  <div style="height: 100%;padding: 10px;">

    <!-- 查询开始-->
    <el-card class="filter-container" shadow="never">
      <header class="el-icon-search" style="margin-bottom: 20px;"><span class="scroll-line" style="margin-left: 5px;">筛选搜索</span></header>
      <el-row>
        <el-form :model="tableData" ref="searchForm" inline size="mini" class="search" label-width="100px">
          <el-form-item label="姓名">
            <el-input v-model="tableData.search.cnName" placeholder="请输入关键字"></el-input>
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

    <base-table ref="tbl1" :tbl="tableData" @tbl_edit_event="onTableEdit"></base-table>

    <el-dialog title="表单" :visible.sync="dialogFormVisible" width="40%" @close="resetForm('formData')">
      <el-form :model="formData" :rules="rules" ref="formData" label-width="100px">
        <el-form-item label="登录账号" prop="username">
          <el-input v-model="formData.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="formData.password" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPass">
          <el-input type="password" v-model="formData.checkPass" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="cnName">
          <el-input v-model="formData.cnName"></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="sex">
          <base-dict :defaultValue="formData.sex" dict-type="sex" facade="radio" @vue-select="onSexSelect"></base-dict>
        </el-form-item>
        <el-form-item label="手机" prop="mobile">
          <el-input v-model="formData.mobile"></el-input>
        </el-form-item>
        <el-form-item label="头像" prop="headPhoto">
          <base-uploader :imageUrl="formData.headPhoto" @vue-upload="onImgUpload"></base-uploader>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitForm('formData')">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="选择" :visible.sync="dialogOrgVisible" width="30%">
      <base-tree source="sys_org" showCheckbox single="on" @tree-check="onTreeCheck"></base-tree>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogOrgVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogOrgVisible = false">确 定</el-button>
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
        dataSelectorConf: {
          param: {
            url: '/sys/dict/list',
            type: 'discount_type'
          },
          columns: ['value'],// multiple 显示字段
        },
        tableData: {
          url: '/sys/user/all',
          search: {
          },
          cols: [
            {col: 'id', label: '用户ID', width: 30},
            {col: 'username', label: '登录账号'},
            {col: 'cnName', label: '姓名', width: 50},
            {col: 'sex', label: '性别', width: 20},
            {col: 'mobile', label: '手机', width: 70},
            // {col: 'orgName', label: '注册来源', width: 50},
            {col: 'roleId', label: '角色', width: 40, formatter: this.roleFmt},
          ],
          btn: {
            add: '', delete: '', update: '', detail: 'hide', width: 50,
			userDefined: [
              {type: 'success', icon: 'el-icon-key', text: '重置密码'},
            ],
          }
        },
        formData: {
          id: null,
          roleId: 1,
          username: '',
          password: '',
          checkPass: '',
          cnName: '',
          sex: '',
          mobile: '',
          email: '',
          orgName: '',
          ext1: null,
          ext2: null,
          orgId: 7,// 网站后台
          url: '/sys/user',
        },
        rules: {
          orgName: [
            {required: true, message: '请输入归属部门'},
          ],
          username: [
            {required: true, message: '请输入用户名'},
          ],
        },
        dialogFormVisible: false,
        dialogOrgVisible: false,
        operation: '',
        roleAll: [],
        queryRoleIds: []
      }
    },
    created() {
      this.roleInit()
    },
    methods: {
      onDataSelect(id, options) { // options是选项列表
        this.formData.ext1 = id
      },
      roleFmt(row, col, cellValue) {
        for (let i = 0; i < this.roleAll.length; i++) {
          if (this.roleAll[i].id == cellValue) { return this.roleAll[i].name }
        }
        return ''
      },
      async roleInit() {
        const res = await this.$findList({url: '/sys/role/list'})
        if (res.code == 0) {
          this.roleAll = res.data
          this.queryRoleIds = res.data.map(x => x.id) // 过滤条件字段
        }
      },
      async onTableEdit(action, idx, row) {
        this.operation = action
        if (action == 'add') {
          this.dialogFormVisible = true
        } else if (action == 'delete') {
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
          Object.assign(this.formData, row)
          this.formData.roleIds = row.roleIds
          this.formData.password = ''
          this.dialogFormVisible = true
        } else if (action === 'user_defined_重置密码') {
          Object.assign(this.formData, row)
          this.formData.newPassword = '111111'
          this.formData.checkPass = '111111'
          await this.$save(this.formData)
          this.$success('密码成功重置为111111')
        }
      },
      async removeConfirm(id) { // 删除
        const res = await this.$remove({url: this.formData.url, id})
        this.$msg(res, this.refresh)
      },
      submitForm(formName) {
        this.$refs[formName].validate(async(valid) => {
          if (valid) {
            const res = await this.$save(this.formData)
            this.$msg(res, this.refresh)
            this.dialogFormVisible = false
          } else {
            return this.$formInvalid()
          }
        })
      },
      resetForm(formName) {
        this.$nextTick(() => {
          this.$refs[formName].resetFields()
        })
      },
      refresh() {
        this.$refs.tbl1.load()
      },
      onTreeCheck({id, name}) {
        this.formData.orgId = id
        this.formData.orgName = name
      },
      onImgUpload(url) {
        this.formData.headPhoto = url
      },
      search() {
        this.tableData.search.roleIdsStr = this.queryRoleIds.join(",")
        this.refresh()
      },
      onSexSelect(value) {
        this.formData.sex = value
      },
    }
  }
</script>

<style lang="less">

</style>
