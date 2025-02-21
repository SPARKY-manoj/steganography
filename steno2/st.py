import json
import cv2
import os
import string
from flask import Flask,request,render_template,url_for,session
import secrets

c={}
app=Flask(__name__)
app.secret_key = secrets.token_hex(16) 
@app.route('/')
def index():
	return render_template('steno.html')

@app.route('/encrypt',methods=['POST'])
def encrypt():

	#img = cv2.imread("/home/manoj/Desktop/steno2/static/images.jpeg") # Replace with the correct image path

	msg = request.form['msg']
	password = request.form['pas']
	image_path=request.form['ipath']
	img=cv2.imread(image_path)
	d = {}
	global c
	print("before",c)
	for i in range(255):
	    d[chr(i)] = i
	    c[i] = chr(i)

	#session['c']=c
	with open("mapping.json","w") as f:
		json.dump(c,f)
	m = 0
	n = 0
	z = 0
	

	for i in range(len(msg)):
	    img[n, m, z] = d[msg[i]]
	    n = n + 1
	    m = m + 1
	    z = (z + 1) % 3

	cv2.imwrite("static/encryptedImage.jpg", img)
	os.system("start encryptedImage.jpg")  # Use 'start' to open the image on Windows
	#c_json=json.dumps(c)

	return render_template("result.html",image=url_for('static',filename='encryptedImage.jpg'),msg=msg,psw=password)


@app.route('/decrypt', methods=['POST'])
def decrypt():
	ms=request.form['stored_msg']
	ep=request.form['password']
	pp=request.form['stored_password']
	message=""
	#c_json=request.form['c_json']
	#cc=json.loads(c_json)
	n=0
	m=0
	z=0
	global c
	with open("mapping.json","r") as f:
		c=json.load(f)
	print("@@@@",c)
	#ccc=session.get('c',None)
	if c is None:
		return "no data found"
	img=cv2.imread("static/encryptedImage.jpg")
	if ep==pp:
		for i in range(len(ms)):
			message =  message + c[img[n,m,z]]
			n=n+1
			m=m+1
			z=(z+1)%3
	else:
		print("not authorized")
	
	return render_template("message.html",message=ms)
		

if __name__ == "__main__":
	app.run(debug=True)
