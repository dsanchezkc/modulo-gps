function checkRut(rut) {
    // Despejar Puntos
    var valor = rut.value.replace('.', '');
    // Despejar Guión
    valor = valor.replace('-', '');

    // Aislar Cuerpo y Dígito Verificador
    cuerpo = valor.slice(0, -1);
    dv = valor.slice(-1).toUpperCase();

    if (rut.value.length == 0) return true;

    // Formatear RUN
    rut.value = cuerpo + '-' + dv

    // Si no cumple con el mínimo ej. (n.nnn.nnn)
    //if (cuerpo.length < 7) { toastr.error("El rut no cumple con el largo mínimo"); return false; }

    // Calcular Dígito Verificador
    suma = 0;
    multiplo = 2;

    // Para cada dígito del Cuerpo
    for (i = 1; i <= cuerpo.length; i++) {

        // Obtener su Producto con el Múltiplo Correspondiente
        index = multiplo * valor.charAt(cuerpo.length - i);

        // Sumar al Contador General
        suma = suma + index;

        // Consolidar Múltiplo dentro del rango [2,7]
        if (multiplo < 7) { multiplo = multiplo + 1; } else { multiplo = 2; }

    }

    // Calcular Dígito Verificador en base al Módulo 11
    dvEsperado = 11 - (suma % 11);

    // Casos Especiales (0 y K)
    dv = (dv == 'K') ? 10 : dv;
    dv = (dv == 0) ? 11 : dv;

    // Validar que el Cuerpo coincide con su Dígito Verificador
    if (dvEsperado != dv) { toastr.error("El rut ingresado es inválido"); rut.focus(); }

}

function clearForms() {
    $(':input').not(':button, :submit, :reset, :hidden, :checkbox, :radio').val('');
    $(':checkbox, :radio').prop('checked', false);
    $('#id').val('');
}



function desvincular() {
    Swal.fire({
        title: 'Esta seguro?',
        text: "Esta acción no podrá revertirse",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, desvincular'
    }).then((result) => {
        if (result.value) {
            $('#trabajador-desvincular').submit();
        }
    });
}

function reprocesar() {
    Swal.fire({
        title: 'Esta seguro?',
        text: "Esta acción no podrá revertirse",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si'
    }).then((result) => {
        if (result.value) {
            $('#trabajador-reprocesar').submit();
        }
    });
}
$(document).ready(function () {
    $('.datepicker').datepicker({
        format: "dd-mm-yyyy",
        language: "es",
        autoclose: true
    });
});