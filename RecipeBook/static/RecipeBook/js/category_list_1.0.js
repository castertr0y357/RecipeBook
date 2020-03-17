$(document).ready(function(){
    $('.th').click(function(){
        let sort, asc, tableID, th_id;
        sort = $(this).attr("data-sort");
        asc = $(this).attr("data-asc");
        tableID = $(this).parents("table").attr("id");
        th_id = $(this);
        $.ajax({
            type: 'GET',
            url: url,
            data:{sorting_method: sort, ascending: asc},
            dataType: 'json',
            success: function (data) {
                replaceTableContents(tableID, data);
                if(asc === "true"){
                    $(th_id).attr("data-asc", "false");
                    $(th_id).find('span').text('/\\');
                } else {
                    $(th_id).attr("data-asc", "true");
                    $(th_id).find('span').text('\\/');
                }
            },
            error: function(){
                alert("Failed to query the database for ordering")
            }
        })
    });
});
function replaceTableContents(table, data) {
    table = $("#" + table);
    console.log(data);
    let body = table.find('tbody');
    body.empty();
    $.each(data, function (index, element) {
        console.log(element);
        body.append($('<tr>')
            .append('<td>' + element.name + '</td>')
            .append($('<td>')
                .text(element.recipe_count))
        );
    });
}