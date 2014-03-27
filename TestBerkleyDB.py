
try:
    from bsddb import db
except ImportError:
    from bsddb3 import db
    print "Error"

print db.DB_VERSION_STRING
