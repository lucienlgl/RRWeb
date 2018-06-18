function bindEmail() {

    $("div.email-info").show();
    $("div.password-info").hide();
    $("div.phone-info").hide();
    $("div.account-info").hide();

}

function modifyPassword() {
    $("div.email-info").hide();
    $("div.password-info").show();
    $("div.phone-info").hide();
    $("div.account-info").hide();
}

function modifyPhone() {
    $("div.email-info").hide();
    $("div.password-info").hide();
    $("div.phone-info").show();
    $("div.account-info").hide();
}

function backAccount() {
    $("div.email-info").hide();
    $("div.password-info").hide();
    $("div.phone-info").hide();
    $("div.account-info").show();

    $.get("/api/user/basic", function (data) {
        var data_json = $.parseJSON(JSON.stringify(data));
        if(data_json.code == 0){
            alert(data_json.msg);
        }else{
            if(data_json.data.email != null ){
                $("#userEmail").html(data_json.data.email);
            }
            if(data_json.data.phone != null ) {
                $("#userPhone").html(data_json.data.phone);
            }
        }
    });

}
//发送验证码按钮，倒计时实现
    function sendCode(thisBtn) {
        var clock = '';
        var nums = 60;
        var btn;
        btn = thisBtn;
        btn.disabled = true; //将按钮置为不可点击
        btn.value = nums + 's';
        clock = setInterval(doLoop, 1000); //一秒执行一次
        function doLoop() {
        nums--;
        if (nums > 0) {
            btn.value = nums + 's';
        } else {
            clearInterval(clock); //清除js定时器
            btn.disabled = false;
            btn.value = 'Get Code';
            nums = 60; //重置时间
        }
    }
    }



jQuery(document).ready(function () {


    $(".backToTop").goToTop();
    $(window).bind('scroll resize', function () {
        $(".backToTop").goToTop();
    });

    islogin()

    function islogin() {
        var name = $.cookie('username');
        if (name != null) {
            $("#id_login_register").hide();
            $("#id_userprofile").show();
            $("#id_username").text(name);

        }
    }

    init();

    function init() {
        $.get("/api/user/basic", function (data) {
            var data_json = $.parseJSON(JSON.stringify(data));
            if (data_json.code == 0) {
                alert(data_json.msg);
                if(data_json.msg=="请重新登录"){
                    window.location.href='/login';
                }
            } else {
                $("#userNickname").val(data_json.data.name);
                if (data_json.data.sex == '1') {
                    $("input[id='man']").attr('checked', 'true');
                } else if (data_json.data.sex == '0') {
                    $("input[id='woman']").attr('checked', 'true');
                } else {
                }
                $("#userCityname").val(data_json.data.location);
                $("#userRemark").val(data_json.data.remark);

            }
        });
    }

    $("#basic_submit").click(function () {
        var userNickname = $("#userNickname").val();
        var userSex = $("input[name='userSex']:checked").val();
        var userCityname = $("#userCityname").val();
        var userRemark = $("#userRemark").val();

        $.post("/api/user/basic", {
                name: userNickname,
                sex: userSex,
                location: userCityname,
                remark: userRemark,
                'csrfmiddlewaretoken': $.cookie('csrftoken'),
            },
            function (data) {
                var data_json = $.parseJSON(JSON.stringify(data));
                alert(data_json.msg);

            });
    });
    
    //通过post修改绑定邮箱
    $("#email-submit").click(function () {
        var email = $("#email").val();
        $.post("/api/user/email", {
                email:email,
                'csrfmiddlewaretoken': $.cookie('csrftoken')
            },
            function (data) {
                var data_json = $.parseJSON(JSON.stringify(data));
                alert(data_json.msg);
                if(data_json.msg=="请重新登录"){
                    window.location.href='/login';
                }
                if(data_json.code == 1){
                    window.location.href='/'
                }
            });
    });

    $("#btn-code").click(function () {
        var phone = $("#newPhone").val();
        $.post("/api/user/phone/code", {
                phone:phone,
                'csrfmiddlewaretoken': $.cookie('csrftoken')
            },function (data) {
                var data_json = $.parseJSON(JSON.stringify(data));
                if(data_json.code == 0){
                    alert(data_json.msg);

                }
                else if(data_json.code == 1){
                    sendCode(document.getElementById("btn-code"));
                }
            });

    });

    $("#phone-submit").click(function () {
        var phone = $("#newPhone").val();
        var code = $("#code").val();
        $.post("/api/user/phone", {
                phone:phone,
                code:code,
                'csrfmiddlewaretoken': $.cookie('csrftoken')
            },function (data) {
                var data_json = $.parseJSON(JSON.stringify(data));
                if(data_json.code == 0){
                    alert(data_json.msg);
                    if(data_json.msg=="请重新登录"){
                    window.location.href='/login';
                }
                }
                else if(data_json.code == 1){
                    alert(data_json.msg);
                    window.location.href='/'
                }
            });
    });

    $("#password-submit").click(function (){
        var oldpw=$("#oldPassword").val();
        var newpw1=$("#newPassword").val();
        var newpw2=$("#newPasswordConf").val();
        if(newpw2 != newpw1){
                $("#pw-span").html("The two new password inputs are inconsistent.");
            }
            else{
                $("#pw-span").html("");
                $.post("/api/user/password", {
                    password : oldpw,
                    new_password : newpw1,
                    confirm_password :newpw2,
                    'csrfmiddlewaretoken': $.cookie('csrftoken')
                },function (data) {
                    var data_json = $.parseJSON(JSON.stringify(data));
                if(data_json.code == 0){
                    alert(data_json.msg);
                }
                else if(data_json.code == 1){
                    alert(data_json.msg);
                    window.location.href='/'
                }
                });
            }
    });





});
