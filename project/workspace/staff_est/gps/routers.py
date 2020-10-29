#class GpsRouter(object): 
#    def db_for_read(self, model, **hints):
#        "Lee desde gps"
#        if model._meta.app_label == 'gps':
#            return 'gps'
#        return 'default'
#
#    def db_for_write(self, model, **hints):
#        "Escribe en default"
#        if model._meta.app_label == 'gps':
#            return 'default'
#        return 'default'
#    
##    def allow_relation(self, obj1, obj2, **hints):
##        "Allow any relation if a both models in chinook app"
##        if obj1._meta.app_label == 'chinook' and obj2._meta.app_label == 'chinook':
##            return True
##        # Allow if neither is chinook app
##        elif 'chinook' not in [obj1._meta.app_label, obj2._meta.app_label]: 
##            return True
##        return False
#    
#    def allow_syncdb(self, db, model):
#        if db == 'gps' or model._meta.app_label == "gps":
#            return False # we're not using syncdb on our legacy database
#        else: # but all other models/databases are fine
#            return True
