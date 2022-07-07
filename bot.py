import os
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()
app = Flask(__name__)

todos="""
    1. Find the school where Marius studied.
    2. Find the highschool where Marius studied.
    3. Buy a meter of beers/shots in one turn or throughout the day.
    4. Get the favourite colour of a retail worker.
    5. Get the name of somebody living outside Bucharest.
    6. Offer a beer to a stranger.
    7. Travel using public transport, without the ticket.
    8. Make a selfie with a policeman.
    9. Call ENEL to ask for a price for a new house in Bragadiru. Talk VERY slowly.
    10. Have a meal in a park.
    11. Go in a taxi and get out form the opposite door. 
    12. Collect 20RON/cigs by asking people on the street.
    13. Mark on the map each place you have visited.

    After you are done reading the ToDos, reply with 'Step 1' to get started.
"""

responses={
    "intromessage": """
        Hello my dear! 
        Get ready for a new experience of Bucharest! 
        This is going to be a treasure hunt. The aim is to get to the final destination while discovering Bucharest through the eyes of Marius. 
        In this game, Marius will be your partner. Think of him like an NPC, nothing more. Everything he is going to say is scripted. He is not allowed to help you or give you answers. 
        All the communication will be done with me, through your phone. The only time Marius is allowed to help you is if this system breaks down.
        
        To start, reply to this message with 'Start'. 
        """,
    "start": """
        Let's get started. Before everything, you need some items to help you on your way.
        Ask Marius for a map, pen and papers. You will need all of them. Once you have received the supporting tools, reply with 'To Dos' to get the list of TODOs. 

        Ah, do not forget to get some supplies for the road. Is going to be a long one.
        """,
    "todos": todos,
    "step1": """
        Go to the tram station and take the tram some stations. The number of stations is the answer to the following puzzle (We will start easy):

        Five pings and five pongs are worth the same as two pongs and eleven pings.
        How many pings is a pong worth?


        Reply with 'Step1' followed by the answer to the puzzle. 
        Do not forget to take note of this address. Might come in handy.
        """,
    "step12": "That's Correct. Take the tram 2 stations. Which one? Good luck. Once you get off, reply with the name of the station. HINT: It is the name of a romanian writer. ",
    "petreispirescu": """
        That's right. Now, follow those instructions
        From the tram station, go South East, take 3rd left and X right.

        The value of X is the answer to the following puzzle:

        How MANY statements are true?
        1. None of the statements is true.
        2. Exactly one of these statements is true.
        3. Exactly two of these statements are true.
        4. All of these statements are true.

        Reply with 'Street' followed by the numerical result.
        """,
    "street1": """
        Correct. The directions are:  From the tram station, go South East, take 3rd left and 1st right.

        Once you get there, head for the first BLUE appartments block and reply with it's number.
        """,
    "61a": """
        Now, here is the place where I have lived most of my life until leaving to Uni.
        Your next mission is to call one of my parents and ask them the directions to my primary school.
        Here the map might come in handy. 

        mom: *
        dad: *

        Once you get there, reply with the number of the school, to get further instructions. 
        """,
    "280": """
        Good.
        Now, go back to the tram station. Take the same tram you took before. How many stations? Well? Guess?

        Answer comes after you solve this puzzle:

        Today, the combined age of three oak trees is exactly 900 years.
        When the youngest tree has reached the present age of the middle tree, the middle tree will be the present age of the oldest one and four times the present age of the youngest one.
        What is the present age of the olderst tree.

        Reply with 'Tree' followed by the age.
        """,   
    "tree480": """
            The number of stations is equal to the street number of the school just visited multiplied by the result of the following puzzle.

            Miss Spelling, the English teacher, asked five of her students how many of the five of them had done their homework the day before.
            Daniel said none, Ellen said only one, Cara said exaclty two, Zain said exaclty three and Marcus said exaclty four.
            Miss Spelling knew that the students who had not done their homework were not telling the truth but those who had done their homework were telling the truth.
            How many of these students had done their homework?

            Reply with 'students' followed by the number of students who did their homework, followed by the street integer number of the school.
        """,             
    "students14": """
            Correct, only one student did their homework. Take the tram 4 stations.

            You can stop at the second one for a story from Marius, ot you can just walk all of the stations.

            Once you get there, reply with the name of the station, JUST THE FIRST NAME OF THE ROMANIAN FIGURE.
        """,             
    "maria": """
            Sweet. 
            Now, some exploration. Using the map, find Carol Park. Once inside, go to the monument.
            Reply with what is inside that monument.
            HINT: Singular Noun
        """,             
    "grave": """
            Good. 
            When was this unveiled?

            Reply with the date in ISO format.
        """,             
    "17-05-1923": """
            That's correct.

            Now, using the map, find Highschool located at the NORTH entrance of the park next to this one.

            Once there, reply with the SURNAME of the Romanian figure whos name was used to name the highschool.
        """,             
    "sincai": """
            Count the number of glass windows from the main entrance. 
            Reply with 'windows' followed by the number.
        """,             
    "windows12": """
            Count the number of sport fields. 
            Reply with 'sport' followed by the number of fields.
        """,             
    "sport4": """
            This was a tricky one. There are 3 fields outside and one indoor. HAHA.

            Your next target is the Tineretului Park. Go find the skatepark.
            Once there, count the number of ramps. Reply with 'ramps' followd by the number.
        """,             
    "ramps6": """
            All good. Ask Marius if you are in time. If you moved well, take a break, walk through the park. Stop and have a coffee at one of the venues near the entrance, or the one on the lake.

            Once done, reply with "What's Next?"
        """,             
    "what'snext?": """
            Do you wanna experience the subway here? 

            Take whatever mean of transport you wish to reach the Historical Center of Bucharest.

            Ask on the street how to get there. This is more exploration for you.

            Once there, reply with the name of the first Shaorma place you see (In front of you once you ENTER). 
        """,             
    "dristor": """
            Nearby that 'restaurant' there is a pub named after the most known beer festival.

            That's your next location, where you can solve some drinking related TODOs.

            To continue, find out which city is know for hosting this festival. No special characters needed.
        """,             
    "munich": """
            To discover more about the Historic Center, count the number of churches nearby. 
            Reply with 'churches' followed by the number you found.
        """,             
    "churches4": """
            What beautiful building is next to the biggest museum in the Historical center?
        """,             
    "cecbank": """
            Now, find your way towards the largest park nearby.

            Take a walk through the park. Find the name of the bird displayed in one of the cages. HINT: The national animal of India.
            Reply with the name of the bird.
        """,             
    "peacock": """
            Good job!
            We are almost done! 
            Our last destination is marked on the map.
            Find the sign and head towards there.

            Once there, reply with 'finish' to get  the final puzzle representing the number of the house where you have to go to.
        """,             
    "finish": """
            Let's do some maths for the end.
            How many of the following numbers are greater than 10?

            3 * sqrt(11); 4 * sqrt(7); 5 * sqrt(5); 6 * sqrt(3); 7 * sqrt(2)

            Reply with 'numbers' followed by the number.
        """,             
    "numbers3": """
            WE ARE DONE!!! WOOOOOOW!!!!
            Hope you had an awesome time discovering Bucharest and sorry for the bugs that happened.
            Hope Marius did not have to run home to fix something.
        """,             
    
}

@app.route('/bot', methods=['GET', 'POST'])
def bot():
    body = request.values.get('Body', None)
    resp = MessagingResponse()

    body_transformed = body.lower().replace(" ", "")

    if body_transformed in responses:
        resp.message(responses[body_transformed])
    else:
        resp.message("Sorry, this is not a valid reply.")

    return str(resp)


def start_ngrok():
    from twilio.rest import Client
    from pyngrok import ngrok

    url = ngrok.connect(5000).public_url
    print(' * Tunnel URL:', url)
    client = Client()
    send_intro_message(client, responses["intromessage"])

    client.incoming_phone_numbers.list(
        phone_number=os.environ.get('TWILIO_PHONE_NUMBER'))[0].update(
            sms_url=url + '/bot')

def send_intro_message(client, intromessage):
    message = client.messages.create(
        to="", 
        from_="",
        body=intromessage)

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        start_ngrok()
    app.run(debug=True)

# TODO 
# 1. Implement a chatbot API which responds to messages which are not part of the responses.
# 2. Better way of managing TODOs (Done and Not Done)
# 3. Design a system which is aware of each puzzle, allowing for near miss recognition.