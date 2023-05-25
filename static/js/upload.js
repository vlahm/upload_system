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

    return JSON.stringify(userMatches);
}

// # inject input of scraped data
window.onload = function() {
    $("#userCols").submit( function(eventObj) {
        var selections = $('#userCols td[name=cols_matches] select');
        var inputs = $('#userCols td[name=cols_input]');

        for (let i = 0; i < selections.length; i++) {

            var selected_col = selections[i].value
            var old_col = inputs[i].innerText

            $("<input />").attr("type", "hidden")
                .attr("name", old_col)
                .attr("value", selected_col)
                .appendTo("#userCols");
        }
    });
};
