function loadPlayerNames(){

    $.get(
        "/players",
        function (data, success) {
            const list = data.map((i) => { return { label: i.player_name } });
            $('#player').autocomplete({
                source: list,
                select: function (event, ui) { player = ui.item.label; }
            });
            $('#bowler').autocomplete({
                source: list,
                select: function (event, ui) { bowler = ui.item.label; }
            });
            $('#batsman').autocomplete({
                source: list,
                select: function (event, ui) { batsman = ui.item.label; }
            });
            $('#non_striker').autocomplete({
                source: list,
                select: function (event, ui) { non_striker = ui.item.label; }
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
            $('#team1').autocomplete({
                source: list,
                select: function (event, ui) { team = ui.item.label; }
            });
            $('#team2').autocomplete({
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

function getMatchDetails(){

    $('#match-info').empty();
    const inputs = $('#update_match_details :input');
    const form_data = {};
    inputs.each(function () {
        form_data[this.id] = $(this).val();
    });
    const match_id = form_data['matchid'];

    $.get(
        "/matchDetails/" + match_id,
        function (data, success) {
            $('#match-info').addClass('alert-success').text(JSON.stringify(data));
        }
    );

}

function updateMatchDetails(){

    $('#match-info').empty();
    
    $('#bt_update_match_details').text("Updating... Please wait");
    $('#bt_update_match_details').prop( "disabled", true);

    const inputs = $('#update_match_details :input');
    const form_data = {};
    inputs.each(function () {
        form_data[this.id] = $(this).val();
    });
    if($('#isActiveMatch').prop('checked') === true){
        form_data['isActiveMatch'] = 'true'
    }
    else{
        form_data['isActiveMatch'] = 'false'
    }
    const post_data = form_data;
    console.log(post_data);

    $.ajaxSetup({
        headers: {
            'Content-Type': 'application/json'
        }
    });

    $.post("matchDetails",
        JSON.stringify(post_data))
        .done(function (data) {
            msgtxt = "Updated";
            $('#match-info').addClass('alert-success').text(msgtxt);
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
            //console.log({ status: textStatus, error_message: jqXHR.responseText });
            //const msgData = JSON.parse(jqXHR.responseText);
            $('#match-info').addClass('alert-danger').text(jqXHR.responseText);
        })
        .always(function () {
            $('#bt_update_match_details').text("Update");
            $('#bt_update_match_details').prop( "disabled", false);
        });
}

function updateMatchResult(){

    $('#match-result-info').empty();
    
    $('#bt_update_match_result').text("Updating... Please wait");
    $('#bt_update_match_result').prop( "disabled", true);

    const inputs = $('#update_match_result :input');
    const form_data = {};
    inputs.each(function () {
        form_data[this.id] = $(this).val();
    });
    if($('#matchWon').prop('checked') === true){
        form_data['result'] = 'Won'
    }
    else{
        form_data['result'] = 'Lost'
    }
    const post_data = form_data;
    console.log(post_data);

    $.ajaxSetup({
        headers: {
            'Content-Type': 'application/json'
        }
    });

    $.post("matchFinalOverDetails",
        JSON.stringify(post_data))
        .done(function (data) {
            msgtxt = "Updated";
            $('#match-result-info').addClass('alert-success').text(msgtxt);
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
            //console.log({ status: textStatus, error_message: jqXHR.responseText });
            //const msgData = JSON.parse(jqXHR.responseText);
            $('#match-result-info').addClass('alert-danger').text(jqXHR.responseText);
        })
        .always(function () {
            $('#bt_update_match_result').text("Update");
            $('#bt_update_match_result').prop( "disabled", false);
        });
}

function updateMatchPrediction(){

    $('#match-result-info').empty();
    $('#bt_update_match_prediction').text("Updating... Please wait");
    $('#bt_update_match_prediction').prop( "disabled", true);

    const inputs = $('#update_match_result :input');
    const form_data = {};
    inputs.each(function () {
        form_data[this.id] = $(this).val();
    });
    const match_id = form_data['matchid'];

    $.post("updatePredictedResult/" + match_id,
        "")
        .done(function (data) {
            $('#match-result-info').addClass('alert-success').text(data);
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
            $('#match-result-info').addClass('alert-success').text(jqXHR.responseText);
        })
        .always(function () {
            $('#bt_update_match_prediction').text("Update Prediction");
            $('#bt_update_match_prediction').prop( "disabled", false);
        });
}

$(document).ready(function () {

    loadPlayerNames();
    loadTeamNames();

});