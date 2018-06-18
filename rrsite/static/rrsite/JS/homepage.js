jQuery(document).ready(function () {

    $("#my_input_near").val("Las Vegas");

    $("#my_input_find").bsSuggest({
        //emptyTip: '未检索到匹配的数据',
        emptyTip: '',
        allowNoKeyword: false,   //是否允许无关键字时请求数据。为 false 则无输入时不执行过滤请求
        multiWord: true,         //以分隔符号分割的多关键字支持
        separator: " ",          //多关键字支持时的分隔符，默认为空格
        getDataMethod: "url",    //获取数据的方式，总是从 URL 获取
        url: '/search/suggest?s=', //优先从url ajax 请求 json 帮助数据，注意最后一个参数为关键字请求参数
        //jsonp: 'cb',    //如果从 url 获取数据，并且需要跨域，则该参数必须设置
        fnProcessData: function (json) {    // url 获取数据时，对数据的处理，作为 fnGetData 的回调函数
            console.log(json);
            var index, len, data = {value: []};
            if (!json || !json.code) {
                return false;
            }
            var result = new Set();
            len = json.data.length;
            for (index = 0; index < len; index++) {
                result.add(json.data[index].name)
            }

            result.forEach(function (element, sameElement, set) {
                data.value.push({
                    word: element
                });
            });
            data.defaults = 'rrweb';

            //字符串转化为 js 对象
            return data;
        }
    }).on('onDataRequestSuccess', function (e, result) {
        console.log('onDataRequestSuccess: ', result);
    }).on('onSetSelectValue', function (e, keyword, data) {
        console.log('onSetSelectValue: ', keyword, data);
    }).on('onUnsetSelectValue', function () {
        console.log("onUnsetSelectValue");
    });

    $("#my_input_near").bsSuggest({
        //emptyTip: '未检索到匹配的数据',
        emptyTip: '',
        allowNoKeyword: false,   //是否允许无关键字时请求数据。为 false 则无输入时不执行过滤请求
        multiWord: true,         //以分隔符号分割的多关键字支持
        separator: " ",          //多关键字支持时的分隔符，默认为空格
        getDataMethod: "url",    //获取数据的方式，总是从 URL 获取
        url: '/search/suggest_city?s=', //优先从url ajax 请求 json 帮助数据，注意最后一个参数为关键字请求参数
        //jsonp: 'cb',    //如果从 url 获取数据，并且需要跨域，则该参数必须设置
        fnProcessData: function (json) {    // url 获取数据时，对数据的处理，作为 fnGetData 的回调函数
            console.log(json);
            var index, len, data = {value: []};
            if (!json || !json.code) {
                return false;
            }
            var result = new Set();
            len = json.data.length;
            for (index = 0; index < len; index++) {
                result.add(json.data[index].city)
            }
            for (index = 0; index < len; index++) {
                result.add(json.data[index].address)
            }

            result.forEach(function (element, sameElement, set) {
                data.value.push({
                    word: element
                });
            });
            data.defaults = 'rrweb';

            //字符串转化为 js 对象
            return data;
        }
    }).on('onDataRequestSuccess', function (e, result) {
        console.log('onDataRequestSuccess: ', result);
    }).on('onSetSelectValue', function (e, keyword, data) {
        console.log('onSetSelectValue: ', keyword, data);
    }).on('onUnsetSelectValue', function () {
        console.log("onUnsetSelectValue");
    });


    $(".mynav-content").hover(function () {
            $(this).find('hr').show();
        },
        function () {
            $(this).find('hr').hide();
        }
    );


    function checkScroll() {
        var startY = $('#mynavbar').height() * 2; //The point where the navbar changes in px

        if ($(window).scrollTop() > startY) {
            $('#mynavbar').addClass("bg-dark");
            // $('#mynavbar').removeClass("navbar-dark");
            // $('#mynavbar').addClass("navbar-light");

            // $('#mynavbar').css({
            //     "background-color": "rgba(244,78,4,0.74)",
            //     "border-bottom-style": "groove",
            //     "border-bottom-width": "1px"
            // })
        } else {
            $('#mynavbar').removeClass("bg-dark");
            // $('#mynavbar').removeClass("navbar-light");
            // $('#mynavbar').addClass("navbar-dark");

            //$('#mynavbar').removeAttr("style")
        }
    }

    if ($('#mynavbar').length > 0) {
        $(window).on("scroll load resize", function () {
            checkScroll();
        });
    }

    function displaynavcontext(tabindex, data) {
        html_text = ""
        for (var row = 0; row < 2; row++) {
            html_text += "<div class=\"row\" style=\"margin-top: 2rem\">";
            for (var column = 0; column < 3; column++) {
                html_text += "<div class=\"col-lg-4\" style=\"color: black;\">" +
                    "                        <a href='/restaurant/" +
                    data[row * 3 + column].id +
                    "'><img id=\"id_tabcon1_1_img\" class=\"rounded\"" +
                    "                             src=\"";
                html_text += data[row * 3 + column].photo_url;
                html_text += "\" alt=\"Generic placeholder image\" width=\"260px\" height=\"200px\"></a>" +
                    "                        <div style=\"text-align:left;margin-top: 0.5rem;margin-left: 3rem;margin-right: 2rem\">" +
                    "                            <a href='/restaurant/" +
                    data[row * 3 + column].id +
                    "'><h5 id=\"id_tabco1_1_name\" href=\" \" style=\"color: #09328d;text-align:left;margin-top: 1rem\">";
                html_text += data[row * 3 + column].name;
                html_text += "</h5></a>" +
                    "                            <div id=\"id_tabcon" + tabindex + "_" + (row * 3 + column) + "_star\" class=\"my-rating-5\" data-rating=\"";
                html_text += data[row * 3 + column].stars;
                html_text += "\" style=\"margin-top: 0.5rem\"></div>" +
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
        $("#category" + tabindex).html("");
        $("#category" + tabindex).html(html_text);


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
        for (var i = 0; i < 5; i++) {
            html_review = "";
            html_review += " <div class=\"row\" style=\"margin-left: 3rem\">" +
                "                    <div class=\"col-md-2\">" +
                "                        <img class=\"rounded-circle\" src=\"";
            html_review += "/static/rrsite/Images/icon/icon" + (i + 2) + ".jpg";
            html_review += "\" alt=\"\" style=\"height: 5rem; width: 5rem\"></div>" +
                "                    <div class=\"col-md-10 user-name\">" +
                "                        <a href='/user_info'><h4>";
            html_review += data[i].user__name;
            html_review += "</h4></a>" +
                "                        <ul class=\"list-unstyled\">" +
                "                            <li>";
            html_review += data[i].date;
            html_review += "                            </li><li>Wrote a review for <a href='/restaurant/" +
                data[i].restaurant_id + "'>";
            html_review += data[i].restaurant__name;
            html_review += "</a></li></ul></div></div><hr>" +
                "                <div class=\"my-rating-5\" data-rating=\"";
            html_review += data[i].stars;
            html_review += "\" style=\"margin-left: 3rem\"></div>" +
                "                <p class=\"lead\" style=\"margin-left: 2rem; font-size: 1rem; text-indent:2em;color: black\">";
            if (data[i].text.length > 800) {
                html_review += data[i].text.substr(0, 900);
                html_review += "......"
            } else {
                html_review += data[i].text;
            }
            html_review += "</p></div>";
            $("#id_review" + (i + 1) + "_content").html(html_review);
            $("#id_review" + (i + 1) + "_img").attr("src", data[i].photo_url);
        }
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

    
    $('#btn_search').click(function () {
        var keyword = $("#my_input_find").val();
        var near = $("#my_input_near").val();
        if (near == "" || near == null){
            near = "Las Vegas";
        }
        window.location.href = "/search/result?s="+keyword+"&city="+near;
    });
});


