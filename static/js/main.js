console.log("Hello world!")


$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
})
