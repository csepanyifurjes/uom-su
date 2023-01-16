# uom-su
University of Miskolc, Synergy Unit research within the field of Human Centered Artificial Intelligence

1. To set up the test DB file execute: persistence/setup_db.py
2. Start up the application execute: run.sh

The Automatic Assessment Tutor application will listen on local port: 3030
The Synergy Unit gateway will listen on local port: 3033

###### To test the evaluation:

* Example question: What do the initials HAL for the HAL 9000 computer mean in the film 2001: A Space Odyssey?
* Expected answer: Heuristically programmed Algorithmic computer
* Actual answer: Heuristically programmed Idontknow computer

###### Request URL:
http://localhost:3030/tutor/evaluate

###### Request body: 
```
{
    "id": 3,
    "answer": "Heuristically programmed Idontknow computer"
}
```
###### Response:
```
{
    "result": [
        "9e6f464c-20b3-4125-83c5-0ee7bd1e11a6",
        "good"
    ]
}
```
To see the explanation word cloud use the UUID from the response: 
http://localhost:3033/sugw/9e6f464c-20b3-4125-83c5-0ee7bd1e11a6/explain.png

######Please cite this paper: 
L. Csépányi-Fürjes, Controllable and explainable AI framework in the Automatic Assessment domain, 2023
