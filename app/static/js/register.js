/**
 * Created by Paweł on 04.11.2016.
 * This file contains script for handling register in application.
 */

$(document).on('pagebeforeshow', '#register', function() {
    var today = new Date(2017, 1, 27);
    $('span.title').html("Dziś jest " + getDayOfWeek(today) + " " + getFormattedDate(today));
    createRegister(today);
});

$(document).on('pagehide', '#register', function() {
    $('.table.clearfix').html('');
});

function createRegister(date) {

    var currDate = date;

    for (var i = 0; i < 5; i++) {
        var dayOfWeek = getDayOfWeek(currDate);

        var output = getFormattedDate(currDate);

        var col = $('<div class="col" data-date="' + output + '"></div>');
        var cell = $('<div class="cell"><span>' + output + '<br>' + dayOfWeek + '</span></div>');
        cell.appendTo(col);

        var classes = getClasses(output);

        for(var c in classes) {
            cell = $('<div class="cell"></div>');
            var classesbox = $('<a href="/groups/' + classes[c].id + '/classes" class="classes classes-' +
                classes[c].classes_type + '">' + classes[c].start_time + '-' +
                classes[c].end_time + ' ' + classes[c].classes_type + '<br>' + classes[c].subject + '<br>' +
                classes[c].short_name + '</a>');
            col.append(cell.append(classesbox));
        }

        col.appendTo($('.table.clearfix'));

        currDate.setTime(currDate.getTime() + 86400000);
    }
}

function getDayOfWeek(date) {
    switch (date.getDay()) {
            case 0:
                return "niedziela";
                break;
            case 1:
                return "poniedziałek";
                break;
            case 2:
                return "wtorek";
                break;
            case 3:
                return "środa";
                break;
            case 4:
                return "czwartek";
                break;
            case 5:
                return "piątek";
                break;
            case 6:
                return "sobota";
        }
}

function getFormattedDate(date) {
    var month = date.getMonth() + 1;
    var day = date.getDate();

    return (day < 10 ? '0' : '') + day + '.' +
        (month < 10 ? '0' : '') + month + '.' +
        date.getFullYear();
}

function getClasses(date) {
    var ret;
    $.ajax({
        url : "/ajax/get_classes/",
        type : "GET",
        data : {date : date},
        async : false,
        success : function(data) {
            ret = data;
        }
    });
    return ret;
}

function loadNext(event) {
    event.preventDefault();

    var lastdate = $('.table.clearfix').children(":visible").last().data("date");
    var lastdate_array = lastdate.split(".");
    var nextdate = new Date(parseInt(lastdate_array[2]), parseInt(lastdate_array[1]) - 1, parseInt(lastdate_array[0]) + 1);
    $('.table.clearfix').html('');
    createRegister(nextdate);
}

function loadPrev(event) {
    event.preventDefault();

    var visiblecols = $('.table.clearfix').children(":visible");
    var firstdate = visiblecols.first().data("date");
    var firstdate_array = firstdate.split(".");
    var prevdate = new Date(parseInt(firstdate_array[2]), parseInt(firstdate_array[1]) - 1, parseInt(firstdate_array[0]) - visiblecols.length);
    $('.table.clearfix').html('');
    createRegister(prevdate);
}