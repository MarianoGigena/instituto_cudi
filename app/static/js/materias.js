// Script para pasar datos al modal de edición
$(document).on("click", ".edit-btn", function () {
    var id_materia = $(this).data('id_materia');
    var nombre = $(this).data('nombre');


    $("#edit-id_materia").val(id_materia);
    $("#edit-nombre").val(nombre);

    // Configurar la acción del formulario para incluir el ID del alumno
    $("#editForm").attr("action", "/materias/edit/" + id_materia);
});

// Script para pasar el ID al modal de eliminación
$(document).on("click", ".delete-btn", function () {
    var id_materia = $(this).data("id");
    $("#deleteForm").attr("action", "/materias/delete/" + id_materia);
});