# uom-su
University of Miskolc, Synergy Unit research within the field of Human Centered Artificial Intelligence

1. To set up the test DB file execute: persistence/setup_db.py
2. To start up the application execute: run.sh

The Automatic Assessment Tutor application will listen on local port: 3030
The Synergy Unit gateway will listen on local port: 3033

###### To test the AA application:

* Example question: What do the initials HAL for the HAL 9000 computer mean in the film 2001: A Space Odyssey?
* Expected answer: Heuristically programmed Algorithmic computer
* Actual answer: Heuristically programmed Idontknow computer

###### Request URL to get the question list:
http://localhost:3030/tutor/questions
###### Response excerpt:
```
[
        3,
        "What do the initials HAL for the HAL 9000 computer mean in \"A Space Odyssey\" film?"
]
```

###### Request URL to evaluate the user's answer:
http://localhost:3030/tutor/evaluate

###### Request body (the ID identifies the question): 
```
{
    "id": 3,
    "answer": "Heuristically programmed Idontknow computer"
}

{
    "id": 1,
    "answer": "Do you have a problem?"
}


```
###### Response:
```
{
    "result": [
        "9e6f464c-20b3-4125-83c5-0ee7bd1e11a6",
        "NOT OK"
    ]
}

{
    "result": [
        "599471d5-185b-43a6-87e1-f920ec93c856",
        "unacceptable, try again"
    ]
}
```

In most cases the answer doesn't have to be exact, like in this example case. In most cases the meaning of the answer 
needs to be matched and not the words themselves. The built-in language model makes it possible to process this kind 
of answer as well. Take a look for example question ID: 1, where we are expecting a polite greeting from the learner. 
The answer can be anything until its meaning matches to the expected sentence.  

###### ExplainSU:
To see the explanation word cloud use the UUID from the response: 

http://localhost:3033/sugw/9e6f464c-20b3-4125-83c5-0ee7bd1e11a6/explain.png

###### ReportSU:
To get statistical information from the system: 

http://localhost:3033/sugw/report

###### ControlSU:
If we feel the AA module's response is too harsh we can change the evaluation scheme to another one that is more 
human friendly. The available schemes: TEXTUAL, BINARY, SCHOOLISH. 

http://localhost:3033/sugw/control/TEXTUAL

###### TeachSU:
We can get a teaching word cloud that emphasizes the importance of the expected answer tokens.

http://localhost:3033/sugw/9e6f464c-20b3-4125-83c5-0ee7bd1e11a6/teach.png

###### Please cite this paper: 
L. Csépányi-Fürjes, Controllable and explainable AI framework in the Automatic Assessment domain, 2023

The related paper: https://www.researchgate.net/publication/373873415_Controllable_and_explainable_AI_framework_in_the_Automatic_Assessment_domain
