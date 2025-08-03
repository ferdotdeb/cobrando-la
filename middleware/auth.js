// middleware/auth.js

// Este es un middleware de ejemplo.
// En una aplicación real, aquí verificarías la sesión o un token JWT.
const isAuthenticated = (req, res, next) => {
  // Por ahora, simularemos que un usuario está autenticado si existe
  // una propiedad 'user' en el objeto de sesión.
  if (req.session && req.session.user) {
    // Si el usuario está autenticado, permite que la solicitud continúe
    // hacia el siguiente middleware o el controlador final.
    return next();
  }

  // Si el usuario no está autenticado, redirígelo a la página de login.
  res.redirect('/login');
};

module.exports = {
  isAuthenticated,
};
