
function getCookie(name) {
   let cookieValue = null;
   if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
         const cookie = cookies[i].trim();
         // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
               break;
            }
      }
   }
   return cookieValue;
}

function ajax_data(id_subelemento, id_elemento){
   const url = document.getElementById("pedidoForm").getAttribute("data-subelementos-url");
   const elementoId = document.getElementById(id_elemento).value;
   const csrftoken = getCookie('csrftoken');

   fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers:{
         'Accept': 'application/json',
         'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
         'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({'elemento_id':elementoId}) //JavaScript object of data to POST
   })
      .then(response => {
         return response.json() //Convert response to JSON
      })
      .then(data => {
         var html_data = '<option value="">---------</option>';
         data.forEach(function (subelemento) {
            html_data += `<option value="${subelemento.id}">${subelemento.codigo_unico}-${subelemento.marca}</option>`
         });
         var subelemento = document.getElementById(id_subelemento)
         subelemento.innerHTML = html_data
      })}



function agregar_inputs(){
   var cantidad_forms = document.querySelector("#id_form-TOTAL_FORMS");
   const campos = ["Cantidad_pedida","Elemento", "Subelemento"]
   const table = document.getElementById("formset") 
   const nuevaFila= table.insertRow(parseInt(cantidad_forms.value)+1);

   for(var i = 0; i < campos.length; i++){
      var nuevo_label = document.createElement('label');
      nuevo_label.innerHTML = campos[i]
      var nuevo_input = document.querySelector("#id_form-0-"+campos[i].toLowerCase()).cloneNode(true);
      nuevo_input.name = 'form-'+cantidad_forms.value+'-'+campos[i].toLowerCase();
      nuevo_input.id = 'id_form-'+cantidad_forms.value+'-'+campos[i].toLowerCase();

      var nuevaCelda = nuevaFila.insertCell(i);
      nuevaCelda.appendChild(nuevo_input)
   }
   var id_elemento = "id_form-"+cantidad_forms.value+"-elemento";
   var id_subelemento = "id_form-"+cantidad_forms.value+"-subelemento";
   const selectElement = document.getElementById(id_elemento);
   selectElement.addEventListener('change', (event) => {
      ajax_data(id_subelemento, id_elemento)
   });

   cantidad_forms.value = parseInt(cantidad_forms.value)+1;
   if(parseInt(cantidad_forms.value) > 1){
      boton = document.getElementById("eliminar-input")
      boton.removeAttribute('disabled');
   }
}

function eliminar_inputs(){
   var cantidad_forms = document.querySelector("#id_form-TOTAL_FORMS");
   var table = document.getElementById("formset");
   var rowCount = table.rows.length;
   table.deleteRow(rowCount -1);
   cantidad_forms.value = parseInt(cantidad_forms.value-1)
   if(parseInt(cantidad_forms.value) < 2){
      boton = document.getElementById("eliminar-input")
      boton.setAttribute('disabled','');
   }
}

var id_elemento = "id_form-"+0+"-elemento";
var id_subelemento = "id_form-"+0+"-subelemento";
const selectElement = document.getElementById(id_elemento);
ajax_data(id_subelemento, id_elemento)
selectElement.addEventListener('change', (event) => {
   ajax_data(id_subelemento, id_elemento)
});

boton = document.getElementById("eliminar-input")

boton.setAttribute('disabled', '');

