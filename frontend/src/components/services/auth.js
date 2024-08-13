// src/services/auth.js

export function isAuthenticated() {
  // Lógica para verificar si el usuario está autenticado
  // Esto puede ser una verificación de token en localStorage, por ejemplo
  return !!localStorage.getItem('token'); // Cambia 'user-token' por el nombre de tu token
}
