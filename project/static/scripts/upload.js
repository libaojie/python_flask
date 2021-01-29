$(function () {

    $("#upload").click(function () {
        var formData = new FormData($('#uploadForm')[0]);
        // 点击上传
        $.ajax({
            url: '/upload_file',
            type: 'POST',
            data: formData,
            cache: false,//上传文件无需缓存
            processData: false,//用于对data参数进行序列化处理 这里必须false
            contentType: false, //必须
            success: function (response) {
                console.log(response)
                if (response.code == 0) {
                    alert('成功')
                }
                else {
                    alert('失败')
                }
            },
            error: function () {
                alert("异常！");
            }
        })
    })


})
