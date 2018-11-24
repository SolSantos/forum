var click = 0;

$("#abrirPergunta").click(function () {
    if (click == 0){
        $("#abrirPergunta").attr("src", "/static/forum/images/close.png");
        $("#fazerPergunta").css("height", "390px");
        $("#inputBox").css("opacity", "1").css("visibility", "visible");
        click = 1;
    } else{
        $("#abrirPergunta").attr("src", "/static/forum/images/more.png");
        $("#fazerPergunta").css("height", "55px");
        $("#inputBox").css("opacity", "0").css("visibility", "hidden");
        click = 0;
    }
});

$("#submit").click(function () {
    $("#abrirPergunta").attr("src", "/static/forum/images/more.png");
    $("#fazerPergunta").css("height", "55px");
    $("#inputBox").css("opacity", "0").css("visibility", "hidden");
    click = 0;

});