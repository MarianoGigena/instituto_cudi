// Script para pasar el ID al modal de eliminación
$(document).on("click", ".delete-btn", function () {
    var id_profesor_dni = $(this).data("id");
    $("#deleteForm").attr("action", "/profesores/delete/" + id_profesor_dni);
});

// Script para pasar datos al modal de edición
$(document).on("click", ".edit-btn", function () {
    var id_profesor_dni = $(this).data('id_profesor_dni');
    var nombre = $(this).data('nombre');
    var apellido = $(this).data('apellido');
    var id_materia = $(this).data('id_materia');
    var materia = $(this).data('materia');
    console.log("Materia: ", materia)
    console.log("id_Materia: ", id_materia)

    $("#edit-id_profesor_dni").val(id_profesor_dni);
    $("#edit-nombre").val(nombre);
    $("#edit-apellido").val(apellido);

    /* $("#edit-materia").val(materia);
    $("#edit-materia2").val(materia); */

    $("#edit-materia").val(id_materia); // Establecer el valor por defecto en el select
    $("#edit-materia2").val(id_materia);
    // Configurar la acción del formulario para incluir el ID del profesor
    $("#editForm").attr("action", "/profesores/edit/" + id_profesor_dni);
});
