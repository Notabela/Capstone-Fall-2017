Team Meeting: Monday, May 7 2018
------------------------------------
* Discussed the next steps needed to complete the project
    - Injecting the sample data in the web application to create a csv : Socratis Katehis
    - Use the csv created to train the system and create a Machine Learning model : Miguel Rodriguez
    - Create interface to display results and add improvements to web application: Daniel Obeng
    

Team Meeting: Monday, April 30 2018
-------------------------------------
* Discussed how the sample videos created can be injected into system
* Discussed possible issues that may come up with the sample video that could hinder predictability rate
* Discussed changes that need to be made to the data being collected
    - Convert Micro-expressions to two second intervals (Micro expression rate): Miguel Rodriguez
    - Convert Blinks to two second intervals (Blink rate): Daniel Obeng
    - Go through training video and create a csv with timestamps of where lie occured: Socratis Katehis
    

Team Meeting: Monday, April 16 2018
-------------------------------------
* Discussed possible issues that may come up with application and how to solve it
* Went through implementations to ensure data being collected can be used
* Discussed Machine Learning algorithm to be used and how the data can be fit into the model


Team Meeting: Monday April 9, 2018
-------------------------------------
* Discussed and created timeline of tasks that need to be completed

see below

#### STEP 1

Facial - 
Blink Pattern (Currently worked on by Daniel)
Microexpressions
Gaze Direction and Pupil Dilation.

     Possible: Combine Blink Pattern with Head Movement (Need to recall research)

Vocal - 
Features from the Vocal Paper (Currently worked on by Socratis). 

     Paper will provide all five features.

#### STEP 2

Data - 
Research and find interrogation videos with deception data available if possible.
IF NOT, go back to our own interviews and data collection.

Measurements -
Begin to analyze the data with the implemented features. Choose the features that are more accurate in detecting lies.

#### STEP 3

Machine Learning  - 
Choose a model that best suites our data and features.
Training a network with the selected features on data that was previously collected.
Make improvements on accuracy and models.

Final Design - 
Build a web app where a video can be uploaded for analysis. Graphical analytics and prediction will be spit back.
