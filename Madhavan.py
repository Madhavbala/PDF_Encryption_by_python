#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Encrypting multiple pdf files

import PyPDF2
import tkinter
from tkinter import filedialog
import os
import sqlite3 as sql

def my_db_ex(db,file_name,password,current_time):
    try:
            db_connection = sql.connect(db)
            create_table = """CREATE TABLE IF NOT EXISTS pdf_info ("F_name" text, "F_password" text, "date_encryption" text)"""
            db_connection.execute(create_table)
            insert_query = f"""INSERT INTO pdf_info("F_name", "F_password", "date_encryption") values ("{file_name}",'{password}',"{current_time}")"""
            db_connection.execute(insert_query)
    except Exception as ex:
        print (ex)
    finally:
        db_connection.commit()
        db_connection.close()     
folder_list = os.listdir(r"C:\Users\madhavan.bala\Documents\Python Scripts") #Checking the pdf files in Sample PDF and storing them in folder_list
print(folder_list)


try:
    for files in folder_list:
        if files.endswith('.pdf'): #Fetching only pdf files which ends with ".pdf"
            print(files)
            file_path = os.path.join(r"C:\Users\madhavan.bala\Documents\Python Scripts",files)
            pdf_in_file = open(file_path, 'rb') #Converting content to machine readable language
            inputpdf = PyPDF2.PdfFileReader(pdf_in_file)
            if not inputpdf.isEncrypted:
                page_no = inputpdf.numPages    #Reading number of page numbers in the pdf file
                output = PyPDF2.PdfFileWriter()
                for i in range(page_no):   #Reading number of page numbers in the pdf file
                    inputpdf = PyPDF2.PdfFileReader(pdf_in_file)
                    from datetime import datetime
                    current_time = datetime.now().replace(microsecond = 0)
                    current_time = datetime.strftime(current_time,"%y_%m_%d_%H_%M_%S") #Changing format of current time
                    print(current_time)
                    print(type(current_time))
                    output.addPage(inputpdf.getPage(i))
                    output.encrypt(files[:-4] + current_time) #Creating password as filename with current time
                
                    output_file_name = "enc_pdf" + files[:-4] + current_time + ".pdf" #Modifying the password protected pdf file name 
                    output_file_path = os.path.join(r"C:\Users\madhavan.bala\Documents\Python Scripts",output_file_name) #Setting location for the encrypted file
                with open(output_file_path, "wb") as outputStream: #Converting file path to machine writable language
                    output.write(outputStream)
                with open(r"C:\Users\madhavan.bala\Sample\Password.txt","a") as file_obj: #Creating a new text file which will contain password for each pdf file
                    file_obj.write(files)
                    password = files[:-4] + current_time
                    file_obj.write(password)
                    file_obj.write("\n___________________________________________\n")
                    
                my_db_ex('pdf.db',files[:-4],password,current_time)   #Storing the credentials in pdf.db database
                    
        
except Exception as ex:
    print (ex)
finally:
    pdf_in_file.close()


# In[ ]:




