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
            data:{sorting_method: sort, ascending: asc, name: name},
            dataType: 'json',
            success: function (data) {
                replaceTableContents(tableID, data);
                $('#'+tableID).find('thead').each(function () {
                    console.log($(this));
                    $(this).find('tr').each(function () {
                        $(this).find('th').each(function () {
                            if($(this).is(th_id)) {
                                //Leave element unaffected
                            } else {
                                $(this).attr("data-asc", "true");
                                $(this).find('span').text('');
                            }
                        });
                    });
                });
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
                .text(element.servings))
            .append($('<td>')
                .text(element.time))
            .append('<td>' + element.source + '</td>')
        );
    });
}