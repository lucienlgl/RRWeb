jQuery(document).ready(function () {
    $(".my-rating-5").starRating({
        totalStars: 5,
        starSize: 25,
        emptyColor: 'lightgray',
        hoverColor: 'salmon',
        activeColor: 'crimson',
        useGradient: false,
        readOnly: true
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    islogin()

    function islogin() {
        var name = getCookie('name');
        if (name == null) {
            $("#id_login_register").hide();
            $("#id_userprofile").show();
            $("#id_username").text("adkfas");
        }
    }

    $("#id_userspace").hover(
        function () {
            $("#id_userspace")
        },
        function () {
            $("#id_userspace").css()
        }
    );


});


