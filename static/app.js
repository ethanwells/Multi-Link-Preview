$(document).ready(function(){
    $('button').on('click', function() {
        $(this).addClass('animate__animated animate__pulse');
        setTimeout(() => {
            $(this).removeClass('animate__animated animate__pulse');
        }, 1000);
    });

    $("#submitLinks").click(function(){
        // Remove the "Copy Combined Link" button, if it exists.
        $("#result").empty();
    
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
                let result = "<button class='btn btn-primary btn-block' onclick='copyToClipboard(`" + response.url + "`)' id='resultButton'>Copy Chainlink</button>";
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
                    $("#submitLinks").html("Create Chainlink");
                }, 60000); // reset button after 60 minutes
            }
        });
    });

    
    for(let i = 1; i < 6; i++){
        const cookie = $.cookie("video_link"+i);
        if(cookie){
            $("#link"+i).val(cookie);

            //Too many request will occur Error 426/429 from linkpreview (Exceeds)

            // if(/^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})(\/\w\W*)*\/??\/.+$/.test(cookie)){

            //     const apiKey = "e643b89bdc8fe8b31fce6595c218c05d";
            
            //     $.ajax({
            //         url: "http://api.linkpreview.net/?key=" + apiKey + "&q=" + cookie,
            //         type: 'get',
            //         success: function(response){                        
            //             $("img#thumb_link"+i).attr('src', response.image).show();
            //         },
            //     });
            // }
        }
    }
    $('div.input-group').find('input').on('input', function() {
        const url = $(this).val();
        const id = $(this).attr('id');
        $.cookie("video_"+id, url);

        if(url && url!=="" && /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})(\/\w\W*)*\/??\/.+$/.test(url)){            
            const apiKey = "26469aad62a864ac4bbb91fcdf43c0e1";

            $.ajax({
                url: "http://api.linkpreview.net/?key=" + apiKey + "&q=" + url,
                type: 'get',
                success: function(response){                    
                    $("img#thumb_"+id).attr('src', response.image).show();
                },
            });
        }else{
            $("img#thumb_"+id).attr('src', "").show();
        }
    });
    $('div.input-group').find('input').blur(function() {
        const url = $(this).val();
        const id = $(this).attr('id');
        
        if(url && url!=="" && /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})(\/\w\W*)*\/??\/.+$/.test(url)){            
            const apiKey = "26469aad62a864ac4bbb91fcdf43c0e1";

            $.ajax({
                url: "http://api.linkpreview.net/?key=" + apiKey + "&q=" + url,
                type: 'get',
                success: function(response){                    
                    $("img#thumb_"+id).attr('src', response.image).show();
                },
            });
        }else{
            $("img#thumb_"+id).attr('src', "").show();
        }
        
    })
});


function pasteFromClipboard(inputId) {
    navigator.clipboard.readText()
        .then(text => {
            document.getElementById(inputId).value = text;

            $.cookie("video_"+inputId, text);

            if(/^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})(\/\w\W*)*\/??\/.+$/.test(text)){
                const apiKey = "26469aad62a864ac4bbb91fcdf43c0e1";          

                $.ajax({
                    url: "http://api.linkpreview.net/?key=" + apiKey + "&q=" + text,
                    type: 'get',
                    success: function(response){                    
                        $("img#thumb_"+inputId).attr('src', response.image).show();
                    },
                });
            }else{
                $("img#thumb_"+inputId).attr('src', "").show();
            }
            
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

function handleBack() {
    window.history.back();
}