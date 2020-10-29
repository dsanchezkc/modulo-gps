# Download the twilio-python library from http://twilio.com/docs/libraries
# from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "AC73d35e68b6b938c2a53290e610682d33"
auth_token = "1db8318032ece98e0f64610af655a837"
client = Client(account_sid, auth_token)

message = client.messages.create(to="+56964590925", from_="+56988949343", body="Hello there!")
