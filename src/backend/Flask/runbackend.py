# runbackend.py
from backend import app
 
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8089,debug=True)
