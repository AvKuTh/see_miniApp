from kafka import SimpleProducer, KafkaClient
import time,datetime
from random import randint

kafkaAdd = 'localhost:9092'
kafka = KafkaClient(kafkaAdd)
producer = SimpleProducer(kafka)
topic = 'my-stream'


def stream_emit():
    counter = 0
    maxC = 2
    while (counter < maxC):
        counter = counter +1
        data = [str(datetime.datetime.now()) , randint(0, 100)]
        producer.send_messages(topic, bytes(str(data), 'utf-8'))
        print (counter)
        time.sleep(1)
    print('done streaming')

if __name__ == '__main__':
    #print( datetime.datetime.now())
    stream_emit()
