$(document).ready(function(){
    $('button').on('click', function() {
        $(this).addClass('animate__animated animate__pulse');
        setTimeout(() => {
            $(this).removeClass('animate__animated animate__pulse');
        }, 1000);
    });

    $("#submitLinks").click(function(){
        let links = [];

        $('.form-control').each(function() {
            let link = $(this).val();
            if (link) {
                links.push(link);
            }
        });
        $.ajax({
            url: "https://multi-link-preview-465eb123f193.herokuapp.com/createMultiLink?" + $.param({links: links}, true),
            type: 'get',
            success: function(response){
                let result = "<button class='btn btn-primary btn-block' onclick='copyToClipboard(`" + response.url + "`)' id='resultButton'>Copy Combined Link</button>";
                $("#result").html(result);
                document.querySelector('#resultButton').scrollIntoView({ behavior: 'smooth' });
                $('#preview').attr('src', response.image_url).show();
            },
            error: function(jqXHR, textStatus, errorThrown){
                if(jqXHR.status == 429){
                    $("#submitLinks").prop('disabled', true);
                    $("#submitLinks").html("Hourly Limit Reached");
                }
                console.log(textStatus, errorThrown);
            },
            complete: function() {
                setTimeout(function() {
                    $("#submitLinks").prop('disabled', false);
                    $("#submitLinks").html("Submit Links");
                }, 60000); // reset button after 60 minutes
            }
        });
    });
});

function pasteFromClipboard(inputId) {
    navigator.clipboard.readText()
        .then(text => {
            document.getElementById(inputId).value = text;
        })
        .catch(err => {
            console.error('Failed to read clipboard contents: ', err);
        });
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        console.log('Copying to clipboard was successful!');
    }, function(err) {
        console.error('Could not copy text: ', err);
    });
}
