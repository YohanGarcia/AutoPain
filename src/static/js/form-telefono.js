// function formatearTelefono() {
//   var telefono = document.getElementById("telefono").value;
//   var expresionRegularTelefono = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,7}$/im;
//   if (!expresionRegularTelefono.test(telefono)) {
//     var nuevoTelefono = telefono.replace(/[^0-9]/g, '')
//       .replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
//     document.getElementById("telefono").value = nuevoTelefono;
//   }
// }

const select = document.querySelector("select");
select.addEventListener("change", function() {
  const allOption = this.querySelector("option[value='all']");
  if (allOption.selected) {
    allOption.selected = true;
    this.querySelectorAll("option").forEach(option => option.selected = true);
  } else {
    allOption.selected = false;
  }
});


function confirmarEliminacion() {
  return confirm('¿Está seguro de que desea eliminar este elemento?');
}

function cancelarEliminacion() {
  document.getElementById('form-eliminar').reset();
}

// document.getElementById('button1').addEventListener('click', showForm1())
// document.getElementById('button2').addEventListener('click', showForm2())
// document.getElementById('button3').addEventListener('click', showForm3())
// document.getElementById('button4').addEventListener('click', showForm4())

// document.getElementById('delete-servicio-pieza').addEventListener('click', deleteServicioPieza())

function showForm1() {
  document.getElementById("form1").style.display = "block";
  document.getElementById("form2").style.display = "none";
  document.getElementById("form3").style.display = "none";
  document.getElementById("form4").style.display = "none";
}

function showForm2() {
  document.getElementById("form1").style.display = "none";
  document.getElementById("form2").style.display = "block";
  document.getElementById("form3").style.display = "none";
  document.getElementById("form4").style.display = "none";
}

function showForm3() {
  document.getElementById("form1").style.display = "none";
  document.getElementById("form2").style.display = "none";
  document.getElementById("form3").style.display = "block";
  document.getElementById("form4").style.display = "none";
}

function showForm4() {
  document.getElementById("form1").style.display = "none";
  document.getElementById("form2").style.display = "none";
  document.getElementById("form3").style.display = "none";
  document.getElementById("form4").style.display = "block";
}


let cantidad = document.getElementById("cantidad");
let cantidades = document.getElementById("cantidades");

if (valorSeleccionado === "UNID") {
  input.value = "Datos para UNID";
} else if (valorSeleccionado === "Libre") {
  input.value = "Datos para Libre";
}


$(document).ready(function(){
    
  var multipleCancelButton = new Choices('#choices-multiple-remove-button', {
     removeItemButton: true,
     maxItemCount:5,
     searchResultLimit:5,
     renderChoiceLimit:5
   }); 
  
  
});