from ..Models import Ticket
from ..Services import TicketDAO
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from ..utils import db, loginManagerApp
from ..utils import Security

ticketsMain = Blueprint('ticketBlueprint', __name__)

@ticketsMain.route('/tickets/', methods=['GET', 'POST'])
def handleTickets():
    try:
        print(request.method)
        if request.method == 'POST':
            
            hasAccess=Security.verifyToken(request.headers)
            if hasAccess:
                data = request.json
                print(data)
                result = TicketDAO.createTicket(data)
                if isinstance(result, Ticket):  
                    return jsonify({'message': 'Operación POST exitosa'}), 201
                else:
                    return jsonify({'message': 'Error desconocido'}), 500
            else: 
                return jsonify({'message': 'Unauthorized'}), 401
        elif request.method == 'GET':
            tickets = TicketDAO.getTickets()
            return jsonify(tickets), 200
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    


@ticketsMain.route('/ticket/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handleTicketById(id):
    try:
        if request.method == 'GET':
            ticket = TicketDAO.getTicketById(id)
            if ticket is not None:
                if isinstance(ticket, Ticket):
                    ticketJSON = ticket.to_JSON()
                    return jsonify(ticketJSON), 200
                else:
                    return jsonify({'message': str(ex)}), 500
                
            else:
                return jsonify({'message': 'Ticket no encontrado'}), 404
        elif request.method == 'PUT':
            hasAccess = Security.verifyToken(request.headers, required_role=2)
            if hasAccess:
                data = request.json
                print(data)
                ticket = TicketDAO.uptadeTicket(id, data)
                if ticket is not None:
                    return jsonify({'message': 'Ticket actualizado con éxito'}), 200
                else:
                    return jsonify({'message': 'Ticket no encontrado'}), 404
            else: 
                return jsonify({'message': 'Unauthorized'}), 401
        elif request.method == 'DELETE':
            hasAccess = Security.verifyToken(request.headers, required_role=3)
            if hasAccess:
                ticket = TicketDAO.getTicketById(id)
                if ticket is not None:
                    # Llama a la función que elimina al ticket
                    is_deleted = TicketDAO.deleteTicket(id)
                    if is_deleted:
                        return jsonify({'message': 'Ticket eliminado con éxito'}), 200
                    else:
                        return jsonify({'message': 'No se pudo eliminar al ticket'}), 500
                else:
                    return jsonify({'message': 'Ticket no encontrado'}), 404
            else: 
                return jsonify({'message': 'Unauthorized'}), 401
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

