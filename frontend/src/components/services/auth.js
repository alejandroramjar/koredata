export function isAuthenticated() {
  // Lógica para verificar si el usuario está autenticado
  return !!localStorage.getItem('token'); // Cambia 'user-token' por el nombre de tu token
}
