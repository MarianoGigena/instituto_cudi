
// Script para pasar el ID al modal de eliminación
$(document).on("click", ".delete-btn", function () {
    var id_alumno = $(this).data("id");
    $("#deleteForm").attr("action", "/alumnos/delete/" + id_alumno);
});

// Script para pasar datos al modal de edición
$(document).on("click", ".edit-btn", function () {
    var id_alumno = $(this).data('id_alumno');
    var nombre = $(this).data('nombre');
    var apellido = $(this).data('apellido');
    var dni = $(this).data('dni');
    var fecha_nacimiento = $(this).data('fecha_nacimiento');
    var genero = $(this).data('genero');

    $("#edit-id_alumno").val(id_alumno);
    $("#edit-nombre").val(nombre);
    $("#edit-apellido").val(apellido);
    $("#edit-dni").val(dni);
    $("#edit-fecha_nacimiento").val(fecha_nacimiento);
    $("#edit-genero").val(genero);

    // Configurar la acción del formulario para incluir el ID del alumno
    $("#editForm").attr("action", "/alumnos/edit/" + id_alumno);
});
