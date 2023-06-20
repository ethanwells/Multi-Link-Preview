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
                // If the request is successful, hide the footer-prompt if it's visible
                $("#footer-prompt").css("display", "none");
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(textStatus, errorThrown);
                // Show the footer-prompt if the error is a 429 'Too Many Requests' error
                if(jqXHR.status == 429){
                    $("#footer-prompt").css("display", "block");
                }
            }
        });
    });
});
