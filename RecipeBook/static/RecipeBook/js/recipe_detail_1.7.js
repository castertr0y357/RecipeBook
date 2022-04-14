$(document).ready(function(){
    $("input[type='button']").click(function(){
        console.log("clicked submit")
        let value, ingredients, func;
        func = 'resize'
        value = $("input[name='default_recipe_sizes']:checked").val();
        console.log(value)
        ingredients = $("#ingredients_ul")
        $.ajax({
            type: 'GET',
            url: url,
            data:{resize_value: value, function_type: func},
            dataType: 'json',
            success: function (data) {
                replaceIngredients(ingredients, data);
            },
            error: function(xhr, status, error) {
                let errorMessage = xhr.status + ': ' + xhr.statusText
                console.log('Error - ' + errorMessage)
                alert("Failed to resize ingredients.  Please check browser console (F12) for errors")
            }
        })
    });
    $("#recipe_sizing_reset").click(function (){
        console.log("clicked reset")
        let ingredients, func;
        func = 'reset'
        ingredients = $("#ingredients_ul")
        $.ajax({
            type: 'GET',
            url: url,
            data:{function_type: func},
            dataType: 'json',
            success: function (data) {
                replaceIngredients(ingredients, data);
            },
            error: function() {
                alert("Failed to resize ingredients.  Please check browser console (F12) for errors")
            }
        })
    });
    $("#ingredients_ul > li").on('click', function (){
        $(this).toggleClass("crossed");
    });
});
function replaceIngredients(ingredients_list, data) {
    ingredients_list.empty();
    $.each(data, function (index, element) {
        ingredients_list.append($('<li>').text(element.ingredient));
    });
    $("#ingredients_ul > li").on('click', function (){
        $(this).toggleClass("crossed");
    });
}