$(function() {
    $("#notes_list_ul a").click(function(){
        var url = $(this).attr("href");
        $("div.span6").load(url + '/ajax');
        history.pushState({id: 'NOTE_ID'}, '', url); 
        return false;
    });
    $(".note_text_area").click(function(){
        $("div.span6").load("{% url edit_note%}{{ note_id }}");
        return false;

})
