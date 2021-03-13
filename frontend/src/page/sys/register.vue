<template>
  <el-container>
    <el-header></el-header>
    <el-main>
      <el-row :gutter="20">
        <el-col :span="12" :offset="6">
          <el-header>注册新用户</el-header>
          <el-form ref="form" :rules="rules" :model="formData" label-width="80px">
            <el-form-item label="账号" prop="username">
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
            <el-form-item label="手机" prop="mobile">
              <el-input v-model="formData.mobile"></el-input>
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="formData.email"></el-input>
            </el-form-item>
            <el-form-item label="头像" prop="headPhoto">
              <base-uploader :imageUrl="formData.headPhoto" @vue-upload="onImgUpload"></base-uploader>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit">立即注册</el-button>
              <el-button @click="onBack">取消</el-button>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
    </el-main>
  </el-container>

</template>

<script>
  import {oscarMixin} from '@/config/mixins'

  export default {
    mixins: [oscarMixin],
    data() {
      return {
        formData: {
          username: '',
          password: '',
          checkPass: '',
          cnName: '',
          mobile: '',
          phone: '',
          email: '',
          orgId: '7',
          roleId: 1,
          url: '/sys/user'
        },
        rules: {
          username: [
            {required: true, message: '账号不能为空'},
          ],
          password: [
            {required: true, message: '密码不能为空'},
          ],
          checkPass: [
            {required: true, message: '密码不能为空'},
          ],
          cnName: [
            {required: true, message: '姓名不能为空'},
          ],
          mobile: [
            {required: true, message: '手机不能为空'},
          ],
        },
      }
    },
    created() {
      this.redirectUrl = this.$route.query.redirectUrl || '/' // 注册成功后跳转地址
    },
    methods: {
      onBack() {
        this.$router.push(this.redirectUrl)
      },
      onSubmit() {
        this.$refs['form'].validate(async(valid) => {
          if (valid) {
            if (this.formData.password != this.formData.checkPass) {
              this.$msg({
                code: 1,type: 'warning',message: '两次输入的不一致'
              })
              return
            }

            let res = await this.$findList({url: '/sys/user/list',cnName: this.formData.cnName})
            if (res.code == 0 && res.data.length > 0) {
              this.$msg({
                code: 1,type: 'warning',message: '姓名已经存在，请更换其他'
              })
              return
            }

            res = await this.$save(this.formData)
            this.$msg(res)
            this.$router.push(this.redirectUrl)
          } else {
            return this.$formInvalid()
          }
        })
      },
      onImgUpload(url) {
        this.formData.headPhoto = url
      }
    }
  }
</script>

<style scoped>

</style>
