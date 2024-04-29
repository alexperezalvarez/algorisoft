$(function () {
  //selecciono la tabla por su id
  $("#data").DataTable({
    //le digo que si va a ser responsivo
    responsive: true,
    //que respete el ancho que yo le ponga
    autoWidth: false,
    //por si quiero reinicializar la tabla con otro proceso
    destroy: true,
    //hagiliza la crga de los datos si superan los 50k registros
    deferRender: true,

    ajax: {
      //le pongo a donde va a hacer la petición, que en este caso es a la misma vista
      url: window.location.pathname,
      type: "POST",
      //le paso los parametros
      data: {
        //nomas le paso la acción para pedir los datos
        action: "searchdata",
      },
      //como no meti los arreglos que pido a la vista en un diccionario donde vaya el arreglo, entonces dejo esto vacio, le pondria data si hubiera mandando los datos asi: data = {'data':[...todos los registros...]}
      dataSrc: "",
    },
    columns: [
      //estas son las columnas, como llegan los datos por diccionarios dentro del arreglo que DataTable recorre, entonces accedo a cada valor y duplico el ultimo porque tengo una columna de opciones
      { data: "id" },
      { data: "name" },
      { data: "desc" },
      //lo duplico para que aparezca otra columna, en este caso la de opciones
      { data: "desc" },
    ],
    columnDefs: [
      {
        //aqui personalizo cada columna o una en especifico
        //el -1 hace referencia a la ultima fila, si lo pusiera -2, al penultimo y asi, o de arriba hacia abajo iniciando con 0
        targets: [-1],
        class: "text-center",
        orderable: true,
        //data hace referencia al valor de la columna, si lo retorno, retornaria la descripción si la tiene, pero puedo retornar cualquier otra cosa, y el row hace referencia a todo el objeto, puedo accedes hasta el id, name, etc
        render: function (data, type, row) {
          //aqui mando lo que necesito en esa columna
          //en este caso, los botones de borrar y editar
          //como ya aqui no lo renderiza jinja, pongo la rutas como son, y sabemos que reciben ids, y gracias a row, puedo acceder a modo de diccionario al id correspondiente
          var botones = `<a href="/erp/category/update/${row.id}" class="btn btn-warning btn-xs"><i class="fas fa-edit"></i></a> `;
          botones += `<a href="/erp/category/delete/${row.id}" class="btn btn-danger btn-xs"><i class="fas fa-trash-alt"></i>`;
          return botones;
        },
      },
      //la otra modificacion es otro diccionario dentro del arreglo, osea, aqui
    ],
    //esto se ejecuta cuando la tabla se haya cargado
    initComplete: function (settings, json) {},
  });
});
//de esta forma los registros se cargan aun más rapido y eso que estoy utilizando la base de datos en la nube
