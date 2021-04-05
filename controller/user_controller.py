import requests
import json
from flask import render_template, Blueprint, request, redirect
from model.user import User, Role
from flask_login.utils import login_required
from login.decorators import admin_login_required

TEMPLATE = './templates'
STATIC = './static'

user_controller = Blueprint('users', __name__, static_url_path='', template_folder=TEMPLATE, static_folder=STATIC)

@user_controller.route("/userForm")
@login_required
def userForm():
  return render_template("users/user.html", roles=Role.query.all())


@user_controller.route("/users", methods=['POST'])
@login_required
def add_user():
  name = request.form.get('name')
  email = request.form.get('email')
  password = request.form.get('password')
  roles = request.form.get('roles')
  jobTitle = " "
  user = User(email, name, jobTitle, password, [Role.query.filter_by(id=roles[0]).first()])
  user.save()

  return redirect("/users")

@user_controller.route("/roles", methods=['POST'])
@login_required
def add_role():
  name = request.form.get('name')
  description = request.form.get('description')
  
  role = Role(name, description)
  role.save()

  return redirect("/roles")

@user_controller.route("/roles")
@login_required
def roles():
  roles = Role.query.all()
  return render_template("users/roles.html", roles=roles)

@user_controller.route("/roleForm")
@login_required
def roleForm():
  return render_template("users/role.html")

@user_controller.route("/prods")


def searchItem():
  HEADERS = {
      "appToken": 'e9effe67cce2734de8b940060eb088cf9a95f7d5',
      "Content-Type": "application/json"
  }

  URL = 'http://api.sefaz.al.gov.br/sfz_nfce_api/api/public/consultarPrecosPorDescricao'

  data = {
    "descricao": "coca",
    "dias": 3,
    "latitude": -9.6432331,
    "longitude": -35.7190636,
    "raio": 15
  }

  r = requests.post(url= URL, data=json.dumps(data), headers = HEADERS)
  result = r.json()

  lista_prods = []

  for i in range(10):
    produto = {
      'nome_prod': result[i]["dscProduto"],
      'nome_loja': result[i]["nomRazaoSocial"],
      'bairro': result[i]["nomBairro"],
      'valor': result[i]["valUnitarioUltimaVenda"]
    }

    lista_prods.append(produto)
    
  return render_template("users/prods.html", users=lista_prods)
