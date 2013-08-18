(function() {

    var table = [[], [], [], [], []], i = 0, j = 0, str = "";

    [9, 81, 153, 225, 297].forEach(function(hue) {
        j = 0;
        [20, 43, 66, 90, 95, 99].forEach(function(light) {
            table[i][j] = $.husl.p.toHex(hue, 100, light);
            j++;
        });
        i++;
    });

    table.forEach(function(hue) {
        str += "<tr>\n<td> X &deg;</td>\n";
        hue.forEach(function(hex) {
            str += "<td style=\"background:" + hex + "\"></td>\n";
        });
        str += "</tr>\n";
    });

    return str;

})();