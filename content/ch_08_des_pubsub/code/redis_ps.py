import redis
import threading
import time

class Listener(threading.Thread):
    def __init__(self, name, channels):
        threading.Thread.__init__(self, name=name)
        self.pubsub = redis.Redis().pubsub()
        self.pubsub.psubscribe(channels)
    
    def run(self):
        for item in self.pubsub.listen():
            if item['type'] == "psubscribe":
                print(self.name, ": someone subscribed on channel {}",
                      item['channel'])
                continue 
                
            if item['data'] == b"KILL":
                self.pubsub.unsubscribe()
                print (self.name, ": unsubscribed and finished")
                break
            else:
                print("{} : channel {}, received: {}".format(
                    self.name, item['channel'], item['data']))

if __name__ == "__main__":
    r = redis.Redis()
    clients = [Listener('A', ['test.1', 'control']),
               Listener('B', ['test.2', 'control']),
               Listener('C', ['test.*', '*.', 'control'])]
    [client.start() for client in clients]

    time.sleep(1)
    r.publish('test.1', 'for 1')
    time.sleep(1)
    r.publish('test.2', 'for 2 ')
    r.publish('test.', 'for neither')

    r.publish('control', 'KILL')
