/**
 * Created by Paweł on 14.01.2017.
 * This file contains script for handling classes in application.
 */

function editTopic(obj, classesdate) {
    var $this = $(obj);
    var $form = $('#edit_topic_form');
    $form.attr('action', '/ajax/edit_topic/' + classesdate + '/');
    $form.find('textarea').val($this.html());
    $('#edit_topic').popup("open");
}

function editComment(obj, classesdate) {
    var $this = $(obj);
    var $form = $('#edit_comment_form');
    $form.attr('action', '/ajax/edit_comment/' + classesdate + '/');
    $form.find('textarea').val($this.html());
    $('#edit_comment').popup("open");
}

function refreshTopicTable() {
    $('table#topic_comment_table tbody').empty();

    $.ajax({
        url      : '/ajax/get_topictable/',
        type     : 'get',
        data     : {'classes_id': $('table#topic_comment_table').data('classes')},
        dataType : 'json'
    })
        .done(function(data) {
            var tbody = $('table#topic_comment_table');
            for (var i in data) {
                tbody.append('<tr><td style="width: 10%;">' + data[i].date + '</td><td onclick="editTopic(this, ' + data[i].id + ')" style="width: 45%;">' + data[i].topic + '</td><td onclick="editComment(this, ' + data[i].id + ')" style="width: 45%;">'+ data[i].comment + '</td></tr>');
            }
        });
}

$(document).on('submit', '#edit_topic_form', function(event) {
    event.preventDefault();

    var $form = $('#edit_topic_form');
    var formData = {
        'csrfmiddlewaretoken' : $form.find('input[name=csrfmiddlewaretoken]').val(),
        'value'               : $form.find('textarea[name=value]').val()
    };

    $.ajax({
        url      : $form.attr('action'),
        type     : 'post',
        data     : formData,
        dataType : 'html'
    })
        .done(function(msg) {
            if(msg == "success")
                $('#edit_topic').popup("close");
                refreshTopicTable()
        });
});

$(document).on('submit', '#edit_comment_form', function(event) {
    event.preventDefault();

    var $form = $('#edit_comment_form');
    var formData = {
        'csrfmiddlewaretoken' : $form.find('input[name=csrfmiddlewaretoken]').val(),
        'value'               : $form.find('textarea[name=value]').val()
    };

    $.ajax({
        url      : $form.attr('action'),
        type     : 'post',
        data     : formData,
        dataType : 'html'
    })
        .done(function(msg) {
            if(msg == "success")
                $('#edit_comment').popup("close");
                refreshTopicTable()
        });
});

/*************************************************************************************************/

function checkPresence(classesdate) {
    $('#check_presence_form').attr('action', '/ajax/check_presence/' + classesdate + '/');
    $('#check_presence').popup("open");
}

$(document).on("pageshow", "#classes", function() {
   $('#id_all_present').click(function(event) {
       $('input[name=students]').each(function() {
           $(this).prop("checked", true).checkboxradio('refresh');
       });
   });
   $('#id_all_absent').click(function(event) {
        $('input[name=students]').each(function() {
           $(this).prop("checked", false).checkboxradio('refresh');
       });
   });
   $('#id_no_classes').click(function(event) {
       if($(this).prop("checked")) {
           $('input[name=students]').each(function() {
               $(this).prop("checked", false).checkboxradio('refresh');
               $(this).checkboxradio("disable");
           });
       } else {
           $('input[name=students]').each(function() {
               $(this).checkboxradio("enable");
           });
       }
   });
});

$(document).on('submit', '#check_presence_form', function(event) {
    event.preventDefault();

    var $form = $('#check_presence_form');
    var studentList = document.getElementsByName("students");
    var checkedStudents = [];
    for(var i = 0; i < studentList.length; i++) {
        if (studentList.item(i).checked)
            checkedStudents.push(studentList.item(i).value)
    }
    var formData = {
        'csrfmiddlewaretoken'   : $form.find('input[name=csrfmiddlewaretoken]').val(),
        'no_classes'            : $form.find('input[name=no_classes]:checked').val(),
        'students'              : checkedStudents
    };

    $.ajax({
        url      : $form.attr('action'),
        type     : 'post',
        data     : formData,
        dataType : 'html',
        traditional : true
    })
        .done(function(msg) {
            if(msg == "success")
                $('#check_presence').popup("close");
                refreshPresenceTable();
        });
});

function editPresence(obj, studentId, classesdateId) {
    var $textarea = $(obj).find("textarea").first();
    $('#edit_presence_form').attr('action', '/ajax/edit_presence/date' + classesdateId + '/student' + studentId + '/');
    $('#edit_presence_form textarea').val($textarea.html());
    $('#edit_presence').popup("open");
}

$(document).on('submit', '#edit_presence_form', function(event) {
    event.preventDefault();

    var $form = $('#edit_presence_form');
    var formData = {
        'csrfmiddlewaretoken'   : $form.find('input[name=csrfmiddlewaretoken]').val(),
        'presence'              : $form.find('input[name=presence]:checked').val(),
        'note'                  : $form.find('textarea').val()
    };

    $.ajax({
        url      : $form.attr('action'),
        type     : 'post',
        data     : formData,
        dataType : 'html'
    })
        .done(function(msg) {
            if(msg == "success")
                $('#edit_presence').popup("close");
                refreshPresenceTable();
        });
});

function refreshPresenceTable() {
    $('table#id_presence_table tbody').empty();

    $.ajax({
        url      : '/ajax/get_presencetable/',
        type     : 'get',
        data     : {'classes_id': $('table#id_presence_table').data('classes')},
        dataType : 'html'
    })
        .done(function(html_code) {
            var tbody = $('table#id_presence_table');
            tbody.append(html_code);
        });
}