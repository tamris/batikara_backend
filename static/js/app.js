document.addEventListener("DOMContentLoaded", function () {
  const flashContainer = document.getElementById("flash-container");

  if (flashContainer) {
    const category = flashContainer.dataset.category;
    const message = flashContainer.dataset.message;

    Swal.fire({
      toast: true,
      position: 'top-end',
      icon: category,
      title: message,
      showConfirmButton: false,
      timer: 2000,
      timerProgressBar: true,
      didClose: () => {
        // ✅ Jika login berhasil, redirect ke dashboard
        if (category === 'success' && message === 'Login berhasil!') {
          window.location.href = "/admin/dashboard";
        }
        // ✅ Jika logout berhasil, redirect ke halaman login
        if (category === 'info' && message === 'Anda berhasil logout.') {
          window.location.href = "/login";
        }
      }
    });
  }
});
