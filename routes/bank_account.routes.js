const express = require('express');
const router = express.Router();
const ctrl = require('../controllers/bank_account.controller');
const { isAuthenticated } = require('../middleware/auth'); // <-- 1. Importar el middleware

// --- Rutas Públicas ---
// La ruta de listar es pública
router.get('/', ctrl.list);

// --- Rutas Privadas (requieren autenticación) ---
// Aplicar el middleware a las rutas que requieren autenticación
router.use(isAuthenticated);

router.get('/create', ctrl.formCreate);
router.post('/create', ctrl.create);
router.get('/edit/:id', ctrl.formEdit);
router.post('/edit/:id', ctrl.edit);
router.get('/delete/:id', ctrl.delete);
router.get('/:phone_number', ctrl.viewOne);

module.exports = router;