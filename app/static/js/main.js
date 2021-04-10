function loadPlayerNames(){

    $.get(
        "/players",
        function (data, success) {
            const list = data.map((i) => { return { label: i.player_name } });
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

function loadCurrentMatchPlayerNames(){

    $.get(
        "/currentMatchPlayers/batting",
        function (data, success) {
            const list = data.map((i) => { return { label: i } });
            $('#cm_batsman').autocomplete({
                source: list,
                select: function (event, ui) { cm_batsman = ui.item.label; }
            });
            $('#cm_non_striker').autocomplete({
                source: list,
                select: function (event, ui) { cm_non_striker = ui.item.label; }
            });
        }
    );

}


function predictMatchResult(){
    
    $('#message-bar').empty();
    $('#message-bar').removeClass("alert-danger");
    $('#message-bar').removeClass("alert-success");

    $('#predict_match_result').text("Calculating... Please wait");
    $('#predict_match_result').prop( "disabled", true);

    const inputs = $('#match_details :input');
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

    $.post("predictMatchResult",
        JSON.stringify(post_data))
        .done(function (data) {
            msgtxt = "Your chances of defending this score in the final over are: " + data.win_probability  + "%";
            if(data.result === 'Lost'){
                $('#message-bar').addClass('alert-danger').text(msgtxt);
            }
            else{
                $('#message-bar').addClass('alert-success').text(msgtxt);
            }
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
            //console.log({ status: textStatus, error_message: jqXHR.responseText });
            //const msgData = JSON.parse(jqXHR.responseText);
            $('#message-bar').addClass('alert-danger').text(jqXHR.responseText);
        })
        .always(function () {
            $('#predict_match_result').text("Calculate");
            $('#predict_match_result').prop( "disabled", false);
        });
}

function predictCurrentMatchResult(){
    
    $('#cm-prediction-result').empty();
    $('#predict_current_match_result').text("Calculating... Please wait");
    $('#predict_current_match_result').prop( "disabled", true);

    const inputs = $('#current_match_details :input');
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

    $.post("currentMatchPrediction",
        JSON.stringify(post_data))
        .done(function (data) {
            console.log(data);
            result_text = '<li class="list-group-item list-group-item-primary">Chances of defending this score per bowler:</li>'
            $('#cm-prediction-result').append(result_text);
            data.forEach(res => {
                if(res.result === 'Lost'){
                    result_text = '<li class="list-group-item list-group-item-danger">'
                }
                else{
                    result_text = '<li class="list-group-item list-group-item-success">'
                }
                result_text += "Chances of defending this score by <strong>" + res.player 
                                + "</strong> are: " + res.win_probability + "%</li>";
                $('#cm-prediction-result').append(result_text);
            });
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
            //const msgData = JSON.parse(jqXHR.responseText);
            $('#cm_message-bar').addClass('alert-danger').text(jqXHR.responseText);
        })
        .always(function () {
            $('#predict_current_match_result').text("Calculate");
            $('#predict_current_match_result').prop( "disabled", false);
        });
}

$(document).ready(function () {

    loadPlayerNames();
    loadCurrentMatchPlayerNames();

});