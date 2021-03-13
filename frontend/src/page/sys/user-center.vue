<template>
  <div style="height: 100%">
    <header class="box-title">个人中心</header>

    <el-row :gutter="20">
      <el-col :span="8" :offset="6">
        <!--<el-header>个人中心</el-header>-->
        <el-form :model="formData" :rules="rules" ref="formData" label-width="100px">
          <el-form-item label="登录账号">
            {{formData.username}}
          </el-form-item>
          <el-form-item label="新密码">
            <el-input type="password" v-model="formData.newPassword" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="确认密码">
            <el-input type="password" v-model="formData.checkPass" auto-complete="off"></el-input>
          </el-form-item>
          <el-form-item label="用户名" prop="cnName">
            <el-input v-model="formData.cnName"></el-input>
          </el-form-item>
          <el-form-item label="性别" prop="sex">
            <base-dict :defaultValue="formData.sex" dict-type="sex" facade="radio" @vue-select="onSexSelect"></base-dict>
          </el-form-item>
          <el-form-item label="电子邮箱" prop="email">
            <el-input v-model="formData.email"></el-input>
          </el-form-item>
          <el-form-item label="手机" prop="mobile">
            <el-input v-model="formData.mobile"></el-input>
          </el-form-item>
          <el-form-item>
            <!--<el-button @click="dialogFormVisible = false">取 消</el-button>-->
            <el-button type="primary" @click="submitForm('formData')">确 定</el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import {oscarMixin} from '@/config/mixins'
  import {Storage} from '@/common/tool'

  export default {
    mixins: [oscarMixin],
    data() {
      return {
        formData: {
          id: null,
          roleIds: [],
          username: '',
          password: '',
          newPassword: '',
          checkPass: '',
          cnName: '',
          sex: '',
          mobile: '',
          phone: '',
          email: '',
          orgName: '',
          url: '/sys/user'
        },
        rules: {

        },
        dialogOrgVisible: false,
        operation: '',
      }
    },
    created() {
      Object.assign(this.formData, this.$store.state.userInfoState)
      this.formData.password = ''
      this.formData.newPassword = ''
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate(async(valid) => {
          if (valid) {
            if (this.formData.newPassword !== '' && this.formData.checkPass !== this.formData.newPassword) {
              this.$msg({
                type: 'error',
                message: '两次输入的密码不一致'
              })
              return
            }
            const res = await this.$save(this.formData)
            this.$msg(res)
            Storage.set("user_info", res.data)
            this.$store.commit('userMutation', res.data)
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
      onImgUpload(url) {
        this.formData.imgUrl = url
      },

      onSexSelect(val) {
        this.formData.sex = val
      }
    }
  }
</script>

<style lang="less">

</style>

