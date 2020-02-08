

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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var csrftoken = getCookie('csrftoken');

$(document).ready(function(){
    var ok = 0;
    var notOk = 0;



    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    $('body').on('click', '.list-group a.list-group-item', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var url = $(this).attr('href');
        var otv = $(this).data('id');
        var vop = $('a.nextVopros.first').attr('data-id');
        console.log(vop);

        if($(this).attr('data-approved') === 'True' || $(this).attr('data-approved') === 'true'){
            $(this).removeClass('list-group-item-success').addClass('list-group-item-success')
            ok ++;
            answerInQuestion(vop, otv, url, 1);
            // console.log('Ok:' + ok);
        }else{
            $(this).removeClass('list-group-item-danger').addClass('list-group-item-danger')
            notOk ++;
            answerInQuestion(vop, otv, url, 0);
        }
        $('div.list-group').removeClass('disabled').addClass('disabled');
    });


     $('body').on('click', 'a.nextVopros', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var url = $(this).attr('href');
        var id = $(this).data('next');
        var count = $(this).attr('data-i');

        // var vop = $('a.nextVopros').data('id');
         $(this).attr('data-id', '').attr('data-next', '').attr('data-i', '');

         if (!$("div.list-group").hasClass("disabled")) {
             alert('Выберите ответ');
         } else {

                 $.ajax({
                     type: 'POST',
                     url: url,
                     data: {
                         'csrfmiddlewaretoken': csrftoken,
                         'id': id,
                         'count': count,
                     },
                     // dataType: 'json',
                     success: function (data) {

                            console.log(data.count, data.total, data.flag);
                            if (data.flag != 1) {


                                // console.log(data.questions_list);
                                // console.log(JSON.parse(data.answers));
                                $('#count').text(data.count);
                                $('h4.alert-heading').text(data.questions_list);


                                var answers = JSON.parse(data.answers);

                                $('div.answers').remove();
                                // $('a.first').remove();

                                var html = '<div class="row mb-5 answers"><div class="list-group w-100 ">';

                                for (i = 0; i < answers.length; i++) {
                                    html += '<a type="button" class="list-group-item list-group-item-action" data-id="' + answers[i].pk + '"\
                                         data-approved="' + answers[i].fields.approved + '" href="/questionajax/">' + answers[i].fields.description + '</a>';
                                }

                                html += '</div></div>';

                                $('div.question').after(html);

                                $('a.nextVopros').attr('data-i', data.count).attr('data-id', data.id).attr('data-next', data.next);
                            }else{
                                $('h1.cover-heading>span').remove();
                                $('div.question').remove();
                                $('div.answers').remove();
                                $('a.nextVopros').remove();
                                $('h1.cover-heading').text('Результат Вашего теста:')


                                console.log(data)


                                var result = JSON.parse(data.list_not_ok_questions);

                                console.log(result)
                                var html = '<div class="row mb-5"><div class="list-group w-100 ">'
                            }
                     }
                 });
            //  }else{
            //     $('h1.cover-heading>span').remove();
			// 	$('div.question').remove();
			// 	$('div.answers').remove();
			// 	$('a.nextVopros').remove();
			// 	$('h1.cover-heading').text('Результат Вашего теста:');
            // }
         }

     });



});


function answerInQuestion(vop, otv, url, correct) {
    var data = {};
    data.correct = correct;
    data.vop = vop;
    data.otv = otv;
    data.csrfmiddlewaretoken = csrftoken;
    console.log(data);
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        success: function (data) {
            // console.log('Все ок');
            // console.log('Все ok_vop:', data.ok_vop);
            // console.log('Все ok_otv:', data.ok_otv);
            // console.log('Все not_ok_vop:', data.not_ok_vop);
            // console.log('Все not_ok_otv:', data.not_ok_otv);
        }
    });
}

