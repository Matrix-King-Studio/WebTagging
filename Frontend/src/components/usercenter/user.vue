<template>
  <div>
    <div class="userInformation">
      <ul>
        <li><i class="el-icon-user">&nbsp;用户名：</i>{{ userInfo.username }}</li>
        <li><i class="el-icon-message">&nbsp;邮箱：</i>{{ userInfo.email }}</li>
        <li><i class="el-icon-date">&nbsp;注册日期：</i>{{ userInfo.date_joined|timefilters }}</li>
      </ul>
    </div>
    <div class="logout"  @click="logout">
      <span>退出登录</span>
    </div>
    <div>
      <!-- 修改密码的按钮 -->
      <el-button id="BtnChangePwd" type="text" @click="dialogFormVisible = true" >修改密码</el-button>
      <!-- 填写修改密码信息的表单 -->
      <el-dialog title="修改密码" :visible.sync="dialogFormVisible" :close-on-click-modal="false">
        <!--三个表单内容-->
        <el-form :model="changePwdForm" status-icon :rules="rules" ref="changePwdForm" label-width="100px" class="demo-changePwdForm">
          <el-form-item label="原密码" prop="old_password">
            <el-input type="password" v-model="changePwdForm.old_password" autocomplete="off" placeholder="请输入原密码" show-password></el-input>
          </el-form-item>
          <el-form-item label="新密码" prop="new_password1">
            <el-input type="password" v-model="changePwdForm.new_password1" autocomplete="off" placeholder="请输入新密码" show-password></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="new_password2">
            <el-input type="password" v-model="changePwdForm.new_password2" autocomplete="off" placeholder="请再次输入新密码" show-password></el-input>
          </el-form-item>
          <!--取消和确定按钮-->
          <el-form-item>
            <el-button @click="dialogFormVisible = false,resetForm('changePwdForm')">取 消</el-button>
            <el-button type="primary" @click="dialogFormVisible = false,submitForm('changePwdForm')">确 定</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
    </div>
  </div>
</template>

<script>
export default {
  filters: {
    //UTC时间格式转换为北京时间
    timefilters(val) {
      if (val == null || val == "") {
        return "加载中";
      } else {
        let d = new Date(val);   //val 为表格内取到的后台时间
        let month =
            d.getMonth() + 1 < 10 ? "0" + (d.getMonth() + 1) : d.getMonth() + 1;
        let day = d.getDate() < 10 ? "0" + d.getDate() : d.getDate();
        let hours = d.getHours() < 10 ? "0" + d.getHours() : d.getHours();
        let min = d.getMinutes() < 10 ? "0" + d.getMinutes() : d.getMinutes();
        let sec = d.getSeconds() < 10 ? "0" + d.getSeconds() : d.getSeconds();
        let times=d.getFullYear() + '-' + month + '-' + day + ' ' + hours + ':' + min + ':' + sec;
        return times;
      }
    }
  },
  data(){
    //原密码不为空检测
    let validateOldPass = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('原密码不能为空'));
      }else{
        callback();
      }
    };
    //新密码与确认密码检测
    let validateNewPass1 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      } else {
        if (this.changePwdForm.new_password2 !== '') {
          this.$refs.changePwdForm.validateField('new_password2');
        }
        callback();
      }
    };
    //新密码与确认密码检测
    let validateNewPass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== this.changePwdForm.new_password1) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    return{
      //用户信息
      userInfo:{},
      //dialog的激活状态
      dialogFormVisible: false,
      //修改密码的表单信息
      changePwdForm: {
        old_password: '',
        new_password1: '',
        new_password2: '',
      },
      //验证规则
      rules: {
        old_password: [
          { validator: validateOldPass, trigger: 'blur' }
        ],
        new_password1: [
          { validator: validateNewPass1, trigger: 'blur' }
        ],
        new_password2: [
          { validator: validateNewPass2, trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.getUserInfo()
  },
  methods: {
    //获取用户信息
    getUserInfo(){
      this.$http.get('v1/users/self').then((res)=>{
        this.userInfo = res.data;
        console.log(this.userInfo);
      })
    },
    //退出登录
    logout(){
      this.$http.post('v1/auth/logout').then((e)=>{
        console.log(e);
        window.sessionStorage.removeItem('token')
        this.$message({
          message:"退出登录成功",
          type: "success"
        })
        this.$router.push('/login')
      })
    },
    //修改密码表单提交
    submitForm(formName) {
      console.log(this.changePwdForm)
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // alert('提交成功');
          this.$http.post('v1/auth/password/change', {old_password: this.changePwdForm.old_password,
            new_password1: this.changePwdForm.new_password1,new_password2: this.changePwdForm.new_password2}).then(e => {
            console.log(e)
            this.$message({
              message: '修改密码失败! ' + e.data.error,
              type: "error"
            })
          }).catch((e)=>{
            console.log(e);
            this.$message({
              message: e,
              type: "error"
            })
          })
        } else {
            console.log('修改密码提交失败');
            this.$message({
              message: "修改密码提交失败！请按照提示规则填写！",
              type: "error"
            })
            return false;
        }
      });
    },
    //重置表单
    resetForm(formName) {
      this.$refs[formName].resetFields();
    }
  },
}
</script>

<style lang="less" scoped>
.userInformation{
  width: 400px;
  border-radius: 8px;
  background-color: #ffffff;
  li{
    padding: 10px;
    list-style:none;
  }
}

.logout {
  height: 40px;
  width: 100px;
  margin-top: 50px;
  border-radius: 5px;
  background-color: #e8fff0;
  text-align: center;
  line-height: 40px;
  cursor: pointer;
}
  .logout:hover{
    background-color: #c0ffd9;
  }

#BtnChangePwd{
  height: 40px;
  width: 100px;
  margin-top: 50px;
  border-radius: 5px;
  background-color: #e8fff0;
  text-align: center;
  size: landscape;
  color: #000000;
  font-size: medium;
  cursor: pointer;
}
#BtnChangePwd:hover{
   background-color: #c0ffd9;
 }


</style>
