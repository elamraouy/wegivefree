// return scroll x y
function timeConverter(UNIX_timestamp) {
    var a = new Date(UNIX_timestamp);
    var months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Decembre'];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = a.getDate();
    var hour = a.getHours();
    var min = a.getMinutes();
    var time = date + ' ' + month + ' ' + year + ' à ' + hour + 'h:' + min + 'min';
    return time;
}
function getScroll() {
    if (window.pageYOffset != undefined) {
        return [pageXOffset, pageYOffset];
    } else {
        var sx, sy, d = document,
            r = d.documentElement,
            b = d.body;
        sx = r.scrollLeft || b.scrollLeft || 0;
        sy = r.scrollTop || b.scrollTop || 0;
        return [sx, sy];
    }
}
function validate_phone(phone) {
    var regex = /^\+(?:[0-9] ?){6,14}[0-9]$/;

    if (regex.test(phone)) {
        return true
    } else {
        return false
    }
}
$(function () {
    function update_message(conversation_id){
           $.ajax({
                    type: 'POST',
                    url: '/update_messages/',
                    data: {
                        'conversation': conversation_id,
                      },
                    success: function (data) {
                        let html = ''; let bg_class; let align_class;
                        $.each(data, function (key, req) {
                            align_class = (req.sender__id == req.conversation__gift__gived_by)? 'flex-row' : 'flex-row-reverse';
                            bg_class =  (req.sender__id == req.conversation__gift__gived_by)? 'bg-light-blue' : 'bg-dark-blue';
                            html+=`
                             <div class="d-flex ${align_class} bd-highlight w-100 ">
                             <div class="w-75 ${bg_class} p-2 my-3 rounded shadow">
                             <h6><img src="${req.sender__profile__user_image}" class="rounded mx-2 rounded-circle" width="30">
                             ${req.sender__first_name} ${req.sender__last_name}</h6>
                             <p dir="auto">${req.message}</p>
                             <small><i class="fas fa-clock"></i> ${timeConverter(req.date_send)}</small>
                            </div></div> `;
                        })
                     $('#chat'+conversation_id).append(html);
                     //$('#chat_modal_body').append(html);
                     $("#chat"+conversation_id).scrollTop($("#chat"+conversation_id)[0].scrollHeight);
                    }
             })
       }
    function get_messages(conversation_id){
            $.ajax({
                    type: 'POST',
                    url: '/get_gift_message/',
                    data: {
                        'conversation': conversation_id,
                      },
                    success: function (data) {
                    let chat_header = `
                     <img src="${data.guest[0].user_image}" class="rounded mx-2 rounded-circle" width="30">
                     ${data.guest[0].first_name}
                    `;
                    $('#chat_modal').find('.modal-title').html(chat_header);
                       if(Object.keys(data.received_messages).length>0){
                        let html = ''; let bg_class; let align_class;
                        html+=`<div
                        class="col-md-12 p-1 mb-1 w-100"
                        style="max-height:400px; overflow: hidden">
                        <div id="chat${conversation_id}" style="max-height:320px; overflow-y: scroll">`;
                        $.each(data.received_messages, function (key, req) {
                            align_class = (req.sender__id == req.conversation__gift__gived_by)? 'flex-row' : 'flex-row-reverse';
                            bg_class =  (req.sender__id == req.conversation__gift__gived_by)? 'bg-light-blue' : 'bg-dark-blue';
                            html+=`
                             <div class="d-flex ${align_class} bd-highlight w-100 ">
                             <div class="w-75 ${bg_class} p-2 my-3 rounded shadow">
                             <h6>
                             <img src="${req.sender__profile__user_image}" class="rounded mx-2 rounded-circle" width="30">
                             ${req.sender__first_name} ${req.sender__last_name}</h6>
                             <p dir="auto">${req.message}</p>
                             <small><i class="fas fa-clock"></i> ${timeConverter(req.date_send)}</small>
                             </div>
                            </div>`;
                        })

                        html+=`</div><div class="col-md-12 bg-light shadow rounded w-100 align-items-center p-4">
                          <div class="type_msg">
                             <div class="input_msg_write">
                             <form class="send_response_form" method="post">
                                 <input type="hidden" name="conversation" value="${conversation_id}">
                                 <input type="text"  autocomplete="off" id="msgInput" class="write_msg"
                                name="response" placeholder="Taper une message"/>
                                <button class="msg_send_btn" type="submit">
                                <i class="fas fa-paper-plane" aria-hidden="true"></i></button>
                             </form>
                             </div>
                        </div>
                       </div>
                     </div>`;
                        //$('#messageContainer'+conversation_id).html(html);
                        $('#chat_modal_body').html(html);
                        $("#chat"+conversation_id).scrollTop($("#chat"+conversation_id)[0].scrollHeight);
                     }else{
                        $('#chat_modal_body').html('Desolé cette conversation est términée');
                       }
                    }
             })
       }
    // stop updating message when chat modal is hidden
     $('#chat_modal').on('hide.bs.modal', function () {
        clearInterval(refrechMessages);
    })
    // send responses
    $('#chat_modal_body').on('submit', '.send_response_form', function(e){
     e.preventDefault();
     let form_data = new FormData($(this)[0])
     $.ajax({
            type: 'POST',
            url: '/sned_response_to/',
            data: form_data,
            dataType: 'json',
            contentType: false,
            processData: false,
            success: function (data) {
                 let req = data.message[0]
                    let html = ''; let bg_class; let align_class;
                    align_class = (req.sender__id == req.conversation__gift__gived_by)? 'flex-row' : 'flex-row-reverse';
                    bg_class =  (req.sender__id == req.conversation__gift__gived_by)? 'bg-light-blue' : 'bg-dark-blue';
                    html+=`
                     <div class="d-flex ${align_class} bd-highlight w-100 ">
                     <div class="w-75 ${bg_class} p-2 my-3 rounded shadow">
                     <h6><img src="${req.sender__profile__user_image}" class="rounded mx-2 rounded-circle"
                                             width="30">
                     ${req.sender__first_name} ${req.sender__last_name}</h6>
                     <p>${req.message}</p>
                     <small><i class="fas fa-clock"></i> ${timeConverter(req.date_send)}</small>
                    </div></div> `;
                 $('#chat'+req.conversation).append(html);
                 $("#chat"+req.conversation).scrollTop($("#chat"+req.conversation)[0].scrollHeight);
                 $('#msgInput').val('');
            }
            })
    })

    // show conversation anywhere
    function show_messages_modal(conversation_id){
         $('#chat_modal_body').html('loading chat wait...')
         $('#chat_modal').modal({ backdrop: "static" })
         // get all messages first
         get_messages(conversation_id)
         // refresh to get new messages
         refrechMessages = setInterval(function(){
                update_message(conversation_id)
         }, 5000);
    }

    $("body").on('click','.show_converstation_messages',function(e){
         e.preventDefault();
         show_messages_modal($(this).data('id'));
    })

    // manage notifications
    // get unread notification on count click
     $('#notify-area').on('shown.bs.dropdown', function(e){
        let loader = `<div>
                    <div class="spinner-grow" style="width: 3rem; height: 3rem;"
                         role="status">
                        <span class="sr-only">Loading...</span>
                    </div>
                    <strong> Patientez un moment SVP </strong>
                </div>`;
        $("#notify_holder").html(loader)
        $.ajax({
            type: 'POST',
            url: '/notifications/',
            dataType: 'json',
            data: { 'task' : 'get_unread'},
            success: function (data) {
            if(data.count!==0){
            let html='';
               for (let i=0; i < data.unread.length; i++) {
                    msg = data.unread[i];
                    let url = (msg.absolute_url !== null)? msg.absolute_url : '#';
                    html +=`<a href="${url}" data-id="${msg.id}"
                    data-type="${msg.type}"
                    data-target="${msg.target}"
                    class="text-reset notification-item">
                    <div class="media">
                        <div class="avatar-xs mr-3">
                        <span class="avatar-title bg-primary rounded-circle font-size-16">
                            <img src="${msg.sender__profile__user_image}" width="40" class="rounded-circle image-fluid">
                        </span>
                        </div>
                        <div class="media-body">
                            <h6 class="mt-0 mb-1">
                             <span class="badge badge-${msg.level}">${msg.type}</span>
                              ${msg.verb}
                            </h6>
                            <div class="font-size-12 text-muted">
                                <p class="mb-0"><i class="mdi mdi-clock-outline"></i>
                                 ${timeConverter(msg.date_send)}</p>
                            </div>
                        </div>
                        </div>
                    </a>`;
                  }
                  $("#notify_holder").html(html)
               }
            else{
              $("#notify_holder").html(' <h6 class="p-2">Pas de nouvelles notifications</h6>')
            }
            }
        })
      })

    $('#notify_holder').on('click', '.notification-item', function(e){
      e.preventDefault();
        let notyId = $(this).data('id');
        let type = $(this).data('type');
        let target = $(this).data('target');
        let url = $(this).attr('href');
        $.ajax({
            type: 'POST',
            url: '/manage_notifications/',
            data: {
                'id': notyId
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                if(type=='message'){
                  show_messages_modal(target)
                }else if (type=='demande'){
                  open(url, '_self');
                }
               }
            }
        })
    })
    // validate and send new gift
    $("#addPostForm").on('submit', function (e) {
        e.preventDefault();
        let form = document.querySelector("#addPostForm");
        let fd = new FormData(form);
        let imageFile = $("#id_image")[0].files[0];
        fd.append("image", imageFile);
        $("#sendGiftBtn").html('Envois en cours patientez...').prop('disabled', true);
        $.ajax({
            type: 'POST',
            url: '/add/',
            data: fd,
            dataType: 'json',
            contentType: false,
            processData: false,
            success: function (data) {
                if (data.success) {
                    $("#sendGiftBtn").html('Je veux offrir').prop('disabled', false);
                    $.alert({
                        closeIcon: true,
                        title: 'Gift bien ajouté',
                        content: 'Votre génerosité n\'a pas de limite! merci ',
                        type: 'green',
                        columnClass: 'col-md-8',
                        buttons: {
                            'Consulter cet offre': function () {
                                btnClass: 'btn-green',
                                    open('/show/?id=' + data.id, '_self');
                            },
                            'Consulter tous': function () {
                                btnClass: 'btn-blue',
                                    open('/gifts/', '_self');
                            },
                            'Ajouter un autre ?': function () {
                            }
                        }
                    });
                } else {
                    let errors = data.errors;
                    let message = ""
                    $('.form-control').removeClass('is-invalid').addClass('is-valid')
                    $.each(errors, function (i, item) {
                        $("#id_" + i).addClass('is-invalid')
                        message += '- ' + item + '<br>'
                    });
                    $("#sendGiftBtn").html('Je veux offrir').prop('disabled', false);
                    $.alert({
                        title: 'Errors',
                        content: message,
                        type: 'orange'
                    })

                }

            }
        });
    });

    // test if user is authenticated and show request modal
    $('.interstedBtn').click(function (e) {
       e.preventDefault();
        $("#card-loader").css('display', 'block');
        if(userIsAauthenticated){
        $("#card-loader").css('display', 'none');
        $("#modalIterested").toggle();
        }else{
         $("#modal-login").modal('show');
        }
    })

    // Validate and send new request
    $("#newDemandeForm").on('submit', function (e) {
        e.preventDefault();
        var form = document.querySelector("#newDemandeForm");
        var fd = new FormData(form);
        let phone = $("#id_user_phone").val()
        if (validate_phone(phone)) {
            $("#modalMask").addClass('d-flex').removeClass("d-none");
            $('#sendNewDemande').prop('disabled', true);
            $.ajax({
                type: 'POST',
                url: '/add_request/',
                data: fd,
                dataType: 'json',
                contentType: false,
                processData: false,
                success: function (data) {
                    if (data.success) {
                        $("#modalMask").addClass('d-none').removeClass("d-flex");
                        $('#sendNewDemande').prop('disabled', false);
                        $("#modalIterested").toggle();
                        $.alert({
                            closeIcon: true,
                            title: 'Demande bien ajouté',
                            content: 'Votre demande a été bien envoyé',
                            type: 'green',
                            columnClass: 'col-md-8',
                            buttons: {
                                'Consulter les offres': function () {
                                    btnClass: 'btn-blue',
                                        open('/gifts/', '_self');
                                },
                                'Fermer': function () {
                                }
                            }
                        });
                    } else {
                        $("#modalMask").addClass('d-none').removeClass("d-flex");
                        $('#sendNewDemande').prop('disabled', false);
                        let message = ""
                        $.each(data.errors, function (i, item) {
                            message += '- ' + item + '<br>'
                        });
                        $.alert({
                            closeIcon: true,
                            title: 'Demande non autorisé',
                            content: message,
                            type: 'red',
                            columnClass: 'col-md-8',
                            buttons: {
                                'Fermer': function () {
                                }
                            }
                        });
                    }
                }
            })
        } else {
            alert('tel non valide')
        }

    });

    // Delete gifts by admin
    $(".adminDel").click(function (e) {
        e.preventDefault();
        let id = $(this).data('id');
        $.confirm({
            title: 'Confirmer action',
            content: 'Voules vous vraiment supprimer cet offre!',
            buttons: {
                confirm: function () {
                    $.ajax({
                        type: 'POST',
                        url: '/delete/',
                        data: {
                            'gift_id': id
                        },
                        success: function (data) {
                            $("#cardHolder" + id).hide('fast');
                        }
                    });
                },
                cancel: function () {

                }

            }
        });
    })

    // hide gift by users
    $(".hideItem").click(function (e) {
        e.preventDefault()
        let id = $(this).data('id');
        $("#cardHolder" + id).hide('fast');
    })

    $(".showMenu").click(function (e) {
        e.preventDefault()
        let id = $(this).data('id');
        $("#giftMenu" + id).show('fast');
    })

    $("#closemodal").on('click', function (e) {
        e.preventDefault();
        $("#newdemande").trigger("reset");
        $("#modalIterested").toggle();
    })

    // AJAX SETUP csrf token This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    let avatar = $("#user_avatar").val()
    $.ajax({
        type: 'POST',
        url: '/save_profile/',
        dataType: 'json',
        data: {
            "avatar": avatar
        },
        success: function (data) {
        }
    })

    // get notifications count
  function get_noty_count(){
  $.ajax({
        type: 'POST',
        url: '/notifications/',
        dataType: 'json',
        data: {'task': 'get_count'},
        success: function (data) {
        if(data.count!==0){
            $(".notify-count").addClass('badge-danger').html(data.count)
         }else{
            $(".notify-count").removeClass('badge-danger').html('')
         }
        }
    })
  }
  if(userIsAauthenticated){
  get_noty_count();
  refrechNoty = setInterval(function(){
                get_noty_count();
         }, 5000);
  }


})

