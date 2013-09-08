{% extends "snippets/base.js" %}
{% load media %}

{% block script %}
function init() {
    $('div.nojs').hide();
    $('div.content').show();
    $('.stars').stars({
        inputType: "select",
        callback: toggle_comments
    });
    $('#submit_survey').click(function() {
        $('#survey_form').submit();
    });
}

function toggle_comments(ui, type, value, event) {
    var speed = 'fast';
    var elem = $('#' + $(event.target).parent().siblings('input').filter(':first').attr('name').replace('answer', 'comm'));
    value <= COMMENT_FROM && value > 0 ? elem.slideDown(speed) : elem.slideUp(speed);
}
{% endblock %}
