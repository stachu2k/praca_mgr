/**
 * Created by Paweł on 14.01.2017.
 * This file contains script for handling classes in application.
 */

function editTopic(obj, classesdate) {

    var $this = $(obj);
    $('#edit_topic_form').attr('action', '/ajax/edit_topic/' + classesdate + '/');
    $('#edit_topic_form textarea').val($this.html());
    $('#edit_topic').popup("open");

}

function editComment(obj, classesdate) {

    var $this = $(obj);
    $('#edit_comment_form').attr('action', '/ajax/edit_comment/' + classesdate + '/');
    $('#edit_comment_form textarea').val($this.html());
    $('#edit_comment').popup("open");

}

function refreshTopicTable() {

    $('table.topic-table tbody').empty();

    $.ajax({
        url      : '/ajax/get_topictable/',
        type     : 'get',
        data     : {'classes_id': $('table.topic-table').data('classes')},
        dataType : 'json'
    })
        .done(function(data) {

            var tbody = $('table.topic-table tbody');
            for (var i in data) {
                tbody.append('<tr><td style="width: 10%;">' + data[i].date + '</td><td onclick="editTopic(this, ' + data[i].id + ')" style="width: 45%;">' + data[i].topic + '</td><td onclick="editComment(this, ' + data[i].id + ')" style="width: 45%;">'+ data[i].comment + '</td></tr>');
            }

        });

}

function submitForm(form ,formData, popupObj) {

    $.ajax({
        url      : $(form).attr('action'),
        type     : 'post',
        data     : formData,
        dataType : 'html'
    })
        .done(function(msg) {
            if(msg == "success")
                $(popupObj).popup("close");
                refreshTopicTable()
        });

}

$(document).on('submit', '#edit_topic_form', function(event) {

    event.preventDefault();

    var $edit_topic = $('#edit_topic');
    var $form = $('#edit_topic_form');
    var formData = {
        'csrfmiddlewaretoken' : $('#edit_topic_form input[name=csrfmiddlewaretoken]').val(),
        'value'               : $('#edit_topic_form textarea[name=value]').val()
    };

    submitForm($form, formData, $edit_topic);

});

$(document).on('submit', '#edit_comment_form', function(event) {

    event.preventDefault();

    var $edit_comment = $('#edit_comment');
    var $form = $('#edit_comment_form');
    var formData = {
        'csrfmiddlewaretoken' : $('#edit_comment_form input[name=csrfmiddlewaretoken]').val(),
        'value'               : $('#edit_comment_form textarea[name=value]').val()
    };

    submitForm($form, formData, $edit_comment);

});