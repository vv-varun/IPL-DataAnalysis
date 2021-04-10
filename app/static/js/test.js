function loadPlayerNames(){

    $.get(
        "/players",
        function (data, success) {
            const list = data.map((i) => { return { label: i.player_name } });
            $('#player').autocomplete({
                source: list,
                select: function (event, ui) { player = ui.item.label; }
            });
        }
    );

}

function loadTeamNames(){
    $.get(
        "/teams",
        function (data, success) {
            const list = data.map((i) => { return { label: i.team_name } });
            $('#team').autocomplete({
                source: list,
                select: function (event, ui) { team = ui.item.label; }
            });
        }
    );
}

function updateTeamAssignment(){
    
    $('#message-bar').empty();
    $('#message-bar').removeClass("alert-danger");
    $('#message-bar').removeClass("alert-success");

    $('#update_team_assignment').text("Updating... Please wait");
    $('#update_team_assignment').prop( "disabled", true);

    const inputs = $('#player_team_assignment :input');
    const form_data = {};
    inputs.each(function () {
        form_data[this.id] = $(this).val();
    });
    const post_data = form_data;
    //console.log(post_data);

    $.ajaxSetup({
        headers: {
            'Content-Type': 'application/json'
        }
    });

    $.post("updateTeamAssignments",
        JSON.stringify(post_data))
        .done(function (data) {
            msgtxt = "Updated";
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
            //console.log({ status: textStatus, error_message: jqXHR.responseText });
            //const msgData = JSON.parse(jqXHR.responseText);
            $('#message-bar').addClass('alert-danger').text(jqXHR.responseText);
        })
        .always(function () {
            $('#update_team_assignment').text("Update");
            $('#update_team_assignment').prop( "disabled", false);
        });
}

$(document).ready(function () {

    loadPlayerNames();
    loadTeamNames();

});