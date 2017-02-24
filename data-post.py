	########################################################################
# 08/02/2015
# ng-demo_02-2016/data-post.py
# ID, Vcc, T, RH, A(x,y,z), P, Vpd, Status
# http://data.sparkfun.com/streams/RM89ZKdGNxsx0zR9XNDo
########################################################################

import RPi.GPIO as GPIO  # RPi.GPIO used for GPIO reading/writing
import time              # time used for delays
import httplib, urllib   # http and url libs used for HTTP POSTs
import socket            # socket used to get host name/IP

import re
import requests
import serial

#################
## Phant Stuff ##
#################
server = "data.sparkfun.com" # base URL of your feed

## 1
publicKey1 = "RM89ZKdGNxsx0zR9XNDo" # public key, everyone can see this	https://data.sparkfun.com/streams/RM89ZKdGNxsx0zR9XNDo
privateKey1 = # private key, only you should know
## 2
publicKey2 = "rozaoqELaGHwzMlD1NXm" # public key, everyone can see this	https://data.sparkfun.com/streams/rozaoqELaGHwzMlD1NXm
privateKey2 = # private key, only you should know

## 3
publicKey3 = "o8yg8yK4X7cNDDo4xKLE" # public key, everyone can see this	https://data.sparkfun.com/streams/o8yg8yK4X7cNDDo4xKLE
privateKey3 = # private key, only you should know


fields = ["id","v_cc","temperature", "humidity", "acceleration_x", "acceleration_y", "acceleration_z", "pressure", "v_pd", "status"] # Your feed's data fields


##########
## Serial ##
##########
ser = serial.Serial(

	port='/dev/ttyAMA0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
#	timeout=100
)

##########
## Loop ##
##########
print("Data monitor now running! Press CTRL+C to exit")
T = time.strftime("%A %B %d, %Y %H:%M:%S %Z")
print T
try:
    # Loop until CTRL+C is pressed
    while 1:
        print "\r\n"
        print "awaiting data..."
        print "\r\n\r\n"
        
	data_stream = ser.readline()
	T = time.strftime("%A %B %d, %Y %H:%M:%S %Z")
	
	print T
	print data_stream

	data = {} # Create empty set, then fill in with our three fields:
	# print "data = {}"
	
	inputdata = re.findall(r'[-+]?\d*\.\d+|\d+]',data_stream)
	# print "inputdata = re.findall(r'[-+]?\d*\.\d+|\d+]',data_stream)"

	inputdata_length = len(inputdata)
	print "length of input_data = "
	print inputdata_length
#	inputdata = re.findall(r'[-+]?\d\*|\d*\.\d+|\d+]',data_stream)
#	inputdata = re.findall(r'[-+]-?(\d+(\.\d*)?|\d*\.\d+)]',data_stream)

	# print "\r\n"
	# print("inputdata= ")
	# print inputdata

        if inputdata_length == 10:
            
            # don't post ID - for some reason the ID is not being picked up.  To investigate further
            data[fields[0]] = inputdata[0]	# ID
            data[fields[1]] = inputdata[1]	# v_bat
            data[fields[2]] = inputdata[2]	# temperature
            data[fields[3]] = inputdata[3]	# humidity
            data[fields[4]] = inputdata[4]	# acceleration_x
            data[fields[5]] = inputdata[5]	# acceleration_y
            data[fields[6]] = inputdata[6]	# acceleration_z
            data[fields[7]] = inputdata[7]	# pressure
            data[fields[8]] = inputdata[8]	# photodiode
            data[fields[9]] = inputdata[9]	# status
            # print "data[fields[0]] = inputdata[0]	# ID"

    #	print "\r\n"
    #	print inputdata

            # print "data= "
            # print data
            
            # print "\r\n"
            params = urllib.urlencode(data)
            # print "params = urllib.urlencode(data)"
            
            # Now we need to set up our headers:
            headers = {} # start with an empty set
            # These are static, should be there every time:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            headers["Connection"] = "close"
            headers["Content-Length"] = len(params) # length of data
			
			
            if inputdata[0] == "0.01":				
				headers["Phant-Private-Key"] = privateKey1 # private key header1
				# Now we initiate a connection, and post the data
				# Using a very short `connect_timeout` gives us a feel for what happens when the
				# server is slow to pickup the connection.
				# connect_timeout = 0.0001
				# try:
				# response = requests.get(url="https://httpbin.org/delay/5",
										# timeout=(connect_timeout, 10.0))
				# except requests.exceptions.ConnectTimeout as e:
				# print "Too slow Mojo!"
				
				
				# Now we initiate a connection, and post the data
				c = httplib.HTTPConnection(server, timeout=1)
				# print "c = httplib.HTTPConnection(server)"
				# Here's the magic, our reqeust format is POST, we want
				# to send the data to data.sparkfun.com/input/PUBLIC_KEY1.txt
				# and include both our data (params) and headers
				c.request("POST", "/input/" + publicKey1 + ".txt", params, headers)
            
            if inputdata[0] == "0.02":				
				headers["Phant-Private-Key"] = privateKey2 # private key header2
				# Now we initiate a connection, and post the data
				c = httplib.HTTPConnection(server)
				# Here's the magic, our reqeust format is POST, we want
				# to send the data to data.sparkfun.com/input/PUBLIC_KEY2.txt
				# and include both our data (params) and headers
				c.request("POST", "/input/" + publicKey2 + ".txt", params, headers)            
            
            if inputdata[0] == "0.03":				
				headers["Phant-Private-Key"] = privateKey3 # private key header2
				# Now we initiate a connection, and post the data
				c = httplib.HTTPConnection(server)
				# Here's the magic, our reqeust format is POST, we want
				# to send the data to data.sparkfun.com/input/PUBLIC_KEY2.txt
				# and include both our data (params) and headers
				c.request("POST", "/input/" + publicKey3 + ".txt", params, headers)     
				
            # print "c.request(...)"

            

            # reset_selective data
            # print "reset_selective data"
                    
    #	r = c.getresponse() # Get the server's response and print it
    #	print r.status, r.reason

            print "data posted"
        else:
            print "data size mismatch"

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO
