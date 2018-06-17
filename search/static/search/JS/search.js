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

    $("#btn_search").click(function () {
        var keyword = $("#my_input_search_find").val();
        var near = $("#my_input_search_city").val();
        if (near == "" || near == null){
            //near = "San Francisco";
            $("#my_input_search_city").val('San Francisco, CA');
        }
        displaySearchResultbyajax("/search", keyword, near);
    });

    function displaySearchResultbyajax(url, keyword, near) {
        $.ajax({
            url: url,
            type: "GET",
            data: {
                s: keyword,
                city: near
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

                    for (index = 0; index < len; index++) {
                        $("#resultlist").append("<hr class=\"featurette-divider\" style='background-color: #cccccc'>");
                        $("#resultlist").append(
                            ' <div style="width: 45rem; text-align: left;margin-top: 1rem">' +
                            '    <div style="display:inline-block; width: 10rem;text-align: center">' +
                            '        <a href="http://localhost:8000/restaurant/' +
                            result[index].id + '"><img id="id_tabcon1_1_img" class="card-img-top"' +
                            '    src="' +
                            result[index].img + '"' +
                            '    alt="Generic placeholder image" style="width: 8rem; height: 6rem">' +
                            '        </a>' +
                            '    </div>' +
                            '    <div style="display:inline-block; text-align: left; width: 20rem; vertical-align: top;">' +
                            '        <h5 class="card-title" id="id_tabco1_1_name">' +
                            '            1. <a href="http://localhost:8000/restaurant/' +
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
                            '    <div style="display:inline-block; text-align: left; width: 14rem; vertical-align: top;margin-top: 1rem">' +
                            '        <div><a id="id_tabcon1_1_city">' +
                            result[index].postal_code + '</a></div>' +
                            '        <div><a id="id_tabcon1_1_address">' +
                            result[index].address + '</a></div>' +
                            '    </div>' +
                            '</div>');
                    }

                }
            }
        });
    }

});