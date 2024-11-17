
// Script para pasar datos al modal de calificación
$(document).on("click", ".calificar-btn", function () {
    var id_alumno_dni = $(this).data('id_alumno_dni');
    var id_materia = $(this).data('id_materia');
    console.log("ID Alumno: ", id_alumno_dni);
    console.log("ID Materia: ", id_materia);

    $("#calificar-id_alumno_dni").val(id_alumno_dni);
    $("#calificar-id_materia").val(id_materia);

    // Cambiar la acción del formulario para incluir los IDs
    $("#calificarForm").attr("action", "/cursos/calificar/" + id_alumno_dni + "/" + id_materia);

});

// Script para pasar datos al modal de calificación
$(document).on("click", ".calificar-btn2", function () {
    var id_alumno_dni = $(this).data('id_alumno_dni');
    var id_materia = $(this).data('id_materia');
    console.log("ID Alumno: ", id_alumno_dni);
    console.log("ID Materia: ", id_materia);

    $("#calificar-id_alumno_dni2").val(id_alumno_dni);
    $("#calificar-id_materia2").val(id_materia);

    // Cambiar la acción del formulario para incluir los IDs
    $("#calificarForm2").attr("action", "/cursos/calificar2/" + id_alumno_dni + "/" + id_materia);

});

$(document).on("click", ".actualizar-nota-btn", function () {
    var id_alumno_dni = $(this).data('id_alumno_dni');
    var id_materia = $(this).data('id_materia');
    $.ajax({
        url: "/cursos/actualizar_nota_final/" + id_alumno_dni + "/" + id_materia,
        type: "POST",
        success: function (response) {
            console.log("Nota final actualizada correctamente.");
            // Puedes añadir lógica aquí para actualizar la interfaz si es necesario
            location.reload(); // Recarga la página para ver los cambios
        },
        error: function (error) {
            console.error("Error al actualizar la nota final: ", error);
        }
    });
});

document.querySelectorAll('.delete-btn').forEach(button => {
    button.addEventListener('click', function () {
        const alumnoDni = this.dataset.id_alumno_dni;
        const materiaId = this.dataset.id_materia;
        const materia = this.dataset.materia;

        document.getElementById('delete-alumno-dni').value = alumnoDni;
        document.getElementById('delete-materia-id').value = materiaId;
        document.getElementById('delete-materia').value = materia;
    });
});

