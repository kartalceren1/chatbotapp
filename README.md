# AI Interview Helper

A web application that provides mock interviews using AI. Users can choose a persona (HR, Tech, Manager), answer questions, and receive feedback and guidance in a natural, conversational way. Powered by OpenAI's GPT-4o-mini model.


## Features

- **Multiple Personas**: HR, Tech, and Manager interview styles.  
- **Interactive Chat**: AI responds naturally to answers and provides feedback on request.  
- **Dynamic Questions**: Randomized questions from JSON files.  
- **Frontend**: Responsive chat interface with styled message bubbles.  
- **Rate Limiting**: Protects the backend from excessive requests.  


## Technologies Used

- **Backend**: Python, Flask, Flask-Limiter  
- **Frontend**: HTML, CSS, JavaScript  
- **AI Integration**: OpenAI GPT-4o-mini  


##Usage

Go to the homepage.

Select a persona: HR, Tech, or Manager.

Start the mock interview.

Type your answer in the chat.

When ready for formal feedback, type:

Ok, I want my feedback now


The AI will provide a score, feedback paragraph, and practical tip.
