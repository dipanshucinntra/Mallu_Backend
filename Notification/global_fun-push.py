from pyfcm import FCMNotification

def sendNotification(registration_id, Title, Message):
    try:
        push_service = FCMNotification(api_key="AAAAbatpOys:APA91bHANX5P9VlXkIP7Apzx8oi0khQSXjTXmwRdFsyg3HZEvHs3lh8iDYTdCWpHNhC-uXHnkivYRqZ4r8XnknRu12Xg7lF5H2QM9IW-A0RlJi9Z7JeAO2mKVElquBzrRXulGp0_ORO8") # vision
        registration_id=registration_id

        #registration_id = "c_EbPZTSRlOWdlmNz6Ntcu:APA91bGEL9tQHNlAY0TztlnKOLSsFELQUKJ6dyujRt3SP8HRTeQAnMo5kr-7VZLhD_nU3FMyA8nm03wlR8i56YB2CPNh1G7dWcc2qKMt8PY0sVjLg2-CVDaEubYohmHxBJFGps6J8zaZ"
        # message_title = "Test Notification"
        # message_body = "Hi Abhishek, your customized news for today is ready"
        message_title = Title
        message_body = Message
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, content_available=True)
        
        # To support rich notifications on iOS 10, set
        extra_kwargs = {
            'mutable_content': True
        }

        print(result)
        return "sent"
    except Exception as e:
        return str(e)



# push notification
registration_id = "c_EbPZTSRlOWdlmNz6Ntcu:APA91bGEL9tQHNlAY0TztlnKOLSsFELQUKJ6dyujRt3SP8HRTeQAnMo5kr-7VZLhD_nU3FMyA8nm03wlR8i56YB2CPNh1G7dWcc2qKMt8PY0sVjLg2-CVDaEubYohmHxBJFGps6J8zaZ"
title = "Vision Test by sk-"
body = "Hi Rahul, your customized news for today is ready"

sendNotification(registration_id=registration_id, Message=body, Title=title)
