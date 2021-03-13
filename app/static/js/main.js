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

$(document).ready(function () {

    loadPlayerNames();

});