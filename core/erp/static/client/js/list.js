var tblClient
function getData() {
  // para guardar el datatable en una variable y ejecutar una funcion que ya tiene para recargar los datos de la tabla
  tblClient=$("#data").DataTable({
    responsive: true,
    autoWidth: false,
    destroy: true,
    deferRender: true,
    ajax: {
      url: window.location.pathname,
      type: "POST",
      data: {
        action: "searchdata",
      },
      dataSrc: "",
    },
    columns: [
      { data: "id" },
      { data: "names" },
      { data: "surnames" },
      { data: "dni" },
      { data: "date_birthday" },
      { data: "gender.name" }, 
      { data: "id" },
    ],
    columnDefs: [
      {
        targets: [-1],
        class: "text-center",
        orderable: false,
        render: function (data, type, row) {
          var buttons =
             '<a href="#" rel="edit" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
          buttons +=
            '<a href="#" rel="delete" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
          return buttons;
        },
      },
    ],
    initComplete: function (settings, json) {},
  });
}
$(function () {
  modal_title=$('.modal-title') // selecciono el titulo del modal
  getData(); // para traer los datos
  
  $('#btnAdd').on('click', function () {
    $('input[name="action').val('add'); // para que la accion sea crear, porque cuando se haga el editar, va a cambiar su valor (value)

    modal_title.find('span').html('Creación de un cliente'); //en su espan vacia pongo el titulo
    modal_title.find('i').removeClass().addClass('fas fa-plus') // a la i le quito todas las clases y luego le pongo las clases del signo de más (+)
    $('form')[0].reset() // selecciono los formulario, solo hay uno pero se guardan como arreglo, selecciono el primero y unico ([0]) y aplico el reset para que cada vez que se abra el modal, el formulario se limpie
    $("#myModalClient").modal("show");
  })
  
  // selecciono la el tbody de la tabla, y agrego el evento click, a cada enlace que tenga en el cuerpo, y le paso cierta funcion
  // el rel edit se lo pongo para diferenciarlo del boton de eliminar
   $('#data tbody').on('click', 'a[rel="edit"]', function (e) {
     // para el titulo del modal
     modal_title.find("span").html("Edición de un cliente");
     modal_title.find("i").removeClass().addClass("fas fa-edit");

     // el closest('td,li') hace referencia a que seleccione la etiqueta padre, ya sea td o li, eso varia cuando se vuelve responsive
     var tr = tblClient.cell($(this).closest("td,li")).index(); // me devuelve la columna y row tambien
     
     // esto me va a devolver un diccionario con unos datos de la fila actual, en este caso el row para poner decirle en la variable data de que row o fila estraiga los valores
     //ya obtengo el row o fila y se la paso al row para que me traiga la data de toda esa linea
     var data = tblClient.row(tr.row).data();
     //le paso los valores al input para luego modificarlo
     $('input[name="id"]').val(data.id); // le pongo el id del cliente
     $('input[name="action"]').val("edit");
     $('input[name="names"]').val(data.names);
     $('input[name="surnames"]').val(data.surnames);
     $('input[name="dni"]').val(data.dni);
     $('input[name="date_birthday"]').val(data.date_birthday);
     $('input[name="address"]').val(data.address);
     $('select[name="gender"]').val(data.gender.id); // le pongo id porque esa es la opcion y ya el muestra en palabras la opcion
     $("#myModalClient").modal("show");
   })
     .on('click', 'a[rel="delete"]', function (e) { // le pueso aplicar otro .on pero le agregaria este evento a los botones de eliminar
       //obtengo los valores de la misma forma
      var tr = tblClient.cell($(this).closest("td,li")).index(); 
      var data = tblClient.row(tr.row).data();
      var parameters = new FormData();
       parameters.append("action","delete")
       parameters.append("id",data.id);
      submit_with_ajax(
        window.location.pathname,
        "Eliminar",
        `¿Desea eliminar el cliente ${data.names}?`,
        parameters,
        function () {
          $("#myModalClient").modal("hide");
          tblClient.ajax.reload(); // esta es una funcion de datatable, para no recargar toda la pagina
        }
      );
    })

  $("form").on("submit", function (e) {
    e.preventDefault();
    var parameters = new FormData(this);
    submit_with_ajax(
      window.location.pathname,
      "Guardar",
      `¿Desea guardar el cliente?`,
      parameters,
      function () {
        $("#myModalClient").modal("hide");
        tblClient.ajax.reload(); // esta es una funcion de datatable, para no recargar toda la pagina
      }
    );
  });
});