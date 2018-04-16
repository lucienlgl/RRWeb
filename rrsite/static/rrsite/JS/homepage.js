jQuery(document).ready(function () {

    $(".my-rating-5").starRating({
        totalStars: 5,
        starSize: 20,
        initialRating: 5,
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
            $("#id_username").text("lucien");
        }
    }

    // function csrfSafeMethod(method) {
    //     // these HTTP methods do not require CSRF protection
    //     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    // }
    //
    // $.ajaxSetup({
    //     beforeSend: function (xhr, settings) {
    //         if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
    //             xhr.setRequestHeader("X-CSRFToken", csrftoken);
    //         }
    //     }
    // });

    function displaynavcontext(tabindex, data) {
        html_text = ""
        for (var row = 0; row < 2; row++) {
            html_text += "<div class=\"row\" style=\"margin-top: 2rem\">";
            for (var column = 0; column < 3; column++) {
                html_text += "<div class=\"col-lg-4\" style=\"color: black;\">\n" +
                    "                        <img id=\"id_tabcon1_1_img\" class=\"rounded\"\n" +
                    "                             src=\"";
                html_text += data[row * 3 + column].photo_url;
                html_text += "\" alt=\"Generic placeholder image\" width=\"260px\" height=\"200px\">\n" +
                    "                        <div style=\"text-align:left;margin-top: 0.5rem;margin-left: 3rem;margin-right: 2rem\">\n" +
                    "                            <h5 id=\"id_tabco1_1_name\" href=\" \" style=\"color: #09328d;text-align:left;margin-top: 1rem\">";
                html_text += data[row * 3 + column].name;
                html_text += "</h5>\n" +
                    "                            <div id=\"id_tabcon1_1_star\" class=\"my-rating-5\" data-rating=\"";
                html_text += data[row * 3 + column].stars;
                html_text += "\" style=\"margin-top: 0.5rem\"></div>\n" +
                    "                            <div><a id=\"id_tabcon1_1_city\">";
                html_text += data[row * 3 + column].city;
                html_text += "</a> &nbsp·&nbsp <a id=\"id_tabcon1_1_reviewcount\">";
                html_text += data[row * 3 + column].review_count;
                html_text += " reviews</a></div> <div><a id=\"id_tabcon1_1_address\">";
                html_text += data[row * 3 + column].address;
                html_text += "</a></div></div></div>";
            }
            html_text += "</div>"
        }
        $("#category" + tabindex).html(html_text);
    }

    function displaynavdatabyajax(url, category, tabindex) {
        $.ajax({
            url: url,
            type: "GET",
            data: {
                category: category,
            },
            contentType: "application/json;charset=utf-8",
            success: function (data) {
                data_json = $.parseJSON(JSON.stringify(data));
                if (data_json.code != 1) {
                    alert(data_json.msg)
                } else {
                    displaynavcontext(tabindex, data_json.data)
                }
            }
        });
    }

    displaynavdatabyajax("/api/recommend/category", "Restaurants", 1)
    $("#id_navtab_all").click(function () {
        displaynavdatabyajax("/api/recommend/category", "Restaurants", 1)
    })
    $("#id_navtab_nightlife").click(function () {
        displaynavdatabyajax("/api/recommend/category", "Nightlife", 2)
    })
    $("#id_navtab_fastfood").click(function () {
        displaynavdatabyajax("/api/recommend/category", "Fast_Food", 3)
    })
    $("#id_navtab_coffeetea").click(function () {
        displaynavdatabyajax("/api/recommend/category", "Coffee_&_Tea", 4)
    })
    $("#id_navtab_pizza").click(function () {
        displaynavdatabyajax("/api/recommend/category", "Pizza", 5)
    })


    function displayreview(data) {
        for(var i = 0; i < 5; i++){
            html_review = "";
            html_review += " <div class=\"row\" style=\"margin-left: 3rem\">\n" +
                "                    <div class=\"col-md-2\">\n" +
                "                        <img class=\"rounded-circle\" src=\"";
            html_review += "/static/rrsite/Images/icon1.jpg";
            html_review += "\" alt=\"\" style=\"height: 5rem; width: 5rem\"></div>\n" +
                "                    <div class=\"col-md-10 user-name\">\n" +
                "                        <h4>";
            html_review += data[i].user_id;
            html_review += "</h4>\n" +
                "                        <ul class=\"list-unstyled\">\n" +
                "                            <li>";
            html_review += data[i].date;
            html_review += "                            </li><li>Wrote a review for <a href=\"#\">";
            html_review += data[i].restaurant_id;
            html_review += "</a></li></ul></div></div>" +
                "<hr>\n" +
                "                <div class=\"my-rating-5\" data-rating=\"";
            html_review += data[i].stars;
            html_review +=   "\" style=\"margin-left: 3rem\"></div>\n" +
                "                <p class=\"lead\" style=\"margin-left: 2rem; font-size: 1rem\">";
            html_review += data[i].text;
            html_review += "</p></div>";
            $("#id_review"+(i+1)+"_content").html(html_review);
            $("#id_review"+(i+1)+"_img").attr("src",data[i].photo_url)
        }
    }

    function displayreviewdatabyajax(url) {
        $.ajax({
            url: url,
            type: "GET",
            contentType: "application/json;charset=utf-8",
            success: function (data) {

                data_json = $.parseJSON(JSON.stringify(data));
                if (data_json.code != 1) {
                    alert(data_json.msg)
                } else {
                    displayreview(data_json.data)
                }
            }
        });
    }

    displayreviewdatabyajax("/api/review/hot")
});


