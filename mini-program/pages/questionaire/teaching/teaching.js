var _ = require('../../i18n.js')._;


Page({
    data:{
        radioItems:[
            { name: '是', value: '0'},
            { name: '否', value: '1'},
        ],
    },
    radioChange: function (e) {
        console.log('radio发生change事件，携带value值为：', e.detail.value);

        var radioItems = this.data.radioItems;
        for (var i = 0, len = radioItems.length; i < len; ++i) {
          radioItems[i].checked = radioItems[i].value == e.detail.value;
        }

        this.setData({
          radioItems: radioItems
        });
    },
    // checkboxChange: function (e) {
    //     console.log('checkbox发生change事件，携带value值为：', e.detail.value);

    //     var checkboxItems = this.data.checkboxItems, values = e.detail.value;
    //     for (var i = 0, lenI = checkboxItems.length; i < lenI; ++i) {
    //         checkboxItems[i].checked = false;

    //         for (var j = 0, lenJ = values.length; j < lenJ; ++j) {
    //             if(checkboxItems[i].value == values[j]){
    //                 checkboxItems[i].checked = true;
    //                 break;
    //             }
    //         }
    //     }

    //     this.setData({
    //         checkboxItems: checkboxItems
    //     });
    // }
});