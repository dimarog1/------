import base64


with open('test.txt', 'r') as doc:
    val = doc.read()

print(base64.b64encode(b'123'))
