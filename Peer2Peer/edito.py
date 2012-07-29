import socket
import threading,thread
import time
class peer(threading.Thread) :
    serverSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    peer_address=""
    mySocket = None
    peerSocket = None
    
    isServer=False
    isClient=False
    port=9019
    
    def __init__(self) :
        self.serverSock.bind(("",self.port))
        threading.Thread.__init__(self)
        
    def get_text(self) :
        while True :
            self.mySocket.send("po")
            print "sent"
            
    def set_text(self) :
        while True :
            str1=self.mySocket.recv(100)
            print str1
            
    def tryServer(self) :
        try :
            print "entered server"
            self.serverSock.listen(4)
            self.peerSocket,self.peer_address=self.serverSock.accept()
            print "entered server 2"
            #if self.isClient :
             #   self.serverSock.close()
              #  return
            self.peer_address=self.peer_address[0]
            self.isServer=True
            self.mySocket=self.peerSocket
            print "server connected"
        except Exception,e :
            print "EC1: ",
            print e

    def tryClient(self) :
        while True :
            try :
                if not(self.isServer or self.isClient) :
                    self.clientSock.connect(("10.105.14.22",self.port))
                    self.peer_address="10.105.14.22"
                    print self.clientSock.getpeername()
                    self.isClient=True
                    self.mySocket=self.clientSock
                    print "client connected"
                    #threading.Timer(1,self.get_text).start()
                else :
                    return
            except Exception,e :
                print e
    
    def find_peer(self) :
        print self.isClient
        print self.isServer
        try :
            t1=threading.Thread(target=self.tryServer)
            t1.start()
            #t2=threading.Thread(target=self.tryClient)
            #t2.start()
            t1.join()
            #t2.join()
            
            t3=threading.Thread(target=self.get_text)
            t3.start()
            #t4=threading.Thread(target=self.set_text)
            #t4.start()
        except Exception,e :
            print "EC3: ",
            print e

class run_in_bg(threading.Thread) :
    def __init__(self) :
        threading.Thread.__init__(self)
    def run(self) :
        p=peer()
        p.find_peer()

p=run_in_bg()
p.start()

#text = document.get_text(document.get_bounds()[0],document.get_bounds()[1], False)
#		print text
		#document.se
