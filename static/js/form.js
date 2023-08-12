
function search_label(tag,atr,vl)
{
   var els = document.getElementsByTagName(''+tag+'');

   vl=""+vl.toLowerCase()+"";
   for (var i = 0; i<els.length; i++) {
      var elem=els[i];
      if ( elem.getAttribute(""+atr+"").toString().toLowerCase()==vl){
         return elem;
      }
   }
}

function select_form(){
   const select = document.getElementById("id_tipo").value;
   const field = document.getElementById("id_trabajador");
   const label = search_label('label', 'for', 'id_trabajador')
   
   if(select == "ACCION"){
      field.style.display="block";
      field.required = true;
      label.style.display="block";
   }
   else{
      field.style.display="none";
      field.required = false;

      label.style.display="none";

   }
}

