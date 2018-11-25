//Ajusta altura da div da coruja para não cortar a caixa do login quando esta é maior que a altura da janela.

var heightAdjust = function () {
    if($(window).width() > 992) {
        if($("#areaRight").height() > $(window).height()) {
            $("#areaLeft").css("height", $("#areaRight").height());
            console.log("hey");
        } else {
            $("#areaLeft").css("height", "100vh");
        }
    } else {
        $("#areaLeft").css("height", "auto");
    }
};

window.addEventListener('resize', heightAdjust, true);