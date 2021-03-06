var u = getApp().utils;
var _ = require('../../i18n.js')._;


Page({
  data: {
    course_id: "",
    class_name: "",
    weekday: "周一",
    start: 0,
    end: 0,
    weekdays: ["周一","周二","周三","周四","周五","周六","周末"],
    class_time_picker: [1,2,3,4,5,6,7,8,9,10],
    index: 0,
  },

  // 课程名
  set_course_name: function(e) {
    this.setData({
      class_name: e.detail.value
    })
  },

  // 星期
  bind_Weekday_Picker_Change: function(e) {
    var date = e.detail.value;
    switch (date) {
      case "0":
        this.setData({
          weekday: 1
        });
        break;
      case "1":
        this.setData({
          weekday: 2
        });
        break;
      case "2":
        this.setData({
          weekday: 3
        });
        break;
      case "3":
        this.setData({
          weekday: 4
        });
        break;
      case "4":
        this.setData({
          weekday: 5
        });
        break;
      case "5":
        this.setData({
          weekday: 6
        });
        break;
      case "6":
        this.setData({
          weekday: 7
        });
        break;
    }
  },

  // 开始时间
  bindDateStartChange: function(e) {
    this.setData({
      start: parseInt(e.detail.value) + 1
    })
  },

  // 结束时间
    bindDateEndChange: function (e) {
    this.setData({
      end: parseInt(e.detail.value) + 1
    })
  },

  // 创建课程
  do_create: function() {
    u.request(
      'PUT', '/class',
      {
        class_name: this.data.class_name,
        weekday: this.data.weekday,
        start: this.data.start,
        end: this.data.end,
        teacher_id: wx.getStorageSync('user_id'),
        course_id: this.data.course_id,
      },
      (res) => {
        wx.showToast({
          title: _('success'),
          duration: 1000
        });
        setTimeout(() => {
          wx.navigateBack();
        }, 1000);
      }
    )
  },

  onLoad: function (options) {
    this.setData({ langIndex: wx.getStorageSync('langIndex') });
    var course_id = options.course_id;
    this.setData({ course_id: course_id });
  },

  clear_information: function () {
    this.setData({

    });
  },

  // 下拉更新
  onPullDownRefresh: function () {
    console.log('onPullDownRefresh')
    wx.showNavigationBarLoading();
    this.clear_information();

    console.log(this.data.staff_id);
    wx.hideNavigationBarLoading();
    wx.stopPullDownRefresh();
  }
})