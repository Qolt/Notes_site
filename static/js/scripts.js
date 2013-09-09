$(function() {
    $("#notes_list_ul a").click(function(){
        var url = $(this).attr("href");
        $("div.span6").load(url + '/ajax');
        history.pushState({id: 'NOTE_ID'}, '', url); 
        return false;
    });
    $("#create_note_button").click(function(){
        var url = $(this).attr("action");
        $("div.span6").load(url);
        return false;
    });
})