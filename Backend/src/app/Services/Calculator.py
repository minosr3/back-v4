from warnings import catch_warnings
from ..Models import Distributor
from .CategoryDAO import CategoryDAO
from .DistributorDAO import DistributorDAO
from app import db

class Calculator():

    @classmethod
    def calcular_comision(self, domain):
        try: 
            distribuidor = DistributorDAO.getDistributorById(domain.distributor_id)
            print(distribuidor)

            if distribuidor is not None:
                if isinstance(distribuidor, Distributor):
                    distribuidorCategory = distribuidor.category_id
                    commission = CategoryDAO.getCategoryById(distribuidorCategory)
                    print(commission.commission)
                    commission = commission.commission
                    commission = commission/100
                    print(commission)
                    venta = domain.costDomain * commission
                    print(domain.costDomain)
                    print(venta)
                    return venta
                else:
                    print ("error get comision")
                    return 0.0
            else: 
                print ("error 010")
                return 0.0
        except Exception as ex:
            print ("error 011")
            return 0.0
        
    @classmethod
    def calcular_precioFinalDomains(self, domains):
        try: 
            finalCostDomains = 0
            for domain in domains:
                finalCostDomains += domain.costDomain
            return finalCostDomains
        except Exception as ex:
            print ("error 012")
            return 0.0
        
    @classmethod
    def calcular_precioFinalHostings(self, hostings):
        try: 
            finalCostHosting = 0
            for hosting in hostings:
                finalCostHosting += hosting.plan.cost_per_year
            return finalCostHosting
        except Exception as ex:
            print ("error 013")
            return 0.0
