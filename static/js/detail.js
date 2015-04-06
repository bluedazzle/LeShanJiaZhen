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

function add_service_info(id, person, time){
    window.location.href = 'appointment_info_add?id=' + id + '&serive_person=' + person + '&servie_time=' + time
}

function finish_all_appointment(){
    window.location.href = 'appointment_finish_all'
}

function onlyNumber(obj){

      //得到第一个字符是否为负号
      var t = obj.value.charAt(0);
      //先把非数字的都替换掉，除了数字和.
      obj.value = obj.value.replace(/[^\d\.]/g,'');
       //必须保证第一个为数字而不是.
       obj.value = obj.value.replace(/^\./g,'');
       //保证只有出现一个.而没有多个.
       obj.value = obj.value.replace(/\.{2,}/g,'.');
       //保证.只出现一次，而不能出现两次以上
       obj.value = obj.value.replace('.','$#$').replace(/\./g,'').replace('$#$','.');

}
//建立一個可存取到該file的url
function getObjectURL(file) {
	var url = null ;
	if (window.createObjectURL!=undefined) { // basic
		url = window.createObjectURL(file) ;
	} else if (window.URL!=undefined) { // mozilla(firefox)
		url = window.URL.createObjectURL(file) ;
	} else if (window.webkitURL!=undefined) { // webkit or chrome
		url = window.webkitURL.createObjectURL(file) ;
	}
	return url ;
}