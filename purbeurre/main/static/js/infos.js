
$(document).ready(function(){
    console.log("Page index loaded")
});


$('#mail').click(function(){
    $.ajax({                    // ajax request from input data
        type:'POST',
        url:`${window.origin}/send_infos`,
        data:JSON.stringify(entry),            
        contentType: 'application/json;charset=UTF-8',

        beforeSend:function(){            
            console.log('before')
        },

        complete:function(){
            console.log('complete')
        },

        success:function(data){      
            console.log(data);
        },

        error:function(e){            
            console.log(e)
        }
   });
});