function setUrlModal(url){
   const link = document.getElementById("url-eliminar-modal");
   link.setAttribute("href", url)
}

function selectMonth(){
   const value = document.getElementById("mes").value
   const url = document.getElementById(value).getAttribute("data-url")
   window.location = url
}


