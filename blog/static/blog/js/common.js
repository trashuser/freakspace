$(function () {
	$('[data-toggle="tooltip"]').tooltip()
});

$(document).ready(function(){
  //при нажатию на элемент, имеющий класс .open-modal, открыть модальное окно 
  $('.open-modal').click(function(){
    $('#PlaylistModal').modal('show');
  });
  //отобразить сообщение, когда модальное окно будет полностью скрыто от пользователя
  // $("#myModal").on('hidden.bs.modal', function(){
  //   alert("Модальное окно было успешно закрыто.");
  // });
});




