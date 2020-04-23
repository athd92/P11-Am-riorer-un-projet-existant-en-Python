

  $('#mail').click(function() {
    // You gotta include the csrf_token in your post data
    let entry = {
                aliment_id: $('#aliment_id').text(),
            };
    console.log("ENTRY : " + entry.aliment_id)
  $.ajax({
      type: 'POST',
      url: `${window.origin}/send_infos/`,
      data: {'aliment_id': entry.aliment_id, 'csrfmiddlewaretoken': '{{ csrf_token }}'},
      success: function (data, textStatus) {
          //alert(data, textStatus);
         console.log('SUCCESS AJAX')
      },
      error: function(xhr, status, e) {
          alert(status, e);
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


