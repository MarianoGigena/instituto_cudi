
// Script para pasar el ID al modal de eliminación
$(document).on("click", ".delete-btn", function () {
    var id_alumno_dni = $(this).data("id");
    $("#deleteForm").attr("action", "/alumnos/delete/" + id_alumno_dni);
});

// Script para pasar datos al modal de edición
$(document).on("click", ".edit-btn", function () {
    var id_alumno_dni = $(this).data('id_alumno_dni');
    var nombre = $(this).data('nombre');
    var apellido = $(this).data('apellido');

    var fecha_nacimiento = $(this).data('fecha_nacimiento');
    var genero = $(this).data('genero');

    $("#edit-id_alumno_dni").val(id_alumno_dni);
    $("#edit-nombre").val(nombre);
    $("#edit-apellido").val(apellido);

    $("#edit-fecha_nacimiento").val(fecha_nacimiento);
    $("#edit-genero").val(genero);

    // Configurar la acción del formulario para incluir el ID del alumno
    $("#editForm").attr("action", "/alumnos/edit/" + id_alumno_dni);
});


/* $('#inscribirModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Botón que activa el modal
    var dni = button.data('dni'); // Extrae el DNI del atributo data-dni
    var modal = $(this);
    modal.find('#alumnos_id_alumno_dni').val(dni); // Establece el DNI en el campo oculto
}); */


/* $('#inscribirModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);  // Botón que activó el modal
    var idAlumno = button.data('id_alumno_dni');  // Extrae el ID del alumno

    var modal = $(this);
    modal.find('#alumnos_id_alumno_dni').val(idAlumno);  // Inserta el ID en el campo oculto
}); */
