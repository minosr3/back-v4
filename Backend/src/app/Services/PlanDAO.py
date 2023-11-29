from ..Models import Plan
from app import db

class PlanDAO():

    @classmethod
    def createPlan(self, data):
        try:
            nuevoPlan = Plan(**data)
            db.session.add(nuevoPlan)
            db.session.commit()
            return nuevoPlan
        except Exception as ex:
            print("error")
            return Exception(ex)
    
    @classmethod
    def getPlans(self):
        try:
            allPlans = Plan.query.all()
            plans = []
            for plan in allPlans:
                planJson = plan.to_JSON()
                plans.append(planJson)
            return plans
        except Exception as ex:
            print("error")
            raise Exception(ex)

    @classmethod
    def getPlanById(self, id):
        try:
            plan = Plan.query.filter_by(id=id).first()
            if plan is not None:
                return plan
            else:
                return None
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
    
    @classmethod
    def updatePlan(self, id, data):
        try:
            plan = Plan.query.filter_by(id=id).first()
            if plan is not None:
                plan.from_JSON(data)
                db.session.commit()
                plan_json = plan.to_JSON()
                return plan_json
            else:
                return False
        except Exception as ex:
            print("error 404")
            raise Exception(ex)
        
    @classmethod
    def deletePlan(self, id):
        try:
            plan = Plan.query.filter_by(id=id).first()
            db.session.delete(plan)
            db.session.commit()
            return plan
        except Exception as ex:
            print("error")
            return Exception(ex)