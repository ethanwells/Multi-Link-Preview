$(document).ready(function(){
    $("#submitLinks").click(function(){
        let links = [];

        $('.linkInput').each(function() {
            let link = $(this).val();
            if (link) {
                links.push(link);
            }
        });

        $.ajax({
            url: "https://multi-link-preview-465eb123f193.herokuapp.com/createMultiLink",
            type: 'get',
            data: { links: links },
            success: function(response){
                $("#result").html("Result link: <a href='" + response + "'>" + response + "</a>");
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(textStatus, errorThrown);
            }
        });
    });
});
