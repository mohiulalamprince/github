#!/usr/bin/env python

import xlrd
from xlrd import cellname
import _mysql
import sys

book = xlrd.open_workbook("G:\\projecttrackeranddatabase\\test\\test.xlsx")

fp = open("E:\\out.txt", "w")

con = None

try:

    con = _mysql.connect('localhost', 'root', 
        'a', 'managementsoftdb')
        
    con.query("create table if not exists FinancialStatus(idpk int primary key auto_increment, \
              SLNo int, PONumber varchar(30), \
              Scope varchar(40), POValue double, InvoiceIst double, \
              Invoice2nd double, PaymentReceivedIst double, \
              PaymentReceived2nd double, ActualPaymentReceived double, \
              Remarks varchar(50), CompanyName varchar(25) )")
    
except _mysql.Error, e:
  
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    
    if con:
        con.close()

cnt = 0
for sheet_name in book.sheet_names():
   sheet = book.sheet_by_name(sheet_name)
   print sheet.nrows
   print sheet.ncols
   cnt = cnt + 1
   if (cnt == 2):
        break
   
   for row_index in range(sheet.nrows):
        strdata = "Insert into FinancialStatus(SLNo, PONumber, \
              Scope, POValue, InvoiceIst, \
              Invoice2nd, PaymentReceivedIst, \
              PaymentReceived2nd, ActualPaymentReceived, \
              Remarks , CompanyName)) values("
        for col_index in range(sheet.ncols):
            if (col_index == 0):
                if (str(sheet.cell(row_index,col_index).value) == ""):
                    strdata = strdata + "null"
                else:
                    strdata = strdata + "" +str(sheet.cell(row_index,col_index).value)
            else:
                if (str(sheet.cell(row_index,col_index).value) == ""):
                    strdata = strdata + ",null"
                else:
                    strdata = strdata + "," +str(sheet.cell(row_index,col_index).value)
        print strdata + ")"
        fp.write(strdata + ")\n")
        
        con = None
        try:
            con = _mysql.connect('localhost', 'root', 
                'a', 'managementsoftdb')
            con.query(strdata)
        
        except _mysql.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)

        finally:
            if con:
                con.close()
