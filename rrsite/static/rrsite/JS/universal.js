jQuery(document).ready(function () {

    $(".backToTop").goToTop();
    $(window).bind('scroll resize', function () {
        $(".backToTop").goToTop({
            pageWidth: 960,
            duration: 0
        });
    });

    $("#id_userprofile").hide();

    islogin()
    function islogin() {
        var name = $("#id_username").val();
        if (name != null && name != "") {
            $("#id_login_register").hide();
            $("#id_userprofile").show();
        }
    }

});