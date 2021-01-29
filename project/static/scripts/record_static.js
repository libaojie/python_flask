$(function () {


    $.ajax({
        url: '/upload_list',
        type: 'POST',
        data: {page: 2},
        success: function (result) {
            if (result.code == 0) {
                // 成功
                if (result.data.length > 0) {

                }

            }
            else {
                alert(result.msg)
            }
        },
        error: function () {
            alert("系统级异常！");
        }
    })
})