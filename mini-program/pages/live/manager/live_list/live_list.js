// pages/live/manager/live_list/live_list.js
var u = getApp().utils;


Page({

  /**
   * 页面的初始数据
   */
  data: {
    live_class: {
      name: '小圆课堂',
      start: "2019-01-01",
      end: "2019-10-10"
    },
  },

  create_class: function() {
    wx.navigateTo({
      url: '../live_create/live_create',
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var role = wx.getStorageSync('role');
    this.setData({ role: role });
    this.refresh();
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

  }
})