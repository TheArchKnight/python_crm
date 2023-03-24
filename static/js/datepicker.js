function datepicker(){
   // Get the data of the dates from the passing in the template
   const data = document.currentScript.dataset;
   const visitas_vigentes = JSON.parse(data.visitas);

   const date = new Date();

   let day = date.getDate();
   let month = date.getMonth() +1;
   let year = date.getFullYear();

   let currentDate = `${year}-${month}-${day}`;
   console.log(currentDate)
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
      var elementos_html = []
      for(var i = 0; i < visitas_vigentes.length; i++){
         if(fecha == visitas_vigentes[i].fecha){
            elementos_html.push(`<li>${visitas_vigentes[i].cliente__nombre_orgnanizacion}, ${visitas_vigentes[i].fecha}</li>`)
         }

      }
      if(elementos_html.length > 0){
         console.log(elementos_html)
         $("#fecha_repetida").html(
            `Elegiste una fecha en la cual ya se encuentran programadas otras visitas:${elementos_html}¿Estas seguro que deseas esta nueva fecha?` );
      }
      else{
         $("#fecha_repetida").html("");
      }

   });
}



