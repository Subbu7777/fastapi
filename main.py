from fastapi import FastAPI,UploadFile,File,Query,HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import aiofiles
from typing import Optional
import os 
import json
from typing import List
import yaml
import time
import shutil


app=FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
timestr = time.strftime("%Y%m%d-%H%M%S")


UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


@app.get('/') #path operation function
def index():
    return "hello world"

@app.get('/abbib')  #type /about to display below function
def anyname():
    return {'name':'subram'}

@app.get('/blog/{id}') #type /blog/100
def show(id):
    return {'myid':{id}}

@app.get('/digg /{id}/comments') #type /blog/100/can type anything not involve in code
def a(id :int): #u have to type integer only otherwise get type error
    return {'myid':id}

@app.get('/blog')#reading item value from input
def aa(item,item2:bool): #/blog?item=4343&item2=True
    if item2:
        return {'data':item}
    else:
        return {'data'}
    

class Blog(BaseModel):
    name: str
    id : int
    val : Optional[bool]

class stu(BaseModel):
    name :str
    age : int
    clas : int

class upd(BaseModel):
    name: str

@app.post('/msgg')        
def create_blog(request : Blog): #ucan use any word in place of request like obj creation 
    aa=request.name  # need to blog class name id val in box 
    # bb=request.id
    # db.update(aa,bb)
    return "{} its my name".format(aa)

students={1:{"name":"subbu","age":45,"class":"33"},2:{'name':'sundar','age':43,'class':"34"}}

@app.get("/")
def index():
    return {"name":"first data"}
@app.get("/get-student/{student_id}")
def get_student(student_id:int):
    return students[student_id]

@app.post('/createstudent/{student_id}')
def cr_stud(student_id : int,stud : stu):
    if student_id in students:
        return {'already exists'}
    students[student_id]=stud
    return students[student_id]

@app.put('/studentnmeupd/{stdid}')
def up_stu(stdid : int,update :upd):
    if stdid not in students:
        return {'not available'}
    students[stdid]['name']=update.name
    return students[stdid]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id:int):
    if student_id not in students:
        return {"Error": "students does not exist"}
    del students[student_id]
    return {"message": "student deleted successfully"}
@app.get('/allstudents')
def all():
    return students


@app.post("/upload-files")
async def create_upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        destination_file_path = "C:/Users/stanneeru/Desktop/Blog/Uploads/yu/"+file.filename #output file path
        async with aiofiles.open(destination_file_path, 'wb') as out_file:
            while content := await file.read(1024):  # async read file chunk
                await out_file.write(content)  # async write file chunk
    return {"Result": "OK", "filenames": [file.filename for file in files]}

#@app.post("downloadfile")
#def down(files: List[]=Dir(...)):
 #   for file in files:
  #      path="C:/Users/stanneeru/Desktop"
       # async with aiofiles.open(path,'wb') as out:













# from typing import List
# from fastapi import FastAPI, Query

# app = FastAPI()
# PATH="C:/Users/stanneeru/Desktop/Blog"

# # @app.get("/shows/")
# # def get_items(q: List[str] = Query(None)):
# #         results = {}
    
# #         query_items = {"q": q}
# #         entry = PATH + "/".join(query_items["q"]) + "/"

# #         dirs = os.listdir(entry)
# #         results["folders"] = [val for val in dirs if os.path.isdir(entry+val)]
# #         results["files"] = [val for val in dirs if os.path.isfile(entry+val)]
# #         results["path_vars"] = query_items["q"]
    
# #         return results






# PATH="C:/"

# @app.get("/download-files")
# async def get_items(q: str = Query(None)):
#         '''
#         Pass path to function.
#         Returns folders and files.
#         '''
    
#         results = {}
    
#         #query_items = {"q": q}
#         entry = PATH +q # +"/"

#         dirs = os.listdir(entry)
#         #results["folders"] = [val for val in dirs if os.path.isdir(entry+val)]
#         results["files"] = [val for val in dirs if os.path.isfile(entry+val)]
#         #results["path_vars"] = query_items["q"]
#         # for file in dirs:
#         #     destination_file_path = "C:/Users/stanneeru/Desktop/Blog/downloads/"+file
#         #     async with aiofiles.open(destination_file_path, 'w+') as out_file:
#         #         while content := file:  # async read file chunk
#         #             await out_file.write(content)  # async write file chunk
#         return dirs

class filep(BaseModel):
    uploadpath : str
    downloadpath : str



@app.post("/down/")
def get(obj:filep):
    try:
        shutil.copytree(obj.uploadpath,obj.downloadpath)
    except FileExistsError:
        shutil.copytree(obj.uploadpath,obj.downloadpath,dirs_exist_ok=True)
    return {"successfully transfered"}
        


if __name__=="__main__":
    uvicorn.run(app,host="127.0.0.1",port="8055")



