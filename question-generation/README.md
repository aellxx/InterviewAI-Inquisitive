# Question Generation

Our objective is to retrieve the document from the text editor and generate questions that will be returned to the text editor as comments in the side margin.

Currently, our system supports reading context from a text file, simulating document retrieval from a text editor. Subsequently, it generates questions using Interview AI. Both the context and generated questions are saved as a JSON dataset, which can then be utilized by the Word API.

How to run (recommended steps):

1. Launch code tunnel to ds1.
2. Git clone this repository.
4. Create a new conda environment for question-generation, then activate the new conda environment.
5. Run `pip install -r requirements.txt`.
6. Run `python main.py <port>`. Note that `<port>` must be some value 500X, where X is between 0~9. Please choose an available port and then [post your choice here](https://teams.microsoft.com/l/message/19:f39cc2b4462c4aa88de10d429d76c5cd@thread.tacv2/1685988735507?tenantId=756349b9-0610-4b01-917b-2a4ac10df947&groupId=1b002a41-ef6d-460c-986e-d32d230bef4f&parentMessageId=1685988735507&teamName=Arnold%20Lab&channelName=Summer23&createdTime=1685988735507&allowXTenantAccess=false).
7. Navigate to `https://dev<X>.kenarnold.org/generate`, where `<X>` is the last digit of your port 500X.