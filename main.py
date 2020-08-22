from gui import *
from db import insert_init_record,create_tables

if __name__ == "__main__":
    create_tables()  ###### SHOULD BE ACTIVE IN THE BIGENING  #######

    ######## INSERT RECORDS IN DB ########### SHOULD BE ACTIVE IN THE BIGNING ##########
    sql = """INSERT OR IGNORE INTO users(userid,username,password,firstname,lastname,age,city,gender,address) VALUES((SELECT IFNULL(MAX(userid), 0)+1 FROM users),'admin','admin','John','Smith','25','Toronto','M','1340 rue champigny')"""
    insert_init_record(sql)

    # Driver Code 
    app = tkinterApp() 
    app.mainloop() 
