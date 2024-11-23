// Función para cargar las materias no inscritas y abrir el modal
function cargarMateriasNoInscritas(dni, nombre) {
    $.ajax({
        url: `/obtener_materias_no_inscritas/${dni}`,
        method: "GET",
        success: function (data) {
            // Limpiar cualquier opción previa en el select
            $('#materia').empty();

            // Agregar las opciones de materias al select
            data.forEach(function (materia) {
                $('#materia').append(`<option value="${materia.id_materia}">${materia.id_materia} - ${materia.nombre}</option>`);
            });

            // Asignar el DNI al campo oculto
            $('#alumnos_id_alumno_dni').val(dni);
            $('#nombre_alumno').val(nombre);

            // Mostrar el modal con las materias
            $('#inscribirModal').modal('show');
        },
        error: function (error) {
            console.error("Error al obtener las materias:", error);
            alert("Hubo un problema al cargar las materias.");
        }
    });
}

$('.btnInscribir').click(function () {
    var dni = $(this).data('dni');
    var nombre = $(this).data('nombre_alumno');  // Obtén el DNI del atributo data-dni del botón
    cargarMateriasNoInscritas(dni, nombre);  // Llama la función pasando el DNI correcto
});

$('#inscribirModal').on('hidden.bs.modal', function () {
    // Eliminar cualquier clase que esté bloqueando la interfaz
    $('.modal-backdrop').remove();
    $('body').removeClass('modal-open');
});