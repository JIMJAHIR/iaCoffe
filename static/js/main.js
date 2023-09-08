// Espera a que el documento HTML esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
  // Obtén referencias a los elementos HTML
  const imageInput = document.querySelector('input[type="file"]');
  const imageElement = document.getElementById('image');
  const resultElement = document.getElementById('result');

  // Maneja el evento de cambio de input de archivo (cuando se carga una imagen)
  imageInput.addEventListener('change', function() {
      // Obtén la imagen cargada
      const file = imageInput.files[0];

      if (file) {
          // Crea una URL del objeto File para mostrar la imagen en la página
          const imageURL = URL.createObjectURL(file);
          imageElement.src = imageURL;
          imageElement.style.display = 'block'; // Muestra la imagen

          // Limpia el resultado anterior
          resultElement.textContent = '';

          // Desplázate automáticamente hacia la imagen
          window.scrollTo(0, imageElement.offsetTop);

          // Opcional: Envía la imagen al servidor para la predicción
          // (Implementa esto en la comunicación con el servidor Flask)
          // Aquí puedes realizar una solicitud POST al servidor Flask con la imagen.
      }
  });
});
