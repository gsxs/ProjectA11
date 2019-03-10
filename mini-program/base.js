function success_callback(res) {}

function fail_callback(res) {}

function logger(res) {
  console.log(res.data);
}

function request(
    method, url, data,
    success = success_callback,
    fail = fail_callback,
    parse_json = true) {

    var status_code_checker = function (res) {
      if (res.statusCode == 200) {
        success(res);
      } else {
        fail(res);
      }
    }

    function _req() {
      wx.request({
        url: url,
        data: data,
        header: { 'Content-Type': 'application/json' },
        method: method,
        dataType: parse_json ? "json" : "binary",
        success: status_code_checker,
        fail: fail,
        complete: logger
      });
    }
  
  console.log(method + ' ' + url);
  url = 'http://localhost:8888/api/v1' + url;

  wx.getStorage({
    key: 'session_id',
    success: function(res) {
      if (res.data) {
        url = url + '?session_id=' + res.data;
      }
      _req();
    },
    fail: function(res) {
      _req();
    }
  });
}


module.exports = {
  request: request,
};
