/**
 * Created by Paweł on 04.11.2016.
 * This file contains script for handling register in application.
 */

$(document).on('pagebeforeshow', '#register', function() {
    console.log('event register fired.');

    var currDate = new Date();

    for (var i = 0; i < 5; i++) {
        var dayOfWeek;

        switch (currDate.getDay()) {
            case 0:
                dayOfWeek = "niedziela";
                break;
            case 1:
                dayOfWeek = "poniedziałek";
                break;
            case 2:
                dayOfWeek = "wtorek";
                break;
            case 3:
                dayOfWeek = "środa";
                break;
            case 4:
                dayOfWeek = "czwartek";
                break;
            case 5:
                dayOfWeek = "piątek";
                break;
            case 6:
                dayOfWeek = "sobota";
        }

        var month = currDate.getMonth() + 1;
        var day = currDate.getDate();

        var output = (day < 10 ? '0' : '') + day + '.' +
            (month < 10 ? '0' : '') + month + '.' +
            currDate.getFullYear();

        var content = $('<div class="col" data-date="' + output + '">\
                <div class="cell"><span>' + output + '<br>' + dayOfWeek + '</span></div>\
                <div class="cell" data-time="7:30"></div>\
                <div class="cell" data-time="8:20"></div>\
                <div class="cell" data-time="9:15"></div>\
                <div class="cell" data-time="10:05"></div>\
                <div class="cell" data-time="11:00"></div>\
                <div class="cell" data-time="11:55"></div>\
                <div class="cell" data-time="12:50"></div>\
                <div class="cell" data-time="13:45"></div>\
                <div class="cell" data-time="14:40"></div>\
                <div class="cell" data-time="15:30"></div>\
                <div class="cell" data-time="16:20"></div>\
                <div class="cell" data-time="17:15"></div>\
                <div class="cell" data-time="18:05"></div>\
                <div class="cell" data-time="19:00"></div>\
                <div class="cell" data-time="19:55"></div>\
            </div>');

        content.appendTo($('.table.clearfix'));

        currDate.setTime(currDate.getTime() + 86400000);
    }
});