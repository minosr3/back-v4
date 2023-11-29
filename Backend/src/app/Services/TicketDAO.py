from ..Models import Ticket
from app import db

class TicketDAO():

    @classmethod
    def createTicket(self, data):
        try:
            nuevoTicket = Ticket(**data)
            db.session.add(nuevoTicket)
            db.session.commit()
            return nuevoTicket
        except Exception as ex:
            print(f"Error: {ex}")
            return Exception(ex)
    
    @classmethod
    def getTickets(self):
        try:
            allTickets = Ticket.query.all()

            tickets = []
            for ticket in allTickets:
                ticketJson = ticket.to_JSON()
                tickets.append(ticketJson)
            return tickets
        except Exception as ex:
            print(f"Error: {ex}")
            raise Exception(ex)

    @classmethod
    def getTicketById(self, id):
        try:
            ticket = Ticket.query.filter_by(id=id).first()
            if ticket is not None:
                return ticket
            else:
                return None
        except Exception as ex:
            print(f"Error: {ex}")
            raise Exception(ex)
    
    @classmethod
    def updateTicket(self, id, data):
        try:
            ticket = Ticket.query.filter_by(id=id).first()
            if ticket is not None:
                ticket.from_JSON(data)
                db.session.commit()
                ticket_json = ticket.to_JSON()
                return ticket_json
            else:
                return False
        except Exception as ex:
            print(f"Error: {ex}")
            raise Exception(ex)
        
    @classmethod
    def deleteTicket(self, id):
        try:
            ticket = Ticket.query.filter_by(id=id).first()
            db.session.delete(ticket)
            db.session.commit()
            return ticket
        except Exception as ex:
            print(f"Error: {ex}")
            return Exception(ex)