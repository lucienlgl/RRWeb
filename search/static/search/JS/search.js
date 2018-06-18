jQuery(document).ready(function () {

    $(".my-rating").starRating({
        totalStars: 5,
        starSize: 25,
        initialRating: 5,
        emptyColor: 'lightgray',
        hoverColor: 'salmon',
        activeColor: 'crimson',
        useGradient: false,
        readOnly: true
    });

    $("#my_input_search_find").bsSuggest({
        //emptyTip: '未检索到匹配的数据',
        emptyTip: '',
        allowNoKeyword: false,   //是否允许无关键字时请求数据。为 false 则无输入时不执行过滤请求
        multiWord: true,         //以分隔符号分割的多关键字支持
        separator: " ",          //多关键字支持时的分隔符，默认为空格
        getDataMethod: "url",    //获取数据的方式，总是从 URL 获取
        url: '//localhost:8000/search/suggest?s=', //优先从url ajax 请求 json 帮助数据，注意最后一个参数为关键字请求参数
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

    $("#my_input_search_city").bsSuggest({
        //emptyTip: '未检索到匹配的数据',
        emptyTip: '',
        allowNoKeyword: false,   //是否允许无关键字时请求数据。为 false 则无输入时不执行过滤请求
        multiWord: true,         //以分隔符号分割的多关键字支持
        separator: " ",          //多关键字支持时的分隔符，默认为空格
        getDataMethod: "url",    //获取数据的方式，总是从 URL 获取
        url: '//localhost:8000/search/suggest_city?s=', //优先从url ajax 请求 json 帮助数据，注意最后一个参数为关键字请求参数
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

    var keyword;
    var near;
    var lat = [];
    var lon = [];

    search();
    function search() {
        keyword = $("#my_input_search_find").val();
        near = $("#my_input_search_city").val();
        if (near == "" || near == null) {
            //near = "San Francisco";
            $("#my_input_search_city").val('San Francisco, CA');
        }
        displaySearchResultbyajax("/search", keyword, near, 1);
    }


    $("#btn_search").click(function () {
        search();
    });

    //分页
    function displayPageofResults(page_num, page) {
        $("#resultlist").append(
            '<div>' +
            '    <hr class="featurette-divider" style=\'background-color: #cccccc\'>' +
            '    <a style="float:left; margin-left: 1rem;font-size: 1.2rem">' +
            'Page ' + page + ' of ' + page_num +
            '    </a>' +
            '    <ul id="id_results_pages" class="pagination" style="float: right;margin-right: 2rem;color: cornflowerblue">' +
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
                if (page > 1) {
                    $("#id_results_pages").append('<li class="page-item"><a class="page-link" ><b> Previous </b></a></li>');
                } else {
                    $("#id_results_pages").append('<li class="page-item disabled"><a class="page-link" ><b> Previous </b></a></li>');
                }

            }
            if (i == page) {
                $("#id_results_pages").append('<li class="page-item active"><a class="page-link" >' + i + '</a></li>');
            } else {
                $("#id_results_pages").append('<li class="page-item"><a class="page-link" >' + i + '</a></li>');
            }
            if (i == end) {
                if (page < page_num) {
                    $("#id_results_pages").append('<li class="page-item"><a class="page-link" ><b> Next </b></a></li>');
                } else {
                    $("#id_results_pages").append('<li class="page-item disabled"><a class="page-link" ><b> Next </b></a></li>');
                }
            }
        }
        $(".page-link").click(function () {
            var newpage = $(this).text();
            switch (newpage) {
                case " Previous ":
                    displaySearchResultbyajax("/search", keyword, near, page - 1);
                    break;
                case " Next ":
                    displaySearchResultbyajax("/search", keyword, near, page + 1);
                    break;
                default:
                    displaySearchResultbyajax("/search", keyword, near, parseInt(newpage));
                    break;
            }
        });
    }

    function mapinit(latitude, longitude) {
        //地图标注
        var uluru = {lat: latitude, lng: longitude};
        map = new google.maps.Map(document.getElementById('id_map_mark'), {
            zoom: 12,
            center: uluru
        });
        return map;
    }

    function mapmark(map, index, latitude, longitude, id, name, stars, city, review_count, address) {
        var uluru = {lat: latitude, lng: longitude};
        var contentString = '' +
            '<div class="card" style="width: 10rem; font-size: 0.75rem">' +
            '    <div class="card-body" style="text-align: left; padding:0">' +
            '        <a href="/restaurant/' + id + '"><h5 class="card-title" id="id_tabco1_1_name">' + name + '</h5></a>' +
            '        <div class="my_rating_map" data-rating="' + stars + '"></div>' +
            '        <div><a>' + city + '</a> &nbsp·&nbsp<a>' + review_count + ' reviews</a></div>' +
            '        <div><a>' + address + '</a></div>' +
            '    </div>' +
            '</div>' +
            '<script>' +
            '$(".my_rating_map").starRating({' +
            '            totalStars: 5,' +
            '            starSize: 20,' +
            '            initialRating: 5,' +
            '            emptyColor: \'lightgray\',' +
            '            hoverColor: \'salmon\',' +
            '            activeColor: \'crimson\',' +
            '            useGradient: false,' +
            '            readOnly: true' +
            '        });' +
            '</script>';

        var infowindow = new google.maps.InfoWindow({
            content: contentString
        });

        var marker = new google.maps.Marker({
            position: uluru,
            label: index,
            map: map
        });
        marker.addListener('click', function () {
            infowindow.open(map, marker);
        });
    }

    function displaySearchResultbyajax(url, keyword, near, page) {
        $.ajax({
            url: url,
            type: "GET",
            data: {
                s: keyword,
                city: near,
                p: page
            },
            contentType: "application/json;charset=utf-8",
            success: function (data) {
                if (data.code != 1) {
                    alert(data.msg)
                } else {
                    $("#resultlist").html("");

                    var index, len, result;
                    result = data.data.data;
                    len = result.length;
                    var map = mapinit(result[0].location.lat, result[0].location.lon);

                    for (index = 0; index < len; index++) {
                        $("#resultlist").append("<hr class=\"featurette-divider\" style='background-color: #cccccc;margin-top: 2rem'>");
                        $("#resultlist").append(
                            ' <div style="width: 45rem; text-align: left;margin-top: 1rem">' +
                            '    <div style="display:inline-block; width: 10rem;text-align: center">' +
                            '        <a href="http://localhost:8000/restaurant/' +
                            result[index].id + '"><img id="id_tabcon1_1_img" class="card-img-top" ' +
                            '    src="' +
                            result[index].cover_url + '"' +
                            '    alt="Generic placeholder image" style="width: 8rem; height: 6rem; box-shadow: 0px 0px 10px #888888;">' +
                            '        </a>' +
                            '    </div>' +
                            '    <div style="display:inline-block; text-align: left; width: 18rem; vertical-align: top;margin-left: 1rem">' +
                            '        <h5 class="card-title" id="id_tabco1_1_name">' +
                            '            ' +
                            (index + 1) + '. <a href="http://localhost:8000/restaurant/' +
                            result[index].id + '">' +
                            result[index].name + '</a></h5>' +
                            '        <div style="margin-top: 0.5rem;">' +
                            '            <div id="id_tabcon1_1_star" class="my-rating" data-rating="' +
                            result[index].stars + '"' +
                            '                 style="display: inline-block"></div>' +
                            '            <div style="display: inline-block;vertical-align: top;"> &nbsp; ' +
                            result[index].review_count + ' reviews</div>' +
                            '        </div>' +
                            '        <div><a id="id_tabcon1_1_city">$$</a> &nbsp·&nbsp' +
                            '            <a> ' +
                            result[index].category + ' </a></div>' +
                            '    </div>' +
                            '    <div style="display:inline-block; text-align: left; width: 13rem; vertical-align: top;margin-left:2rem;margin-top: 1rem">' +
                            '        <div><a id="id_tabcon1_1_city">' +
                            result[index].postal_code + '</a></div>' +
                            '        <div><a id="id_tabcon1_1_address">' +
                            result[index].address + '</a></div>' +
                            '    </div>' +
                            '</div>');

                        mapmark(map, index + 1, result[index].location.lat, result[index].location.lon,
                            result[index].id, result[index].name, result[index].stars, result[index].city,
                            result[index].review_count, result[index].address);
                    }

                    displayPageofResults(data.data.page_nums, page)
                    fresh_star()
                }
            }
        });
    }

    // var X = $('#right_map').offset().top;
    // var Y = $('#right_map').offset().left;
    // alert(X+"hhhhh"+Y)
    // $("#id_map_card").css({"position":"absolute","top":"X","left":"Y"});

    fresh_star()

    function fresh_star() {
        $(".my-rating").starRating({
            totalStars: 5,
            starSize: 20,
            initialRating: 5,
            emptyColor: 'lightgray',
            hoverColor: 'salmon',
            activeColor: 'crimson',
            useGradient: false,
            readOnly: true
        });
        $(".my_rating_map").starRating({
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


});