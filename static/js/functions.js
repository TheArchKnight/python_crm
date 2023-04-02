
//Funcion usada en eliminar pago y eliminar obra para no 
//cargar modales iguales
function setUrlModal(url, attr){
   const link = document.getElementById('url-eliminar-modal'); 
   console.log(attr)
   link.setAttribute(attr, url)
}

function selectMonth(){
   const value = document.getElementById("mes").value
   const url = document.getElementById(value).getAttribute("data-url")
   window.location = url
}

function setUrlPagos(pk){
   const inicio = document.getElementById("inicio").value
   const final = document.getElementById("final").value
   url = "/fachadas/" + pk + "/" + inicio + "/" + final + "/pagos/"
   console.log(url)
   window.location = url
}


