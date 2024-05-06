import cv2
from playsound import playsound
from twilio.rest import Client


rat_cascade = cv2.CascadeClassifier('haarcascade_car.xml')  # Replace with the actual path

cap = cv2.VideoCapture(0)

TWILIO_ACCOUNT_SID = 'YOUR_SID'
TWILIO_AUTH_TOKEN = 'YOUR_AUTH_TOKEN'
TWILIO_PHONE_NUMBER = '+YOUR_TWILO_PHONE_NUMBER'
TO_PHONE_NUMBER = 'YOUR_NUMBER '

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms_alert(message):
    try:
        twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=TO_PHONE_NUMBER
        )
        print("SMS Alert Sent!")
    except Exception as e:
        print(f"Error sending SMS: {e}")


while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rats = rat_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in rats:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        print("Rat Detected")
        send_sms_alert("Rat detected in your Enivironment")

    cv2.imshow('Rat Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()