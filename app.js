const express = require('express');
const app = express();
const path = require('path');
const sequelize = require('./config/db');
const session = require('express-session'); // 1. Importar express-session

// Rutas

const bank_accountRoutes = require('./routes/bank_account.routes.js'); // Corregir el nombre del archivo de rutas

// Configuracion de express

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.urlencoded({ extended: false }));
app.use(express.json());

// 2. Configurar el middleware de sesión
app.use(session({
    secret: 'keyboard cat', // Cambia esto por un secreto más seguro en producción
    resave: false,
    saveUninitialized: false,
    cookie: { 
        secure: false, // Cambiar a true en producción con HTTPS
        maxAge: 24 * 60 * 60 * 1000 // 24 horas
    }
}));

// Middleware para hacer disponible el usuario en todas las vistas
app.use((req, res, next) => {
    res.locals.user = req.session.user || null;
    res.locals.isAuthenticated = !!req.session.user;
    next();
});

// Rutas de autenticación
app.get('/login', (req, res) => {
    if (req.session.user) {
        return res.redirect('/bank_accounts');
    }
    res.render('login', { error: req.query.error });
});

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    
    // Simulación de autenticación (en producción usarías una base de datos)
    if (username === 'admin' && password === '123456') {
        req.session.user = { 
            id: 1, 
            username: username,
            email: 'admin@example.com'
        };
        res.redirect('/bank_accounts');
    } else {
        res.redirect('/login?error=Credenciales inválidas');
    }
});

app.get('/logout', (req, res) => {
    req.session.destroy(err => {
        if (err) {
            console.error('Error al destruir la sesión:', err);
            return res.redirect('/bank_accounts');
        }
        res.clearCookie('connect.sid');
        res.redirect('/login');
    });
});

// Ruta para verificar estado de autenticación
app.get('/auth/status', (req, res) => {
    res.json({
        isAuthenticated: !!req.session.user,
        user: req.session.user || null
    });
});

// Activar rutas

app.use('/bank_accounts', bank_accountRoutes);

// Ruta raíz opcional
app.get('/', (req, res) => {
    res.redirect('/bank_accounts');
});
  
sequelize.sync({force: false})
.then(() => {
    console.log('Base de datos conectada y sincronizada');
    app.listen(3000, () => {
        console.log('Server corriendo en http://localhost:3000')
    });
})
.catch(err => {
    console.error('ERROR AL CONECTARSE') // Uso de logger xd
})