
function setup_csrf() {
    // CSRF TOKEN stuff is foregin to me...
    //  most ajax code taken from this thread: https://groups.google.com/d/msg/otree/nUrvTTAu6QA/4DHiw8_zBQAJ
    var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        data: {csrfmiddlewaretoken: csrftoken}
    });
}

var get_metadata = function(data_holder){
    return {
        player_id_in_group: data_holder.attr("data-player-id"),
        group_id: data_holder.attr("data-group-id"),
        session_id: data_holder.attr("data-session-id"),
        subsession_id: data_holder.attr("data-subsession-id"),
        example: data_holder.attr("data-example"),
    };
};
