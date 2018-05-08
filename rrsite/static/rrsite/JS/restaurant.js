jQuery(document).ready(function () {
    $(".backToTop").goToTop();
    $(window).bind('scroll resize', function () {
        $(".backToTop").goToTop();
    });

    $("#id_userprofile").hide();
    islogin()

    function islogin() {
        var name = $.cookie('username');
        if (name != null) {
            $("#id_login_register").hide();
            $("#id_userprofile").show();
            $("#id_username").text(name);
        }

        // var name = $("#id_username").val();
        // if (name != null && name != "") {
        //     $("#id_login_register").hide();
        //     $("#id_userprofile").show();
        // }
    }

    fresh_thumbs()

    function fresh_thumbs() {
        $(".mythumbs").hover(
            function () {
                $(this).attr("class", "mythumbs fa fa-thumbs-up");
            },
            function () {
                $(this).attr("class", "mythumbs fa fa-thumbs-o-up");
            }
        );
    }

    fresh_star()

    function fresh_star() {
        $("#id_restaurant_star_1").starRating({
            totalStars: 5,
            starSize: 30,
            initialRating: 5,
            emptyColor: 'lightgray',
            hoverColor: 'salmon',
            activeColor: 'crimson',
            useGradient: false,
            readOnly: true
        });
        $(".review_star").starRating({
            totalStars: 5,
            starSize: 20,
            initialRating: 5,
            emptyColor: 'lightgray',
            hoverColor: 'salmon',
            activeColor: 'crimson',
            useGradient: false,
            readOnly: true
        });
    }

    // window.initMap = function () {
    //     var uluru = {lat: -25.363, lng: 131.044};
    //     var map = new google.maps.Map(document.getElementById('id_restaurant_map'), {
    //         zoom: 15,
    //         center: uluru
    //     });
    //     var marker = new google.maps.Marker({
    //         position: uluru,
    //         map: map
    //     });
    //     var t = new Date().getTime();
    //     displayMapbyAjax("/api/restaurant/info", restaurant_id);
    // }

    displayBasicInfobyAjax("/api/restaurant/info", restaurant_id);

    function displayBasicInfobyAjax(url, id) {
        $.ajax({
            url: url,
            type: "GET",
            cache: false,
            data: {
                id: id,
            },
            contentType: "application/json;charset=utf-8",
            success: function (data) {
                data_json = $.parseJSON(JSON.stringify(data));
                if (data_json.code != 1) {
                    alert(data_json.msg)
                } else {
                    var info = data_json.data;
                    $("#id_restaurant_name").text(info.name);
                    $("#id_restaurant_city").text(info.city);
                    $("#id_restaurant_reviewcount").text(info.review_count + " reviews");
                    $("#id_restaurant_address").text(info.address);
                    $("#id_restaurant_postalcode").text(info.postal_code);
                    $("#id_restaurant_star").html('<div id="id_restaurant_star_1" class="my-rating-5" data-rating="' + info.stars + '"></div>');
                    var categoties = ""
                    for (var i = 0; i < info.categories.length; i++) {
                        if (i != 0) {
                            categoties += ",";
                        }
                        categoties += info.categories[i];
                    }
                    $("#id_restaurant_categories").text(categoties);

                    for (var i = 0; i < info.hours.length; i++) {
                        var daytime = info.hours[i];
                        switch (daytime.day) {
                            case "Monday":
                                $("#id_hour_mon").text(daytime.hours);
                                break;
                            case "Tuesday":
                                $("#id_hour_tue").text(daytime.hours);
                                break;
                            case "Wednesday":
                                $("#id_hour_wed").text(daytime.hours);
                                break;
                            case "Thursday":
                                $("#id_hour_thu").text(daytime.hours);
                                break;
                            case "Friday":
                                $("#id_hour_fri").text(daytime.hours);
                                break;
                            case "Saturday":
                                $("#id_hour_sat").text(daytime.hours);
                                break;
                            case "Sunday":
                                $("#id_hour_sun").text(daytime.hours);
                                break;
                        }
                    }

                    fresh_star();

                    mapinit(info.latitude,info.longitude);
                    //google.maps.event.addDomListener(window, 'load', mapinit);
                }
            }
        });
    }

    function mapinit(latitude,longitude) {
        //地图标注
        var uluru = {lat: latitude, lng: longitude};
        var map = new google.maps.Map(document.getElementById('id_restaurant_map'), {
            zoom: 15,
            center: uluru
        });
        var marker = new google.maps.Marker({
            position: uluru,
            map: map
        });
    }

    displaySpecialInfobyAjax("/api/restaurant/special", restaurant_id);

    function displaySpecialInfobyAjax(url, id) {
        $.ajax({
            url: url,
            type: "GET",
            data: {
                id: id,
            },
            contentType: "application/json;charset=utf-8",
            success: function (data) {
                data_json = $.parseJSON(JSON.stringify(data));
                if (data_json.code != 1) {
                    alert(data_json.msg)
                } else {
                    var info = data_json.data;
                    $("#id_restaurant_special").html('');
                    for (var item in info) {
                        var value = info[item];
                        var isjson = typeof(value) == "object";
                        var key = item.replace(/Restaurants/, "").replace(/Business/, "");
                        if (!isjson) {
                            $("#id_restaurant_special").append('<tr><td><b>' + key + '</b></td><td>' + value + '</td></tr>')
                        } else {
                            var j = "";
                            for (var i in value) {
                                if (value[i] == "True") {
                                    if (j != "")
                                        j += ",";
                                    j += i;
                                }
                            }
                            $("#id_restaurant_special").append('<tr><td><b>' + key + '</b></td><td>' + j + '</td></tr>')
                        }
                    }
                    $("#id_restaurant_special").attr('class', 'table table-hover table-sm');
                }
            }
        });
    }

    displayTipsbyAjax("/api/restaurant/tip", restaurant_id);

    function displayTipsbyAjax(url, id) {
        $.ajax({
            url: url,
            type: "GET",
            data: {
                id: id,
            },
            contentType: "application/json;charset=utf-8",
            success: function (data) {
                data_json = $.parseJSON(JSON.stringify(data));
                if (data_json.code != 1) {
                    alert(data_json.msg)
                } else {
                    var tips = data_json.data.tips;
                    for (var i = 0; i < tips.length; i++) {
                        var tip = tips[i];
                        if (i == 0) {
                            $("#id_restaurant_tips").append("" +
                                "<div class=\"card\">" +
                                "    <div class=\"card-header\">" +
                                "        <h3 style=\"color: #e80027;margin-left: 2rem\">Tips</h3>" +
                                "    </div>" +
                                "</div>");
                        } else {
                            $("#id_restaurant_tips").append("<hr class=\"featurette-divider\" style='background-color: rgba(134,214,14,0.33);'>");
                        }
                        $("#id_restaurant_tips").append(
                            '<div id="id_tip" class="row" style="margin-top: 2rem">' +
                            '    <div id="id_tip_icon" class="col-2" style="text-align: center">' +
                            '        <img class="rounded" src="/static/rrsite/Images/icon/icon' + (i + 1) + '.jpg"' +
                            '            alt="icon" style="height: 4rem; width: 4rem;">' +
                            '    </div>' +
                            '    <div class="col-10">' +
                            '        <a style="text-indent:2em">' +
                            tip.text +
                            '        </a>' +
                            '        <div style="text-align: right;color: #5a5a5a;margin-right: 2rem">' +
                            '            <a>' +
                            tip.date +
                            '            </a>' +
                            '            <a class="mythumbs fa fa-thumbs-o-up" style="margin-left: 5rem;"></a>' +
                            '            <a>' +
                            tip.likes +
                            '            likes</a>' +
                            '        </div>' +
                            '    </div>' +
                            '</div>');
                        fresh_thumbs();
                    }
                }
            }
        });
    }

    displayReviewsbyAjax("/api/restaurant/review", restaurant_id, 1);

    function displayReviews(reviews) {
        for (var i = 0; i < reviews.length; i++) {
            var review = reviews[i];
            $("#id_restaurant_reviews").append(
                '<div class="row" style="margin-top: 2rem">' +
                '<div class="col-4">' +
                '        <div class="row">' +
                '            <div class="col-5" style="text-align: center;">' +
                '                <img class="rounded" src="/static/rrsite/Images/icon/icon' + (i + 1) + '.jpg"' +
                '                  style="height: 4rem; width: 4rem;">' +
                '            </div>' +
                '            <div class="col-7" style="color: #5a5a5a">' +
                '                <a style="color: cornflowerblue;font-size: 1.1rem" href="#"><b>' +
                review.user.name +
                '               </b></a>' +
                '                <br><a style="font-size: 0.85rem;margin-top: 0.2rem"><i class="fa fa-child"></i><i' +
                '                   class="fa fa-child"></i> <b>' +
                review.user.friend_count +
                '                   </b> friends</a>' +
                '                <br><a style="font-size: 0.85rem"> &nbsp;<i class="fa fa-star"></i> &nbsp;<b>' +
                review.user.review_count +
                '</b> reviews</a>' +
                '            </div>' +
                '        </div>' +
                '    </div>' +
                '    <div class="col-8">' +
                '        <div class="row" style="margin-top: 1rem">' +
                '            <div id="" class="col-4 review_star" data-rating="' +
                review.stars +
                '           "></div>' +
                '            <div id="" class="col-4"><a>' +
                review.date +
                '           </a></div>' +
                '        </div>' +
                '        <p style="font-size: 1rem; text-indent:2em;color: black;margin-top: 1.5rem">' +
                review.text +
                '        </p>' +
                '        <button type="button" class="btn btn-sm btn-outline-secondary"' +
                '                style="margin-left: 1.5rem"> Userful' +
                '            &nbsp; <a> ' +
                review.useful +
                '           </a></button>' +
                '        <button type="button" class="btn btn-sm btn-outline-secondary"' +
                '                style="margin-left: 1.5rem"> Funny' +
                '            &nbsp; <a>' +
                review.funny +
                '           </a></button>' +
                '        <button type="button" class="btn btn-sm btn-outline-secondary"' +
                '                style="margin-left: 1.5rem"> Cool' +
                '            <a>' +
                review.cool +
                '</a></button>' +
                '    </div>' +
                '</div>');
            $("#id_restaurant_reviews").append(
                '<hr class="featurette-divider" style=\'background-color: rgba(134,214,14,0.33);\'>');
        }
        fresh_star();
    }

    function displayPageofReviews(page_num, page, has_pre, has_next) {
        $("#id_restaurant_reviews").append(
            '<div>' +
            '    <a style="margin-left: 1rem;font-size: 1.2rem">' +
            'Page ' + page + ' of ' + page_num +
            '    </a>' +
            '    <ul id="id_restaurant_reviews_pages" class="pagination" style="float: right;margin-right: 2rem;color: cornflowerblue">' +
            '    </ul>' +
            '</div>');
        var begin = 1;
        var end = page_num;
        if (page_num > 9) {
            if (page <= 5) {
                begin = 1;
                end = 9;
            } else if ((page_num - page) <= 4) {
                begin = page_num - 8;
                end = page_num;
            } else {
                begin = page - 4;
                end = page + 4;
            }
        }
        for (var i = begin; i <= end; i++) {
            if (i == begin) {
                if (has_pre) {
                    $("#id_restaurant_reviews_pages").append('<li class="page-item"><a class="page-link" ><b> Previous </b></a></li>');
                } else {
                    $("#id_restaurant_reviews_pages").append('<li class="page-item disabled"><a class="page-link" ><b> Previous </b></a></li>');
                }

            }
            if (i == page) {
                $("#id_restaurant_reviews_pages").append('<li class="page-item active"><a class="page-link" >' + i + '</a></li>');
            } else {
                $("#id_restaurant_reviews_pages").append('<li class="page-item"><a class="page-link" >' + i + '</a></li>');
            }
            if (i == end) {
                if (has_next) {
                    $("#id_restaurant_reviews_pages").append('<li class="page-item"><a class="page-link" ><b> Next </b></a></li>');
                } else {
                    $("#id_restaurant_reviews_pages").append('<li class="page-item disabled"><a class="page-link" ><b> Next </b></a></li>');
                }
            }
        }
        $(".page-link").click(function () {
            var newpage = $(this).text();
            switch (newpage) {
                case " Previous ":
                    displayReviewsbyAjax("/api/restaurant/review", restaurant_id, page - 1);
                    break;
                case " Next ":
                    displayReviewsbyAjax("/api/restaurant/review", restaurant_id, page + 1);
                    break;
                default:
                    displayReviewsbyAjax("/api/restaurant/review", restaurant_id, parseInt(newpage));
                    break;
            }
        });
    }

    function displayReviewsbyAjax(url, id, page) {
        $.ajax({
            url: url,
            type: "GET",
            data: {
                id: id,
                page: page,
            },
            contentType: "application/json;charset=utf-8",
            success: function (data) {
                data_json = $.parseJSON(JSON.stringify(data));
                if (data_json.code != 1) {
                    alert(data_json.msg)
                } else {
                    var info = data_json.data;
                    var reviews = info.reviews;
                    var page_num = info.page_num;
                    $("#id_restaurant_reviews").html('');
                    $("#id_restaurant_reviews").append(
                        '<div class="card">' +
                        '    <div class="card-header">' +
                        '        <h3 style="color: #e80027;margin-left: 2rem">Recommended Reviews</h3>' +
                        '    </div>' +
                        '</div>');
                    displayReviews(reviews);
                    if (page_num == 1) {
                        $("#id_restaurant_reviews").append('<div><a style="margin-left: 3rem;font-size: 1.2rem">Page 1 of 1</a></div>');
                    } else {
                        displayPageofReviews(page_num, page, info.has_pre, info.has_next);
                    }
                }
            }
        });
    }


});