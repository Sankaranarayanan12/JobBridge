# JobBridge 

It is an AI agent created for deaf and mute professionals. It helps them to find relevant jobs and draft suitable emails making this process easier for them.

### Tools, thought process and workflow:
The main tools and technologies used in this project include:
1) Google ADK (Agent Development Kit)- Used to create AI agents , provides various functionalities like scaffolding, testing , evaluvation making the process of creating AI agents easier.
2) FastAPI - For backend wraps the agent code in it and to connect with frontend to create a web application.
3) React js- For frontend , used to create beautiful UIs and coordinates with backend to show interactive completion steps.
4) Docker- For deploying the backend
5) Adzuna API - For finding realtime jobs

So first I focused on creating the AI agent, following a single agent architecture which contains the root agent which uses gemini-3.5-flash and accompanied with 3 tools namely:
1) search_jobs- Searches for realtime jobs using Adzuna API 
2) assess_communication_requirements- Filters out jobs fetched in step 1) using a predefined set of keywords
3) save_as_pdf - Used to save the results as pdf for user reference.

Now once the agent setup is complete , next I focused on creating the backend using fastAPI:
It has the following features:
1) Defines the allowed origins to access the backend.
2) Contains the SSE ( Server Sent Events)- One way HTTP method sent from backend to frontend used for live updates from backend accordingly used in frontend for live completion of steps.
3) Contains the agent pipeline- Imports the agent we created before and then creates a runner and a session to execute the pipeline and for each step in the pipeline gives out a message to the frontend.
4) Contains 2 endpoints - 1) /api/stream - the main endpoint where backend communicates the pipeline results to frontend 2) /api/health- general endpoint for health check purposes used to verify if the server is running.

Now Dockerfile is created to build the image and run the container on port 8080.

Coming to the frontend which has the following:
Screens:
1) ProfileScreen - The first screen where the user is asked to enter his details in the form which are later used for cutomization of email draft.
2) SearchScreen- The main results screen which shows the completion of steps in the agent pipeline , it does this by using the details filled from ProfileScreen to create a custom prompt to be sent to the backend and then creating eventListeners for each event sent from backend like "agent_start","agent_complete" etc which are used to show the dynamic completion of steps.
   
Component:
1) StepNode- Used for creating the UI for the agent pipeline steps and activates the node according to the status received from backend.
2) Tag- Used for creating UI for showing the tools used in the pipeline.

Finally all these are rendered using the default function App.

So now the full project is complete and for testing purposes I used 1) The web application method 2) adk web method which creates a playground used to test the logic with the help of prompt and also shows the agent workflow 3) adk run - used to test the agent via CLI.


