<template>
  <div style="height: 100%;">

    <div class="login_page fillcontain login_page_bg">

      <transition name="form-fade" mode="in-out">
        <section class="form_container">
          <div class="manage_tip">
            <p>moviestar</p>
          </div>

          <el-form :model="loginForm" :rules="rules" ref="loginForm">
            <el-form-item prop="username">
              <el-input prefix-icon="el-icon-user-solid" v-model="loginForm.username" placeholder=""></el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input prefix-icon="el-icon-lock" type="password" placeholder="" v-model="loginForm.password"></el-input>
            </el-form-item>
            <el-form-item>
            </el-form-item>
            <el-form-item>
              <el-row>
                <el-button icon="el-icon-s-platform" type="success" @click="submitForm('loginForm')" class="submit_btn">Login</el-button>
                <el-button icon="el-icon-circle-plus-outline" type="primary" @click="toRegister" class="register_btn">Register</el-button>
              </el-row>
            </el-form-item>
          </el-form>
          <p class="tip"></p>
        </section>
      </transition>
    </div>
  </div>
</template>

<script>
  import {login} from '@/api'
  import {mapActions, mapState} from 'vuex'
  import {Storage, backendVersion} from '@/common/tool'

  export default {
    components: {},
    data() {
      return {
        loginForm: {
          username: '',
          password: '',
        },
        rules: {
          username: [
            {required: true, message: 'Username can not empty', trigger: 'blur'},
          ],
          password: [
            {required: true, message: 'Password can not empty', trigger: 'blur'}
          ],
        },
      }
    },
    mounted() {
    },
    created() {
      backendVersion()
      this.onEnterDown()
      this.initSysDescAction()
    },
    computed: {
      ...mapState(['sysDescState']), // mapState通过扩展运算符将store.state.sysDescState 映射到vue对象上
    },
    methods: {
      ...mapActions(['initSysDescAction']),
      onEnterDown() {
        const that = this
        document.onkeydown = function(e) {
          if (e.keyCode == 13) {
            that.submitForm('loginForm')
          }
        }
      },
      toRegister() {
        this.$router.push('/register')
      },
      async submitForm(formName) {
        this.$refs[formName].validate(async(valid) => {
          if (valid) {
            // const res = await login(this.loginForm)
            const res = {
              "code": 0,
              "type": "success",
              "message": "Success",
              "data": {
                "user": {
                  "id": 100001,
                  "cnName": "admin",
                  "username": "1",
                  "sex": "Man",
                  "age": 27,
                  "roleIds": [1],
                  "roleId": 1,
                  "roleName": "Admin"
                }, "token": {"token": "hqpPnnbU4Mc=", "timeout": 30}
              }
            }
            this.$msg(res, () => {
              Storage.setToken(res.data.token)
              Storage.set("user_info", res.data.user)
              this.$store.commit('userMutation', res.data.user)
              this.$router.push('tb_movie')
            })
          } else {
            return this.$formInvalid()
          }
        });
      },
    },
  }
</script>

<style lang="less" scoped>
  .login_page {
    font-family: 'Open Sans', sans-serif;
    background-size: cover;
  }

  .login_page_bg {
    /*background-color: #3b5963;*/
    background: url(/static/img/bg.jpg) no-repeat 0px 0px;
    background-size: 100% 100%;
  }

  .manage_tip {
    position: absolute;
    width: 100%;
    top: -100px;
    left: 0;

    p {
      font-size: 40px;
      color: #009688;
      font-weight: 500;
      text-shadow: 0 6px 9px #2196F3, 0px -2px 1px #fff;
      letter-spacing: 4px;
      text-align: center;
      position: absolute;
      padding: 100px 200px;
      left: 48%;
      transform: translate(-50%, -50%);
      width: 360px;
    }
  }

  .form_container {
    .wh(320px, 219px);
    .ctp(320px, 210px);
    padding: 25px;
    border-radius: 5px;
    text-align: center;
    left: 47%;
    /*background-color: #fff;*/
    /*box-shadow: 0 0 10px #3FBEEB;*/
    border: 1px solid #74B5C9;

    .submit_btn {
      width: 152px;
      box-shadow: 0 0 8px #67C23A;
    }

    .register_btn {
      width: 152px;
      box-shadow: 0 0 8px #3FBEEB;
    }
  }

  .tip {
    font-size: 12px;
    color: red;
  }

  .form-fade-enter-active, .form-fade-leave-active {
    transition: all 1s;
  }

  .form-fade-enter, .form-fade-leave-active {
    transform: translate3d(0, -50px, 0);
    opacity: 0;
  }
</style>
