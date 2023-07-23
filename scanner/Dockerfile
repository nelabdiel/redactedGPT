From python:3.8

Maintainer Nelson A. Colon, GH: nelabdiel
# tell the port number the container it should expose
Expose 5003

# run the application
#command: gunicorn -w 4 -b 127.0.0.1:5002 chatgphit:app
#CMD ['"python", "chatgphitAPP.py"]
#CMD ["gunicorn", , "-w", "-4", "-b", "0.0.0.0:5002", "chatgphitAPP:APP"]

# make directories suited to your application
RUN mkdir -p /home/project/scanner
WORKDIR /home/project/scanner

#copy and install packages for flask
COPY requirements.txt /home/project/scanner
RUN pip install --no-cache-dir -r requirements.txt

# copy contents from your local to your docker container
COPY . /home/project/scanner