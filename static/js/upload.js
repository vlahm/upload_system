function Convert() {
    var table = document.getElementById("tblUserCols");
    var header = [];
    var rows = [];

    for (var i = 0; i < table.rows.length; i++) {
        header.push(table.rows[i].cells[i].innerHTML);
    }

    for (var i = 1; i < table.rows.length; i++) {
        var row = {};
        for (var j = 0; j < table.rows[i].cells.length; j++) {
            row[header[j]] = table.rows[i].cells[j].innerHTML;
        }
        rows.push(row);
    }

    alert(JSON.stringify(rows));
}

function userColsConvert() {
    var table = document.getElementById("tblUserCols");
    var userMatches = {};

    for (var i = 1; i < table.rows.length; i++) {
        // key: user-input column name
        col = table.rows[i].cells[0].innerHTML

        // value: user-selected match
        sel = table.rows[i].cells[1].children[0]
        sel_index = sel.selectedIndex
        selection = sel[sel_index].text

        userMatches[col] = selection
    }

    // Ajax Monstrosity
    $.ajax({
        type: 'POST',
        url:'/_colToVar',
        data: JSON.stringify(userMatches),
        contentType: 'application/json;charset=UTF-8',

        success: function() {
            console.log("nailed it!");
        error: function(error){
            console.log(error);
    });

    return JSON.stringify(userMatches);
}
