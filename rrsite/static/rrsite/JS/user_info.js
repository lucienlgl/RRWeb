    function bindEmail() {
        var txt_email = "<div class=\"hd\">\n" +
            "                <h4><a href=\"#\" onclick=\"backAccount()\">Account Information</a>\n" +
            "                    " +
            "                    <span>\n" +
            "                    <em> >    </em>\n" +
            "                    Modify Email\n" +
            "                </span>\n" +
            "                </h4>\n" +
            "            </div>\n" +
            "            <div class=\"con\">\n" +
            "                <p style=\"color: #999\">Please input your E-mail address.</p>\n" +
            "                <form method=\"post\">\n" +
            "                    <div class=\"form-box\">\n" +
            "                        <ul>\n" +
            "                            <li>\n" +
            "                                <label style=\"width: 130px;text-align: right;float: left;padding-top: 10px\" for=\"email\">New E-mail:</label>\n" +
            "                                <input style=\"width: 250px;left: 13px;position: relative\" class=\"form-control\" name=\"email\" id=\"email\" type=\"text\">\n" +
            "                            </li>\n" +
            "                        </ul>\n" +
            "                    </div>\n" +
            "                    <input class=\"btn btn-primary\" type=\"button\" value=\"Submit\" style=\"left: 185px;position: relative\">\n" +
            "                </form>\n" +
            "            </div>\n";
        <!--html代码定义完毕-->
        $("div.v-pills-account").empty().append(txt_email);
    }

    function modifyPassword() {
        var txt_password = "<div class=\"hd\">\n" +
            "                <h4><a href=\"#\" onclick=\"backAccount()\">Account Information</a>\n" +
            "                    " +
            "                    <span>\n" +
            "                    <em> > </em>\n" +
            "                    Modify Password\n" +
            "                    </span>\n" +
            "                </h4>\n" +
            "            </div>\n" +
            "            <div class=\"con\">\n" +
            "                <p style=\"color: #999\">In order to make sure your account's safety,please don't user the same password with other site.</p>\n" +
            "                <form method=\"post\">\n" +
            "                    <div class=\"form-box\" style=\"left: 30px;position: relative\">\n" +
            "                        <ul>\n" +
            "                            <li>\n" +
            "                                <label style=\"position: relative;left:10px\" for=\"newPassword\">New Password:</label>\n" +
            "                                <input style=\"width: 250px;left: 13px;position: relative\" class=\"form-control\" name=\"newPassword\" id=\"newPassword\" type=\"text\">\n" +
            "                            </li>\n" +
            "                            <li>\n" +
            "                                <label style=\"position: relative;left:10px\" for=\"newPasswordConf\">Confirm New Password:</label>\n" +
            "                                <input style=\"width: 250px;left: 13px;position: relative\" class=\"form-control\" id=\"newPasswordConf\" type=\"text\">\n" +
            "                            </li>\n" +
            "                        </ul>\n" +
            "                    </div>\n" +
            "                    <input class=\"btn btn-primary\" style=\"position: relative;left:85px\" type=\"button\" value=\"Submit\">\n" +
            "                </form>\n" +
            "            </div>"
        $("div.v-pills-account").empty().append(txt_password);
    }

    function modifyPhone() {
        var txt_phone = "<div class=\"hd\">\n" +
            "                <h4><a href=\"#\" onclick=\"backAccount()\">Account Information</a>\n" +
            "                    " +
            "                    <span>\n" +
            "                    <em> > </em>\n" +
            "                    Modify Phone Number\n" +
            "                    </span>\n" +
            "                </h4>\n" +
            "            </div>\n" +
            "            <div class=\"con\">\n" +
            "                <form method=\"post\" style=\"left: 50px;position: relative\">\n" +
            "                    <div class=\"form-box\">\n" +
            "                        <ul>\n" +
            "                            <li>\n" +
            "                                <label style=\"left: 10px;position: relative\" for=\"newPhone\">New Phone Number:</label>\n" +
            "                                <input name=\"newPhone\" id=\"newPhone\" type=\"text\" class=\"form-control\" style=\"width: 250px;left: 13px;position: relative\">\n" +
            "\n" +
            "                            </li>\n" +
            "                            <li>\n" +
            "                                <label style=\"left: 10px;position: relative\" for=\"vCode\">Verification Code:</label>\n" +
            "                                <div>\n" +
            "                                <input name=\"vCode\" id=\"vCode\" type=\"text\" class=\"form-control\" style=\"width: 100px;left: 13px;position: relative;float: left\">\n" +
            "                                <input class=\"btn btn-primary\" value=\"Get Code\" type=\"button\" style=\"color: #fff;float: left;left: 20px;position: relative\">\n" +
            "                                </div>\n" +
            "                            </li>\n" +
            "                        </ul>\n" +
            "                    </div>\n" +
            "                    <input type=\"button\" value=\"Submit\" class=\"btn btn-primary\" style=\"position: relative;top: 30px;right:180px\">\n" +
            "                </form>\n" +
            "            </div>";
        $("div.v-pills-account").empty().append(txt_phone);
    }

    function backAccount() {
        var txt_account = "<div class=\"account-info\">\n" +
            "            <div class=\"hd\">\n" +
            "                <h4>Account Information</h4>\n" +
            "            </div>\n" +
            "            <div class=\"con\">\n" +
            "                <div class=\"form-box\" >\n" +
            "                    <ul>\n" +
            "                        <li>\n" +
            "                            <label for=\"\">E-mail box :</label>\n" +
            "                            <span>E-mail has not been bound.    </span>\n" +
            "                            <a href=\"#\" class=\"bind-email\" onclick=\"bindEmail()\">[Bind now]</a>\n" +
            "                        </li>\n" +
            "                        <li>\n" +
            "                            <label for=\"\">Password :</label>\n" +
            "                            <span>******</span>\n" +
            "                            <a href=\"#\" class=\"modify-password\" onclick=\"modifyPassword()\">[Modify]</a>\n" +
            "                        </li>\n" +
            "                        <li>\n" +
            "                            <label for=\"\">Phone Number :</label>\n" +
            "                            <span>18813062966</span>\n" +
            "                            <a href=\"#\" class=\"modify-phone\" onclick=\"modifyPhone()\">[Modify]</a>\n" +
            "                        </li>\n" +
            "                    </ul>\n" +
            "                </div>\n" +
            "            </div>\n" +
            "        </div>";
        $("div.v-pills-account").empty().append(txt_account);

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

    $("#basic_submit").click(function () {
        var userNickname = $("#userNickname").val();
        var userSex = $("input[name='userSex']:checked").val();
        var userCityname = $("#userCityname").val();
        var userRemark = $("#userRemark").val();
        alert(userRemark)
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

    init();
    function init() {
        $.get("/api/user/basic", function (data) {
            var data_json = $.parseJSON(JSON.stringify(data));
            if (data_json.code == 0) {
                alert(data_json.msg);
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
});
