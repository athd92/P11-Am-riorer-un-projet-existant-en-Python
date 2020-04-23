  $('#mail').click(function() {
    let entry = {
                aliment_id: $('#aliment_id').text(),
                };
    console.log("ENTRY : " + entry.aliment_id)
  $.ajax({
      type: 'POST',
      url: `${window.origin}/send_infos/`,
      data: {'aliment_id': entry.aliment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
      beforeSend:function(){            
        console.log('before')
        $('#mail').hide();
        $('#sending').show();
    },
      complete:function(){
        console.log("after")
        $('#sending').hide();
       
      },

      success: function (data, textStatus) {
         console.log('SUCCESS AJAX')
         $('#sent').show();
         $('#sent').click(false);
      },
      error: function(e) {
          $('#sent').hide();
          console.log('Ajax request failed: ' + e)
          $('#error').show();
      }
  });
});


























// $("#mail").click(function() {
//     let entry = {
//         aliment_id: $('#aliment_id').text(),
//     };
//     console.log("ENTRY : " + entry.aliment_id)
//     send_mail_request(entry);
// });


// function send_mail_request(entry){   // the ajax request function
//     console.log("VALUE:" + entry.aliment_id)
    
//     $.ajax({                    // ajax request from input data
//         type:'POST',
//         url:`${window.origin}/send_infos/`,
//         data: JSON.stringify(entry.aliment_id),
//         contentType: 'application/json;charset=UTF-8',

//         beforeSend:function(){            
          
//         },

//         complete:function(){
//         },

//         success:function(data){      
            
        
//             },
        

//         error:function(e){            
         
//         }
//    });
// };


