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

    var materia = $(this).data('materia');

    $("#edit-id_profesor_dni").val(id_profesor_dni);
    $("#edit-nombre").val(nombre);
    $("#edit-apellido").val(apellido);

    $("#edit-materia").val(materia);

    // Configurar la acción del formulario para incluir el ID del alumno
    $("#editForm").attr("action", "/profesores/edit/" + id_profesor_dni);
});
