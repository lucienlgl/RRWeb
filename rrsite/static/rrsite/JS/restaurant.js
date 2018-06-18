jQuery(document).ready(function () {

    var header_height = $("#myheader").height();

    $("#mymain").css({
        "background-image": "url(/static/rrsite/Images/bg_restaurant.jpg)",
        "background-repeat": "no-repeat",
        "background-position": "0 height"
    });

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

    $(".first-slide").hover(
        function () {
            $(this).stop(true);
            $("#id_photo_2").stop(true);
            $("#id_photo_2").animate({
                width: "14rem",
                height: "14rem"
            }, "fast");
            $(this).animate({
                width: "16rem",
                height: "16rem"
            }, "fast");
        },
        function () {
            $(this).stop(true);
            $("#id_photo_2").stop(true);
            $(this).animate({
                width: "14rem",
                height: "14rem"
            }, "fast");
            $("#id_photo_2").animate({
                width: "15.5rem",
                height: "15.5rem"
            }, "fast");
        }
    );

    $("#id_restaurant_photo_no").hide();
    $("#id_restaurant_photo_few").hide();

    // window.initMap = function () {
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


                        var daytime = info.hours;
                        $("#id_hour_mon").text(daytime.Monday);
                        $("#id_hour_tue").text(daytime.Tuesday);
                        $("#id_hour_wed").text(daytime.Wednesday);
                        $("#id_hour_thu").text(daytime.Thursday);
                        $("#id_hour_fri").text(daytime.Friday);
                        $("#id_hour_sat").text(daytime.Saturday);
                        $("#id_hour_sun").text(daytime.Sunday);

                        fresh_star();

                        mapinit(info.latitude, info.longitude);
                        //google.maps.event.addDomListener(window, 'load', mapinit);
                    }
                }
            }
        );
    }

    function mapinit(latitude, longitude) {
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


    // 图片
    var isPhotoMany = false;
    var isStart_photo = true;
    var has_next_page_photo = false;
    var page_now_photo = 1;
    var photo_index = 0;
    var photo_num = 0;
    var photos_urls = new Array();

    //若图片数目大于3
    function initPhoto() {
        if (isPhotoMany) {
            if (isStart_photo) {
                isStart_photo = false;
                setPhotourl(0);
                //设置定时刷新
                setInterval(function () {
                    if (photo_index < photos_urls.length - 5) {
                        photo_index += 3;
                    } else {
                        photo_index = photos_urls.length - 3;
                    }
                    setPhotourl(photo_index);
                }, 8000);
                //设置前后监听
                $("#id_photo_prev").click(function () {
                    if (photo_index != 0) {
                        photo_index -= 1;
                        setPhotourl(photo_index);
                    }
                });
                $("#id_photo_next").click(function () {
                    if (photo_index < photos_urls.length - 3) {
                        photo_index += 1;
                        setPhotourl(photo_index);
                    }
                });
            }
        }
    }

    function setPhotourl(photo_index) {
        $("#id_photo_1").attr("src", photos_urls[photo_index]);
        $("#id_photo_2").attr("src", photos_urls[photo_index + 1]);
        $("#id_photo_3").attr("src", photos_urls[photo_index + 2]);
        if (photo_index >= (photos_urls.length - 4) && has_next_page_photo) {
            displayPhotos("/api/restaurant/photo", restaurant_id, ++page_now_photo);
        }
    }

    displayPhotos("/api/restaurant/photo", restaurant_id, 1);

    function displayPhotos(url, id, page) {
        $.ajax({
            url: url,
            type: "GET",
            cache: false,
            data: {
                id: id,
                page: page
            },
            contentType: "application/json;charset=utf-8",
            success: function (data) {
                data_json = $.parseJSON(JSON.stringify(data));
                if (data_json.code != 1) {
                    if (data_json.msg == "无图片信息") {
                        $("#id_restaurant_photo_many").hide();
                        $("#id_restaurant_photo_few").hide();
                        $("#id_restaurant_photo_no").show();
                    }
                    //alert(data_json.msg)
                } else {
                    var photos_data = data_json.data;
                    photo_num = photos_data.photo_num;
                    var photos = photos_data.photos;
                    if (photo_num > 3) {
                        $("#id_restaurant_photo_no").hide();
                        $("#id_restaurant_photo_few").hide();
                        $("#id_restaurant_photo_many").show();
                        $("#id_restaurant_photonum_many").text(photo_num + " Photos");
                        has_next_page_photo = photos_data.has_next;
                        isPhotoMany = true;
                        for (var i = 0; i < photos_data.photos_this_page; i++) {
                            photos_urls.push(photos[i].url);
                        }
                        initPhoto();
                    } else {
                        $("#id_restaurant_photo_no").hide();
                        $("#id_restaurant_photo_many").hide();
                        $("#id_restaurant_photo_few").show();
                        $("#id_restaurant_photo_few").html("");
                        var width = 14;
                        var height = 14;
                        if (photo_num == 1) {
                            width = 24;
                            height = 18;
                        } else if (photo_num == 2) {
                            width = 18;
                            height = 17;
                        }
                        var htmltext = '<div style="width: 45rem; height: 20rem; margin-top: 2rem; text-align: center">';
                        for (var i = 0; i < photo_num; i++) {
                            htmltext +=
                                '<img class="img-fluid img-rounded"  data-src="holder.js/200*200/auto"\n' +
                                '    style="padding: 0.2rem;width: ' + width + 'rem; height: ' + height + 'rem; box-shadow: 0px 0px 10px #888888;"\n' +
                                '    src="' + photos[i].url + '" alt="photo">';
                        }
                        htmltext +=
                            '<br><p style="color: red; margin-top: 0.5rem"><b id="id_restaurant_photonum">Just '
                            + photo_num + ' Photos</b></p></div>';
                        $("#id_restaurant_photo_few").html(htmltext);
                    }
                }
            }
        });
    }

    //商家特殊服务
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

    //tips
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

    //Reviews
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

    //Reviews分页
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

    //写评论
    var star_rated_myreview = 0;
    $("#btn_writeReview").click(function () {
        var user = $("#id_username").text();
        if (user == null || user == "") {
            window.location.href = '/login'
        } else {
            star_rated_myreview = 0;
            $("#myModal").modal("show");
            initReviewStar(star_rated_myreview);
        }
    });
    $("#id_review_star").mouseenter(function () {
        initReviewStar(star_rated_myreview);
    });

    function initReviewStar(rating) {
        $("#id_review_star").starRating({
            totalStars: 5,
            starSize: 30,
            emptyColor: 'lightgray',
            hoverColor: 'crimson',
            activeColor: 'crimson',
            useFullStars: true,
            initialRating: rating,
            strokeWidth: 0,
            useGradient: false,
            callback: function (currentRating, $el) {
                star_rated_myreview = currentRating;
            }
        });
    }

    $("#btn_review_submit").click(function () {
        var review_text = $("#id_myreview_text").val();
        if (star_rated_myreview == 0) {
            alert("The star rating can not be 0")
        } else if (review_text == null || review_text == "") {
            alert("The Review can not be empty!")
        } else {
            $.post("/api/restaurant/review", {
                    id: restaurant_id,
                    stars: star_rated_myreview,
                    text: review_text,
                    'csrfmiddlewaretoken': $.cookie('csrftoken'),
                },
                function (data) {
                    data_json = $.parseJSON(JSON.stringify(data));
                    alert(data_json.msg)
                    if (data_json.code == 1) {
                        $("#myModal").modal("hide");
                    }
                });
        }
    });

});