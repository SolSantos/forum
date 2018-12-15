var selected_trash_id = -1;

$(".lixo").click(function () {
    $("#confirm").css("opacity", "1").css("visibility", "visible");
    selected_trash_id = this.id.split("_")[1];
});

function hide_popup(){
    $("#confirm").css("opacity", "0").css("visibility", "hidden");
}

$("#no_button").click(hide_popup);

$("#yes_button").click(function () {
    location.href = "/delete_answer/" + selected_trash_id + "/";
    hide_popup();
});
