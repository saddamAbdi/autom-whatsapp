from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime
cluster = MongoClient("mongodb+srv://sa:123@cluster0.x1m6y.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster["bakery"]
users = db["users"]
orders = db["orders"]
#orders = db["orders"]



app = Flask(__name__)

@app.route("/", methods=["get" , "post"])

def reply():

    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")[:-2]
    #number = number.replace("Whatsapp:", "")


    response = MessagingResponse()
    user = users.find_one({"number": number})
    if bool(user) == False:
        response.message("hi, thanks for contacting *Garaadso Technology*.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ Our *services*  \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*")
        users.insert_one({"number": number, "status": "main", "messages": []})
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            response.message("Please enter a valid response")
            return str(response)
        if option == 1:
            response.message(
                "You can contact us through phone or e-mail.\n\n*Phone*: +25261 5384768\n*E-mail* : info.garaadso@gmail.com")
        elif option == 2:
            response.message("You have entered *Our services*.")
            users.update_one(
                {"number": number}, {"$set": {"status": "services"}})
            response.message(
                "You can select one of the following services: \n\n1️⃣Training   \n2️⃣ Softwares \n3️⃣ Consaltance "
                "\n0️⃣ Go Back")

        elif option == 3:
            response.message("We work from *9 a.m. to 5 p.m*.")
        elif option == 4:
             response.message(
                 "We have multiple offices across the city. Our main center is at *Tree Piano, Maka Al Mukarama Road, Muqdisho*")

        else:
            response.message("Please enter a valid response")
    elif user["status"] == "services":
        try:
            option = int(text)
        except:
            response.message("Please enter a valid response")
            return str(response)
        if option == 0:
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            response.message("You can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ Our *services*  \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*")
        elif 1 <= option <= 4:

            serv = ["Training", "Softwares", "Consaltance"]
            selected = serv[option - 1]
            users.update_one(
                {"number": number}, {"$set": {"status": "address"}})
            users.update_one(
                 {"number": number}, {"$set": {"item": selected}})
            response.message("Excellent choice 😉")
            response.message("Please enter your address to confirm the order")
        else:
            response.message("Please enter a valid response")
    elif user["status"] == "address":
        selected = user["item"]
        response.message("Thanks for shopping with us 😊")
        response.message(f"Your order for *{selected}* has been received and will be delivered within an hour")
        orders.insert_one({"number": number, "item": selected, "address": text, "order_time": datetime.now()})
        users.update_one(
            {"number": number}, {"$set": {"status": "ordered"}})

    elif user["status"] == "ordered":
        response.message(
            "Hi, thanks for contacting again*.\nYou can choose from one of the options below: "
            "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ Our *services*  \n 3️⃣ To know our *working hours* \n 4️⃣ "
            "To get our *address*")
        users.update_one(
            {"number": number}, {"$set": {"status": "main"}})

    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    # return str(res)



    # users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})


    return str(response)

if __name__ == "__main__":
    app.run(port=6000)






#if __name__ == "__main__":
   # app.run()



