// pages/class/classes-control/classes-control.js
var u = getApp().utils;


Page({
  data: {
    apps: [
      {
        title: '课程创建',
        url: '../course-create/course-create',
        image: '../../../images/icons/classes-create.png'
      },
      {
        title: '课程列表',
        url: '../courses-list/courses-list',
      },
    ]
  },
})