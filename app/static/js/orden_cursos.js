/* let ordenAscendente = true;  // Variable para controlar la dirección del orden (ascendente o descendente)

function ordenarTabla(columna) {
    const tabla = document.getElementById("tablaInscripciones");
    const filas = Array.from(tabla.querySelectorAll("tbody tr"));

    // Función para obtener el valor de la celda dependiendo de la columna
    const obtenerValorCelda = (fila, columna) => {
        return fila.children[columna].innerText || fila.children[columna].textContent;
    };

    // Ordenar las filas basándonos en el valor de la columna seleccionada
    filas.sort((filaA, filaB) => {
        const valorA = obtenerValorCelda(filaA, columna);
        const valorB = obtenerValorCelda(filaB, columna);

        // Comparamos los valores
        if (ordenAscendente) {
            return valorA > valorB ? 1 : -1;  // Orden ascendente
        } else {
            return valorA < valorB ? 1 : -1;  // Orden descendente
        }
    });

    // Vaciamos el cuerpo de la tabla y agregamos las filas ordenadas
    tabla.querySelector("tbody").innerHTML = "";
    filas.forEach(fila => tabla.querySelector("tbody").appendChild(fila));

    // Cambiar el estado del orden para la próxima vez
    ordenAscendente = !ordenAscendente;
} */
let ordenAscendente = true; // Variable para controlar la dirección del orden (ascendente o descendente)

// Función para verificar si un valor es numérico
function isNumber(value) {
    return !isNaN(parseFloat(value)) && isFinite(value);
}

function ordenarTabla(columna) {
    const tabla = document.getElementById("tablaInscripciones");
    const filas = Array.from(tabla.querySelectorAll("tbody tr"));

    // Función para obtener el valor de la celda dependiendo de la columna
    const obtenerValorCelda = (fila, columna) => {
        return fila.children[columna].innerText || fila.children[columna].textContent;
    };

    // Ordenar las filas basándonos en el valor de la columna seleccionada
    filas.sort((filaA, filaB) => {
        let valorA = obtenerValorCelda(filaA, columna);
        let valorB = obtenerValorCelda(filaB, columna);

        // Verificar si ambos valores son números
        if (isNumber(valorA) && isNumber(valorB)) {
            valorA = parseFloat(valorA);
            valorB = parseFloat(valorB);
        }

        // Comparar valores según el tipo
        if (ordenAscendente) {
            return valorA > valorB ? 1 : -1; // Orden ascendente
        } else {
            return valorA < valorB ? 1 : -1; // Orden descendente
        }
    });

    // Vaciamos el cuerpo de la tabla y agregamos las filas ordenadas
    tabla.querySelector("tbody").innerHTML = "";
    filas.forEach(fila => tabla.querySelector("tbody").appendChild(fila));

    // Cambiar el estado del orden para la próxima vez
    ordenAscendente = !ordenAscendente;
}
