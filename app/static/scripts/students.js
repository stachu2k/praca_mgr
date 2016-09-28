/**
 * Created by Paweł on 30.08.2016.
 * This file contains script for handling students in application.
 */

$(document).on("pageshow", "#students", function(){
    $.ajax({
        url : "/students/",
        type : "GET",
        beforeSend : function(){
            $('#students-main').html('<div class="loading">' +
                '<img src="/static/images/ajax-loader.gif" alt="Loading..." ></div>');
        },
        success : function(students) {
            var btn = '<a href="#new-student"' +
                'class="ui-btn ui-icon-plus ui-btn-icon-right ui-corner-all ui-shadow ui-mini">' +
                'Dodaj studenta</a>';
            $('#students-main').append(btn).trigger("create");

            var form = $('<form></form>').addClass("ui-filterable");
            var input = $('<input>').attr({"id":"filter", "data-type":"search"});
            $('#students-main').append(form.append(input)).trigger("create");

            var ul = $('<ul></ul>').attr({
                "data-role":"listview",
                "data-inset":"true",
                "data-autodividers":"true",
                "data-filter":"true",
                "data-input":"#filter"
            });
            for(i in students)
            {
                var li = $('<li></li>');
                var a = $('<a data-id="' + students[i].id + '" href="#student-details">' +
                    students[i].surname + " " + students[i].name + '</a>');
                a.on("click", getStudentDetails);
                ul.append(li.append(a));
            }
            $('#students-main').append(ul).trigger("create");
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        },
        complete : function(){
            $('#students-main .loading').remove();
        }
    });
});

$(document).ready(function(){
    $('#new-student-form').on("submit", function(event){
        $('#std-result-box').html("");
        event.preventDefault();
        console.log("form submitted!");
        addNewStudent();
    });
});

$(document).on("pagehide", "#students", function(){
    $('#students-main *').remove();
});

$(document).on("pagehide", "#new-student", function(){
    $('#std-result-box').html("");
});

function addNewStudent(){
    console.log("newStudentFormPost is working!") // sanity check
    $.ajax({
        url : "/students/create/",
        type : "POST",
        data : {name : $('#id_name').val(), surname : $('#id_surname').val()},
        success : function(json) {
            $('#id_name').val(''); // remove the value from the input
            $('#id_surname').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            if(json.error == true) $('#std-result-box').css("color", "red");
            else $('#std-result-box').css("color", "#47a447");
            $('#std-result-box').html(json.result);
        },
        error : function(xhr,errmsg,err) {
            $('#std-result-box').html("Error: " + errmsg); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function getStudentDetails() {

   var studentId = $(this).attr("data-id");

   $.ajax({
        url : "/students/details/",
        type : "GET",
        data : {id : studentId},
        beforeSend : function(){
            $('#student-details-main').html('<div class="loading">' +
                '<img src="/static/images/ajax-loader.gif" alt="Loading..." ></div>');
        },
        success : function(student) {
            var h2 = $('<h2>' + student.name + ' ' + student.surname + '</h2>');
            $('#student-details-main').append(h2).trigger("create");
        },
       error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        },
        complete : function(){
            $('#student-details-main .loading').remove();
        }
    });
}