pip install  kaggle
import kaggle
!kaggle datasets download ankitbansal06/retail-orders -f orders.csv

#extract file from zip file
import zipfile
zip_ref = zipfile.ZipFile('orders.csv.zip') 
zip_ref.extractall() # extract file to dir
zip_ref.close() # close file

#read data from the file and handle null values
import pandas as pd
df = pd.read_csv('orders.csv',na_values=['Not Available','unknown']) #'Not Available','unknown' will also be treated as nan
df['Ship Mode'].unique()

#rename columns names ..make them lower case and replace space with underscore
df.columns=df.columns.str.lower() # convert all column into lower case
df.columns=df.columns.str.replace(' ','_') # replace all space to _

#derive new columns discount , sale price and profit
df['discount']=df['list_price']*df['discount_percent']*.01
df['sale_price']= df['list_price']-df['discount']
df['profit']=df['sale_price']-df['cost_price']

#convert order date from object data type to datetime
df['order_date']=pd.to_datetime(df['order_date'],format="%Y-%m-%d")

#drop cost price list price and discount percent columns
df.drop(columns=['list_price','cost_price','discount_percent'],inplace=True)

#connecting to oracle database
pip install cx_Oracle
pip install oracledb

#load the data into oracle sql server

import sqlalchemy as sal
import cx_Oracle
from sqlalchemy.dialects.oracle import (
                                        FLOAT,
                                        NUMBER,
                                        VARCHAR2,
                                        DATE
                                        )

#connecting to database (oracle)
engine = sal.create_engine('oracle+oracledb://system:admin@localhost:1521/?service_name=XEPDB1')
conn = engine.connect()

#converting datatypes from float to int (due to some incomaptiability error.
import numpy as np
df['discount'] = df['discount'].astype(np.int64)
df['sale_price'] = df['sale_price'].astype(np.int64)
df['profit'] = df['profit'].astype(np.int64)


#load the data into sql server using append option
df.to_sql('df_orders', con=conn , index=False, if_exists = 'append')

