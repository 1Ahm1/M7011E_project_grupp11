import Swal from 'sweetalert2';

export function success(message: string = '') {
    Swal.fire({
        title: "Success",
        text: message,
        icon: "success",
      });   
}

export function fail(message: string = '') {
    Swal.fire({
        title: "Error",
        text: message,
        icon: "error",
      });
}