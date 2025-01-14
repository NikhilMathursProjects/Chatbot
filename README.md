# Chatbot using RASA
 Download the repository and navigate to its terminal.
Then install rasa using:
 pip3 install rasa
 
Now that we have all the packages installed ,we can go ahead an run the command { rasa train } in the terminal.
This will train the model off the particular intents, rules, stories and actions that have been made and will allow the model to detect the intents with an accuracy of 90%. Once the intent is identifies, it then checks which rule can be applied to it and performs some action based on that rule.

The actions file is used to store our python code to apply some data collecction/ manipulation that we wish to do on a users query. Here, i have used a simple dictionary that contains the location data and how many charging stations are in that location and i have used a EV model data that contaions the EV model and the information on its battery life, performance, range and price.
These action functions can get {entities} that a model picks up on from the intents and uses it to figure out what model/location the user is speaking about and performs some action on it so that the model can give a proper reply.
