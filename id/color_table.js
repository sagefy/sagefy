(function() {

    var table = [[], [], [], [], [], []], i = 1, j = 0, str = "";

    [20, 43, 66, 90, 95, 99].forEach(function(light) {
        table[0][j] = $.husl.p.toHex(9, 10, light);
        j++;
    });

    [9, 81, 153, 225, 297].forEach(function(hue) {
        j = 0;
        [20, 43, 66, 90, 95, 99].forEach(function(light) {
            table[i][j] = $.husl.p.toHex(hue, 100, light);
            j++;
        });
        i++;
    });

    table.forEach(function(hue) {
        hue.forEach(function(hex) {
            str += hex + ",";
        });
        str += "\n";
    });

    return str;

})();