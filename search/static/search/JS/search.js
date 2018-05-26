jQuery(document).ready(function () {

    var search_url = "/search/"

    $('.searchList').on('click', '.searchItem', function(){
        $('.searchList .searchItem').removeClass('current');
        $(this).addClass('current');
    });

    $.each($('.subfieldContext'), function(i, item){
        $(this).find('li:gt(2)').hide().end().find('li:last').show();
    });

    function removeByValue(arr, val) {
      for(var i=0; i<arr.length; i++) {
        if(arr[i] == val) {
          arr.splice(i, 1);
          break;
        }
      }
    }
    $('.subfieldContext .more').click(function(e){
        var $more = $(this).parent('.subfieldContext').find('.more');
        if($more.hasClass('show')){

            if($(this).hasClass('define')){
                $(this).parent('.subfieldContext').find('.more').removeClass('show').find('.text').text('自定义');
            }else{
                $(this).parent('.subfieldContext').find('.more').removeClass('show').find('.text').text('更多');
            }
            $(this).parent('.subfieldContext').find('li:gt(2)').hide().end().find('li:last').show();
        }else{
            $(this).parent('.subfieldContext').find('.more').addClass('show').find('.text').text('收起');
            $(this).parent('.subfieldContext').find('li:gt(2)').show();
        }

    });

    $('.sideBarShowHide a').click(function(e) {
        if($('#main').hasClass('sideBarHide')){
            $('#main').removeClass('sideBarHide');
            $('#container').removeClass('sideBarHide');
        }else{
            $('#main').addClass('sideBarHide');
            $('#container').addClass('sideBarHide');
        }

    });
    var key_words = "{{ key_words }}"





    $('.searchList').on('click', '.searchItem', function(){
        $('.searchList .searchItem').removeClass('current');
        $(this).addClass('current');
    });

    // 联想下拉显示隐藏
    $('.searchInput').on('focus', function(){
        $('.dataList').show()
    });

    // 联想下拉点击
    $('.dataList').on('click', 'li', function(){
        var text = $(this).text();
        $('.searchInput').val(text);
        $('.dataList').hide()
    });

    hideElement($('.dataList'), $('.searchInput'));




    var searchArr;
    //定义一个search的，判断浏览器有无数据存储（搜索历史）
    if(localStorage.search){
        //如果有，转换成 数组的形式存放到searchArr的数组里（localStorage以字符串的形式存储，所以要把它转换成数组的形式）
        searchArr= localStorage.search.split(",")
    }else{
        //如果没有，则定义searchArr为一个空的数组
        searchArr = [];
    }
    //把存储的数据显示出来作为搜索历史
    MapSearchArr();

    function add_search(){
        var val = $(".searchInput").val();
        if (val.length>=2){
            //点击搜索按钮时，去重
            KillRepeat(val);
            //去重后把数组存储到浏览器localStorage
            localStorage.search = searchArr;
            //然后再把搜索内容显示出来
            MapSearchArr();
        }

        window.location.href=search_url+'?q='+val+"&s_type="+$(".searchItem.current").attr('data-type')

    }

    function MapSearchArr(){
        var tmpHtml = "";
        var arrLen = 0
        if (searchArr.length > 6){
            arrLen = 6
        }else {
            arrLen = searchArr.length
        }
        for (var i=0;i<arrLen;i++){
            tmpHtml += '<li><a href="/search?q='+searchArr[i]+'">'+searchArr[i]+'</a></li>'
        }
        $(".mySearch .historyList").append(tmpHtml);
    }
    //去重
    function KillRepeat(val){
        var kill = 0;
        for (var i=0;i<searchArr.length;i++){
            if(val===searchArr[i]){
                kill ++;
            }
        }
        if(kill<1){
            searchArr.unshift(val);
        }else {
            removeByValue(searchArr, val)
            searchArr.unshift(val)
        }
    }

});