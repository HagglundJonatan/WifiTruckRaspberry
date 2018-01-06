#!/usr/bin/python
import socket
import threading
import signal
import sys
import time
from wifi_truck_controller import WifiTruckController
from Queue import Queue

HOST = "192.168.43.100"
print(sys.argv)
if len(sys.argv) > 1:
	HOST = sys.argv[1]

print(HOST)

PORT = 2000
MSGLEN = 13

exit_prog = False

class WifiTruckServer:
	def __init__(self, myServerSocket=None, clientSocket=None, incomingMsgQueue=None, outgoingMsgQueue=None,
				 disconnect=False, wifiTruckController=None):
		if myServerSocket is None:
			self.myServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.myServerSocket = myServerSocket

		self.myServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.myServerSocket.bind((HOST, PORT))
		self.myServerSocket.listen(1)
		self.incomingMsgQueue = Queue()
		self.outgoingMsgQueue = Queue()
		self.disconnect = False
		self.wifiTruckController = WifiTruckController()

	def startServer(self):
		#print("Waiting on connection...")
		
		(clientSocket, address) = self.myServerSocket.accept()
		#print("Connection accepted!")
		self.clientSocket = clientSocket
		self.disconnect = False

	def listenToClient(self):
		while not self.disconnect:
			chunks = []
			bytes_recd = 0
			while bytes_recd < MSGLEN:
			#	print("Try to get " + str(MSGLEN - bytes_recd) + "number of bytes")
				try:
					chunk = self.clientSocket.recv(min(MSGLEN - bytes_recd, 2048))
				except Exception:
					self.disconnect = True
					break
				if chunk == '':
					self.disconnect = True
					break
				# raise RuntimeError("socket connection broken")
				chunks.append(chunk)
				bytes_recd += len(chunk)
			#	print("Received - " + chunk + "\nBytes received - " + str(bytes_recd))
			msgFromClient = ''.join(chunks).rstrip()
			self.incomingMsgQueue.put(msgFromClient)

	def writeToClient(self):
		while not self.disconnect:
			bytes_sent = 0
			msgToSend = self.outgoingMsgQueue.get(True)
			#print("Msg to send to client:" + msgToSend)
			while bytes_sent < MSGLEN:
				sent = self.clientSocket.send(msgToSend)
				if (sent == 0):
					self.disconnect = True
					break
				bytes_sent += sent
				#print("Bytes sent to client:" + str(bytes_sent))

	def handleIncomingMsgs(self):
		while not self.disconnect:
			currentMsg = self.incomingMsgQueue.get(True)
			try:
				firstPart, secondPart = currentMsg.split("#")
			except ValueError:
				currentMsg += "ValueError"
				continue
	
			if (firstPart == "CMD_JOYY"):
#				print("MOVE!")
				self.wifiTruckController.move(float(secondPart))
			#elif (firstPart == "CMD_DWN"):
			#	print("BACKWARD!")
			#	self.wifiTruckController.move(float(secondPart))
			elif (firstPart == "CMD_JOYX"):
#				print("STEER!")
				self.wifiTruckController.steer(float(secondPart))
			#elif (firstPart == "CMD_RGT"):
			#	print("TURN RIGHT!")
			#	self.wifiTruckController.steer(float(secondPart))
			#elif (firstPart == "CMD_RL1"):
			#	print("RELEASE SERVO 1")
			#	self.wifiTruckController.releaseSteering()
			#elif (firstPart == "CMD_RL2"):
                        #        print("RELEASE SERVO 2")
                        #        self.wifiTruckController.releaseMovement()
			elif (firstPart == "CMD_DSCNNCT"):
#				print("Disconnect!")
				self.disconnect = True
				self.wifiTruckController.stop()
#			else:
#				print("else - currentMsg:" + currentMsg)
			self.outgoingMsgQueue.put("Server got " + currentMsg)

	def stopServer(self):
#		print("Stopping server")
		self.myServerSocket.close
		# Reset this bool
		self.disconnect = False

	def signal_handler(self, signal, frame):
#		print("Exiting gracefullyerererer!")
		self.stopServer()
		exit_prog = True
		sys.exit(0)

# Main loop!
# Wait for wifi connection to be set up
#print("Sleep 10 s to let wifi connect correct")
time.sleep(10)

myServer = WifiTruckServer()

signal.signal(signal.SIGINT, myServer.signal_handler) # Receives Ctrl + c and closes the sockets nicely

while not exit_prog:
	myServer.startServer()
	clientListener = threading.Thread(target=myServer.listenToClient)
	clientListener.start()
	#clientWriter = threading.Thread(target=myServer.writeToClient)
	#clientWriter.start()
	myServer.handleIncomingMsgs()
	myServer.stopServer()

