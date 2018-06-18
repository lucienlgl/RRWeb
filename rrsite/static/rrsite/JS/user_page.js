function showCollection() {
    $("div.review-container").hide();
    $("div.mainpage-container").hide();
    $("div.collection-container").show();
    $("div.photo-container").hide();

}
function showMainPage() {
$("div.review-container").hide();
    $("div.mainpage-container").show();
    $("div.collection-container").hide();
    $("div.photo-container").hide();
}
function showReview() {
$("div.review-container").show();
    $("div.mainpage-container").hide();
    $("div.collection-container").hide();
    $("div.photo-container").hide();
}
function showPhoto() {
$("div.review-container").hide();
    $("div.mainpage-container").hide();
    $("div.collection-container").hide();
    $("div.photo-container").show();
}

jQuery(document).ready(function () {
    if_myself();
    function if_myself(){

    }




    fresh_star();

    function fresh_star() {

        $("#id_star_1").starRating({
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