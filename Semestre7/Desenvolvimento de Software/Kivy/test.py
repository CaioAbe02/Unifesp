from firebase import firebase

firebase = firebase.FirebaseApplication('https://desenvolvimento-de-softw-5bbfe-default-rtdb.firebaseio.com/', None)
result = firebase.get('/', None)
print(result)