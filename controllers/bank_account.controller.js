const { Bank_Account } = require('../models');

// Crear - CREATE

exports.formCreate = (req, res) => {
    res.render('bank_accounts/create');
};

exports.create = async (req, res) => {
    await Bank_Account.create(req.body);
    res.redirect('/bank_accounts');
};

// Listar - SELECT - Read

exports.list = async (req, res) => {
    const bank_accounts = await Bank_Account.findAll();
    res.render('bank_accounts/index', {
      bank_accounts,
      error: req.query.error
    });
  };
  
exports.viewOne = async (req, res) => {
    const phone = req.params.phone_number;
    try {
      const bank_accounts = await Bank_Account.findOne({
        where: { phone_number: phone }
      });
      if (!bank_accounts) {
        return res.redirect('/bank_accounts?error=Cuenta no encontrada');
      }
      res.render('bank_accounts/show', {
        bank_accounts
      });
    } catch (err) {
      console.error(err);
      res.redirect('/bank_accounts?error=Error interno');
    }
  };

// Actualizar - UPDATE

exports.formEdit = async (req, res) => {
    const bank_account = await Bank_Account.findByPk(req.params.id);
    res.render('bank_accounts/editar', { bank_account });
};

exports.edit = async (req, res) => {
    await Bank_Account.update(req.body, {
        where: {phone_number: req.params.id}
    });
    res.redirect('/bank_accounts') // Preguntarle al chalan si esto redirige automaticamente al ser completada la op. intuyo que si xd
};

// Eliminar - DELETE

exports.delete = async (req, res) => {
    try {
        await Bank_Account.destroy({ where: { phone_number: req.params.id } });
        res.redirect('/bank_accounts')
    }
    catch (error) {
        if (error.parent && error.parent.errno === 1451) { // Esto es un error relacionado a la foreign key
            res.redirect('/bank_accounts?errno=relacion')
        } else {
            res.redirect('/bank_accounts?errno=desconocido')
        }
    }
};