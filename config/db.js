// Conector hacia PostgreSQL (Local)

const { Sequelize } = require('sequelize');

// TODO: Agregar variables de entorno para la conexión a la DB
const sequelize = new Sequelize('cobrandola', 'feradmin', 'feradmin123', {
    host: '127.0.0.1',
    dialect: 'postgres',
    logging: console.log // false para desactivar logs en consola de la DB
});

module.exports = sequelize;

// TO-DO

// Implementar conexion a RDS y configurar todo con DOTENV