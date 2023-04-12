function getEventsOnDate(date, events, element_id, clear=false){

   var elementos_html = []
   for(var i = 0; i < events.length; i++){
      if(date == events[i].fecha){
         elementos_html.push(`<li>${events[i].cliente__nombre_orgnanizacion}, ${events[i].fecha}</li>`)
      }
   }
   if(elementos_html.length > 0 && clear==false){
      $(element_id).html(
         `Elegiste una fecha en la cual ya se encuentran programadas otras visitas:${elementos_html}` );
   }
   else{
      $(element_id).html("");
   }
}

function getRecentEvent(){

   const date= new Date()
   let day = date.getDate();
   let month = date.getMonth() +1;
   let year = date.getFullYear();
   if(month < 10){
      var currentDate = `${year}-0${month}-${day}`;
   }
   else{
      var currentDate = `${year}-${month}-${day}`;
   }
   return currentDate
}


function datepicker(){
   // Get the data of the dates from the passing in the template
   const data = document.currentScript.dataset;
   const visitas_vigentes = JSON.parse(data.visitas);
   const name = data.nombre
   currentDate = getRecentEvent(visitas_vigentes, name) 
   var fecha_general;
   $('.datepicker').datepicker
   ({
      format: 'yyyy-mm-dd',
      startDate: currentDate,
      clearBtn: true,
      autoclose: true,
      todayHighlight: true,
      language: 'es',
      daysOfWeekDisabled: [6,0],
   });
   $(".datepicker").on("changeDate", function(event) {
      fecha = event.format()
      getEventsOnDate(fecha, visitas_vigentes , "#fecha_repetida")
   });

   $("#id_fecha").change(function(){
      fecha_general = $("#id_fecha").val()
      tipo = document.getElementById("id_tipo").value;
      console.log(tipo)
      if(tipo == "VISITA"){
         getEventsOnDate(fecha_general, visitas_vigentes, "#fecha_repetida_form")
      }
   });

   var tipo_select = document.getElementById("id_tipo");
   tipo_select.addEventListener('change',(event) =>{
      if(tipo_select.value == "VISITA"){
         getEventsOnDate(fecha_general, visitas_vigentes, "#fecha_repetida_form");
      }
      else{
         getEventsOnDate(fecha_general, visitas_vigentes, "#fecha_repetida_form", true)
      }
   });



}



