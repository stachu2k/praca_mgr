/**
 * Created by Paweł on 05.09.2016.
 * This file contains script for handling semesters in application.
 */

$(document).ready(function(){
    $('#new-semester-form').on("submit", function(event){
        $('#sem-result-box').html("");
        event.preventDefault();
        console.log("form submitted!");
        addNewSemester();
    });
});

$(document).on("pageshow", "#semesters", getSemesters)
    .on("pagehide", "#semesters", cleanSemestersPage)
    .on("pagehide", "#new-semester", cleanNewSemesterPage)
    .on("pagehide", "#sem-properties", cleanSemesterPropertiesPage);

function getSemesters(){
    $.ajax({
        url : "/semesters/",
        type : "GET",
        beforeSend : function(){
            $('#semesters-main').html('<div class="loading">' +
                '<img src="/static/images/ajax-loader.gif" alt="Loading..." ></div>');
        },
        success : function(semesters) {
            var btn = '<a href="#new-semester"' +
                'class="ui-btn ui-icon-plus ui-btn-icon-right ui-corner-all ui-shadow ui-mini">' +
                'Nowy semestr</a>';

            $('#semesters-main').append(btn).trigger("create");

            if(semesters.length) {
                var ul = $('<ul></ul>').attr({
                    "data-role": "listview",
                    "data-inset": "true"
                });

                var li = $('<li data-role="list-divider">Aktywny</li>');
                ul.append(li);

                for (i in semesters) {
                    if (semesters[i].active) {
                        var li = $('<li></li>');
                        var a = $('<a href="#">' +
                            '<h4>' + semesters[i].name + '</h4>' +
                            '<p>Od: ' + semesters[i].start_date + ' | ' +
                            'Do: ' + semesters[i].end_date + '</p>' +
                            '</a>');
                        a.on("click", getSemesterProperties);
                        ul.append(li.append(a));

                        a = $('<a data-id="' + semesters[i].id + '" href="#" data-icon="check">Opcje</a>');
                        ul.append(li.append(a));
                    }
                }

                $('#semesters-main').append(ul).trigger("create");

                ul = $('<ul></ul>').attr({
                    "data-role": "listview",
                    "data-inset": "true"
                });

                li = $('<li data-role="list-divider">Pozostałe</li>');
                ul.append(li);

                for (i in semesters) {
                    if (!semesters[i].active) {
                        li = $('<li></li>');
                        a = $('<a href="#">' +
                            '<h2>' + semesters[i].name + '</h2>' +
                            '<p>Od: ' + semesters[i].start_date + ' | ' +
                            'Do: ' + semesters[i].end_date + '</p>' +
                            '</a>');

                        ul.append(li.append(a));

                        a = $('<a data-id="' + semesters[i].id +
                            '" href="#sem-properties" data-transition="pop" data-icon="gear">Opcje</a>');
                        a.on("click", getSemesterProperties)
                        ul.append(li.append(a));
                    }
                }

                $('#semesters-main').append(ul).trigger("create");
            }
            else {
                var div = $('<div class="no-data-infobox">Brak semestrów w bazie danych</div>');
                $('#semesters-main').append(div).trigger("create");
            }
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        },
        complete : function(){
            $('#semesters-main .loading').remove();
        }
    });
}

function cleanSemestersPage() {
    $('#semesters-main *').remove();
}

function getSemesterProperties() {
    var semesterId = $(this).attr("data-id");

    $.ajax({
        url : "/semesters/properties/",
        type : "GET",
        data : {id : semesterId},
        beforeSend : function(){
            $('#sem-properties-main').html('<div class="loading">' +
                '<img src="/static/images/ajax-loader.gif" alt="Loading..." ></div>');
        },
        success : function(semester) {
            var h2 = $('<h2>' + semester.name + '</h2>');
            var a = $('<a href="#" class="ui-btn ui-btn-inline ui-btn-b ui-shadow ui-corner-all ui-icon-check ui-btn-icon-left ui-btn-inline ui-mini" data-rel="back">Aktywuj</a>');
            var a2 = $('<a href="#" class="ui-btn ui-btn-inline ui-shadow ui-corner-all ui-btn-inline ui-mini" data-rel="back">Usuń</a>');
            $('#sem-properties-main').append(h2).append(a).append(a2).trigger("create");
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        },
        complete : function(){
            $('#sem-properties-main .loading').remove();
        }
    });
}

function cleanSemesterPropertiesPage() {
    $('#sem-properties-main *').remove();
}

function addNewSemester() {
    console.log("addNewSemester is working!") // sanity check

    var sem_type;

    if($('#id_sem_type_0').is( ":checked")) sem_type = 'z';
    else if($('#id_sem_type_1').is( ":checked")) sem_type = 'l';
    else sem_type = 'z';

    $.ajax({
        url : "/semesters/create/",
        type : "POST",
        data : {
            academic_year : $('#id_academic_year').val(),
            sem_type : sem_type,
            start_date : $('#id_start_date').val(),
            end_date : $('#id_end_date').val()
        },
        success : function(json) {
            $('#id_academic_year').val('');
            $('#id_start_date').val('');
            $('#id_end_date').val('');
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            if(json.error == true) $('#sem-result-box').css("color", "red");
            else $('#sem-result-box').css("color", "#47a447");
            $('#sem-result-box').html(json.result);
        },
        error : function(xhr,errmsg,err) {
            $('#sem-result-box').html("Error: " + errmsg); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function cleanNewSemesterPage() {
    $('#sem-result-box').html("");
}