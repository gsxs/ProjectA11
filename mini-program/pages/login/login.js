var base = require('../../base.js');
const request = base.request;

Page({
  data: {
    account_types: ["学生", "教师"],
    account_types_name: ["学号", "教职工号"],
    account_type_index: 0,
    username: null,
    password: null,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    if(app.appData.userInfo == null ){
      wx.redirectTo("../register/register");
    }
    else {
      this.setDate({username:app.appData.username})
    }
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },

  loginBtnClick: function () {
    wx.request({
      url: 'http://127.0.0.1:8888/api/v1/credential/account',
      data: {
        "user_id": 12345678,
        "password": "p@ssword"
      },
      method: 'POST',
      header: {
        'content-type': 'application/json' // 默认值
      },
      success(res) {
        console.log(res.data)
      }
    })
  },

  registerBtnClick:function() {
    
  },

  bind_account_type_change: function (e) {
    this.setData({
      account_type_index: e.detail.value
    });
  },

  do_login: function (e) {
    request(
      'PUT', '/credential/account',
      {
        user_id: 123456,
        password: "p@ssword"
      },
    );
  }
});
