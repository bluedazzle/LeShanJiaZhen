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

function cancel_appointment_n(id){
    var r = confirm("您确定要取消预约么？");
    if(r==true){
        window.location.href = 'appointment_cancel_n?id='+id;
    }
}

function cancel_appointment_g(id){
    var r = confirm("您确定要取消预约么？");
    if(r==true){
        window.location.href = 'appointment_cancel_g?id='+id;
    }
}

function cancel_appointment_all_n(){
    var r = confirm("您确定要取消所有预约么？");
    if(r==true){
        window.location.href = 'appointment_cancel_all_n?';
    }
}

function cancel_appointment_all_g(){
    var r = confirm("您确定要取消所有预约么？");
    if(r==true){
        window.location.href = 'appointment_cancel_all_g';
    }
}

function get_appointment(id){
    window.location.href = 'appointment_get?id='+id
}

function get_all_appointment(){
    window.location.href = 'appointment_get_all'
}

function finish_appointment(id){
    window.location.href = 'appointment_finish?id='+id
}

function finish_all_appointment(){
    window.location.href = 'appointment_finish_all'
}