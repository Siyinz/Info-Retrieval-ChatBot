# Info-Retrieval-ChatBot
Information Retrieval (IR) has many applications outside of search engines. This project develops a chatbot using IR techniques. While chatbots, also known as conversational agents, seem like a far stretch from IR, they have a natural synergy if you start from a collection of conversations. 
This project consists of two parts. In Part 1, I created a ground truth dataset of conversations ranked for relevance. In Part 2, I used this dataset to build and evaluate the chatbot. 

This project could help IR learner in many ways: 1) learn how to apply IR to a non-traditional IR task; 2) Develop skills in working with messy text data; 3) Learn how to annotate relevance data, when working with a large dataset; 4) Become more familiar with different ranking and retrieval methods for specific IR applications;
5) Develop skills at annotating and manually ranking for IR; 6) Improve software development skills; 7) Practice working with larger datasets.

### Conversation Data 
The dataset includes a large corpus of 2,326,394 conversation pairs from Reddit. Here, each message has one or more replies to it,r_i, . . . , r_k. Both messages and replies have unique identifiers (message_id and response_id). I use the message data in this dataset to match with the user queries and to reply to the user with one of the responses.

### Part 1: Ground Truth Annotation 
Reply relevance is scored on the following scale:
- 2– A great response to this message that is salient, self-contained, and clear for use in achatbot conversation
- 1– A good response to this message that is on-topic, but potentially not self-contained foruse in a chatbot conversation. Users will likely continue the conversation after such a reply
- 0– A mediocre response that may or may not be on topic, or may be vacuous (e.g,.  “ok”). A user may be confused from this response when used in a chatbot conversation or may beless likely to continue the conversation.
- -1– An off-topic response to a message in a chatbot conversation, which would likely leadthe user to be confused
- -2– A toxic, bad, or otherwise off-topic response to a message in a chatbot conversation

### Part 2: Build the ChatBot
In this part, I applied inverted index to all of the messages and used BM25 to retrieve the most relevant message (according to BM25); then I used BM25 to retrieve most relevant response to this message in the dataset.
The interface is created by Flask.

![chatbot image](https://github.com/Siyinz/Info-Retrieval-ChatBot/blob/main/chatbot.png)

This is a class project for SI 650.
