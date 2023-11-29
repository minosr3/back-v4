from app import createApp, db

app = createApp('development')

from app.Routes.UsersRoutes import userMain
from app.Routes.authRoutes import authMain
from app.Routes.TicketsRoutes import ticketsMain
from app.Routes.DistributorRoutes import distributorsMain
from app.Routes.HostingRoutes import hostingsMain
from app.Routes.DomainRoutes import domainsMain
from app.Routes.BuyoutRoutes import buyoutsMain
from app.Routes.CategoryRoutes import categoriesMain
from app.Routes.CountryRoutes import countriesMain
from app.Routes.PayModeRoutes import payModesMain
from app.Routes.PayPlanRoutes import payPlansMain
from app.Routes.PlanRoutes import plansMain
from app.Routes.PlatformRoutes import platformsMain
from app.Routes.RolRoutes import rolsMain
from app.Routes.CreditCardRoute import creditCardsMain

app.register_blueprint(userMain)
app.register_blueprint(authMain)
app.register_blueprint(ticketsMain)
app.register_blueprint(distributorsMain)
app.register_blueprint(hostingsMain)
app.register_blueprint(domainsMain)
app.register_blueprint(buyoutsMain)
app.register_blueprint(categoriesMain)
app.register_blueprint(countriesMain)
app.register_blueprint(payModesMain)
app.register_blueprint(payPlansMain)
app.register_blueprint(plansMain)
app.register_blueprint(platformsMain)
app.register_blueprint(rolsMain)
app.register_blueprint(creditCardsMain)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 

    app.run()



