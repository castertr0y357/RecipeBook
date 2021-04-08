$(document).ready(function(){
    $("input[type='button']").click(function(){
        console.log("clicked submit")
        let value, ingredients;
        value = $("input[name='default_recipe_sizes']:checked").val();
        console.log(value)
        ingredients = $("#ingredients_ul")
        $.ajax({
            type: 'GET',
            url: url,
            data:{resize_value: value},
            dataType: 'json',
            
        })
    })
    $("#recipe_sizing_reset").click(function (){
        console.log("clicked reset")
    })
})