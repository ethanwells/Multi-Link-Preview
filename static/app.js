$(document).ready(function(){
    $("#submitLinks").click(function(){
        let links = [];

        $('.linkInput').each(function() {
            let link = $(this).val();
            if (link) {
                links.push(link);
            }
        });
        console.log(links);
        $.ajax({
            url: "https://multi-link-preview-465eb123f193.herokuapp.com/createMultiLink?" + $.param({links: links}, true),
            type: 'get',
            success: function(response){
                $("#result").html("Result link: <a href='" + response.url + "'>" + response.url + "</a>");
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(textStatus, errorThrown);
            }
        });
    });
});
