from threading import Thread

def heythere():
    print "penguin"

def sup():
    print "magical"

if __name__ == "__main__" :
    
    thread1 = Thread(target=heythere,args=())
    thread2 = Thread(target=sup,args=())

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()