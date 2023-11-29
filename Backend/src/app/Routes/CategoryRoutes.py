from ..Models import Category
from ..Services import CategoryDAO, Calculator
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from ..utils import db, loginManagerApp
from ..utils import Security


categoriesMain = Blueprint('categoryBlueprint', __name__)

@categoriesMain.route('/categories/', methods=['GET', 'POST'])
def handleCategories():
    try:
        print(request.method)
        if request.method == 'POST':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                data = request.json
                result = CategoryDAO.createCategory(data)
                if isinstance(result, Category):  
                    return jsonify({'message': 'Operación POST exitosa'}), 201
                else:
                    return jsonify({'message': 'Error desconocido'}), 500
        elif request.method == 'GET':
            categories = CategoryDAO.getCategories()
            return jsonify(categories), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@categoriesMain.route('/category/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handleCategoryById(id):
    hasAccess=Security.verifyToken(request.headers)
    if hasAccess:
        try:
            if request.method == 'GET':
                category = CategoryDAO.getCategoryById(id)

                if category is not None:
                    if isinstance(category, Category):
                        categoryJSON = category.to_JSON()
                        return jsonify(categoryJSON), 200
                    else:
                        return jsonify({'message': str(ex)}), 500
                    
                else:
                    return jsonify({'message': 'Category no encontrado'}), 404
            elif request.method == 'PUT':
                hasAccess = Security.verifyToken(request.headers, required_role=3)
                if hasAccess:
                    data = request.json
                    print(data)
                    category = CategoryDAO.getCategoryById(id, data)
                    if category is not None:
                        return jsonify({'message': 'Category actualizado con éxito'}), 200
                    else:
                        return jsonify({'message': 'Category no encontrado'}), 404
                else: 
                    return jsonify({'message': 'Unauthorized'}), 401
            elif request.method == 'DELETE':
                hasAccess = Security.verifyToken(request.headers, required_role=3)
                if hasAccess:
                    category = CategoryDAO.getCategoryById(id)
                    if category is not None:
                        # Llama a la función que elimina al category
                        is_deleted = CategoryDAO.deleteCategory(id)
                        if is_deleted:
                            return jsonify({'message': 'Category eliminado con éxito'}), 200
                        else:
                            return jsonify({'message': 'No se pudo eliminar al category'}), 500
                    else:
                        return jsonify({'message': 'Category no encontrado'}), 404
                else: 
                    return jsonify({'message': 'Unauthorized'}), 401
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else: 
        return jsonify({'message': 'Unauthorized'}), 401
