function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
console.log(csrftoken);

//Ajax call
function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('.likes').click(function () {
    var button = $(this);
    var count = button.siblings('.like_count');
    var countDislike = button.siblings('.dislike_count')
    var currentLikeCount = count.text();
    var currentDislikeCount = countDislike.text();
    var id = $(this).attr("data-prod");

    $.ajax({
        url: '/products/like/' + id + '/',
        type: 'POST',
        success: function(data) {
            console.log(data, countDislike)
            if (data === "False") {
                countDislike.text(+currentDislikeCount - 1);
            }
        }
    });
    button.siblings('.dislikes').attr("disabled", false);
    button.attr("disabled", true);
    count.text(+currentLikeCount + 1);
});


$('.dislikes').click(function () {
    var button = $(this);
    var count = button.siblings('.dislike_count');
    var countLike = button.siblings('.like_count');
    var currentDislikeCount = count.text();
    var currentLikeCount = countLike.text();
    var id = $(this).attr("data-prod");

    $.ajax({
        url: '/products/dislike/' + id + '/',
        type: 'POST',
        success: function(data) {
            if(data === "False") {
                countLike.text(+currentLikeCount -1);

            }
        }
    });
    button.siblings('.likes').attr("disabled", false);
    button.attr("disabled", true);
    count.text(+currentDislikeCount + 1);
});


$('#comment').click(function(event) {
    event.preventDefault();
    // pobierz text komentarza
    var id = $(this).attr("data-prod");
    var comment = $('#comment-input').val();
    // wyczysc input
    // $('#comment-input').val('');
    // umiec comentarz w nowym divie

    // wyslij komentarz do bazy danych
    $.post(
        '/product/' + id + '/comments/',
        comment
    ).done(function (response) {
        console.log(response);
        var parsedDate = new Date(response.date);
        var date = parsedDate.getUTCDate() + '/' + (parsedDate.getMonth() + 1) + '/' + parsedDate.getFullYear();
        var time = parsedDate.getHours() + ':' + parsedDate.getMinutes();
        newCommentDiv = $('.new');
        $('<div>' + response.comment +
            '<button class="btn btn-default" type="button" style="float: right">' +
            '<span class="glyphicon glyphicon-trash"></span><small>delete</small>' +
            '</button><p>' +
            response.author +
            ', <small>' +
            date + ' ' + time +
            '</small></p></div><hr>').insertBefore(newCommentDiv)
    });
});