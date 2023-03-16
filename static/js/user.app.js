$(function () {
    // display all requests for a gift
    $(".show_requests").click(function (e) {
        e.preventDefault();
        let gift_id = $(this).data('id');
        $("#requestHolder" + gift_id).show();
        $.ajax({
            type: 'POST',
            url: '/display_requests/',
            data: {'gift_id': gift_id},
            success: function (data) {
            if(data.success){
                    let html = ''; let borderClass; let btnAccept;
                    $.each(data.req, function (key, req) {
                       let city = ( req.user_city == 'All')? '---' : req.user_city;
                       if(req.stats == "accepted"){
                           btnAccept= `<button disabled class="btn btn-success mx-1 manageBtn">
                                         <i class="fas fa-check"></i> Demande acceptée </button>`;
                           btnOpenChat = `<button class="btn btn-warning mx-1 show_converstation_messages"
                            data-id="${req.conversation}">
                           <i class="fas fa-comments"></i> Ouvrir la conversation </button>`;
                           borderClass = 'success';
                       }else{
                           btnAccept = `<button id="acceptMe${req.id}" data-req_user="${req.user}" data-gift_id="${req.gift__id}"
                           data-requset_id="${req.id}" data-action="accept" data-action="accept" class="btn btn-success mx-1 manageBtn">
                                          Accepter cette demande </button>`;
                           borderClass = 'warning';
                           btnOpenChat = '';
                       }
                    html += `<div id="requestCard${req.id}"
                    class="bg-white border-bottom border-5 border-${borderClass} rounded text-dark p-2 my-3 col-md-12">
                      <div class="card-body">
                          <div class="row">
                              <div class="col-md-12">
                                  <h5 class="card-title">
                                  <img src="${req.user__profile__user_image}"
                                  class="ronded rounded-circle" width="40" height="40">
                                     ${req.user_name}
                                  </h5>
                                  <h6>${city}</h6>
                                  <h6> <i class="fas fa-phone"></i> ${req.user_phone}</h6>
                                  <h6><i class="fas fa-at"></i> ${req.user_email}</h6>
                                  <h6 class="card-subtitle mb-2 text-muted">${timeConverter(req.date_add)}</h6>
                              </div>
                              <div class="col-md-12" id="requestbuttons${req.id}" >
                                  <p class="card-text p-4 rounded shadow  bg-light">${req.user_message}</p>
                                  ${btnAccept}
                                  ${btnOpenChat}
                              </div>
                          </div>
                      </div>
                    </div>`;
                           });
                    $("#requestHolder" + gift_id).html(html);
            }else{
             $("#requestHolder" + gift_id).html('<h4 class="alert alert-warning">Aucune demande pour cet offre</h4>');
            }


            }
        })

    })
    // manage requests users_requests template
    $("#offresContent").on('click', '.manageBtn', function(e){
        e.preventDefault()
        let request_id = $(this).data('requset_id');
        let action = $(this).data('action');
        let request_user = $(this).data('req_user')
        let gift_id = $(this).data('gift_id')
        $.ajax({
                type: 'POST',
                url: '/manage_request/',
                data: {
                    'request_id': request_id,
                    'request_user': request_user,
                    'gift_id': gift_id,
                    'action': action
                  },
                success: function (data) {
                    if(data.success){
                    if(action=='accept'){
                    let btnOpenChat;
                     $("#acceptMe"+request_id).html('<i class="fas fa-check"></i> Demande acceptée').prop('disabled', true);
                     $("#requestCard"+request_id).removeClass('border-primary').addClass('border-success');
                     req = data.message.conversation[0];
                     console.log(req)
                     btnOpenChat = `<button class="btn btn-warning mx-1 show_converstation_messages"
                            data-id="${req.id}">
                          <i class="fas fa-comments"></i> Ouvrir conversation </button>`;
                     $("#requestbuttons"+request_id).append(btnOpenChat);
                         $.alert({
                            title: 'Merci',
                            content: data.message.result,
                            type: 'green'
                         })
                     }else{
                     $("#acceptMe"+request_id).html('Accpeter').prop('disabled', false);
                     $("#requestCard"+request_id).removeClass('border-success').addClass('border-primary');
                     }
                    }
                }
            });
    })
    // show conversations by gift
    $(".show_message").click(function(e){
         e.preventDefault();
         $('#messagesHolder').html("Chargement en cours patientez...");
         let gift_id = $(this).data('id');
         $.ajax({
                type: 'POST',
                url: '/get_all_conversation/',
                data: {
                    'gift_id': gift_id,
                  },
                success: function (data) {
                   let html = '';
                   if(Object.keys(data).length !== 0){
                    $.each(data, function (key, req) {
                    html+=`<a class="show_converstation_messages nav-link" data-id="${req.id}">
                    <div class="card bg-light-blue shadow rounded p-1 mb-2">
                    <div class="col-md-12">
                     <div class="row">
                     <div class="col-md-4 col-sm-12 text-center">
                       <div class="d-inline justify-content-center text-center">
                          <img src="${req.c_host__profile__user_image}" width="60" class="rounded border-white rounded-circle">
                          <img src="${req.c_guest__profile__user_image}" width="60" style="margin-left:-20px"
                          class="rounded rounded-circle border-white">
                          </div>
                     </div>
                     <div class="col-md-8 text-center mt-1 justify-content-center">
                         <h6 class="text-center text-dark">${req.c_host__first_name} ${req.c_host__last_name}
                          et ${req.c_guest__first_name} ${req.c_guest__last_name}</h6>
                          <i class="fas fa-comments fa-x2"></i> ouvrir la discussion
                     </div>

                     </div>
                    </div>
                    </div> </a>
                    <div class="card bg-light d-none messageContainer" id="messageContainer${req.id}">
                    </div>`;
                    })
                   }else{
                     html+=`<h4 class="alert alert-warning text-center shadow rounded mt-4">
                     Aucune conversation active pour cet offre </h4>`;
                   }
                    $('#messagesHolder').html(html);
                  }
                })
        })

})