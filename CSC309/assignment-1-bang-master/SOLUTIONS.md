## Group Members
### Please follow the format-> Student 1: Name of student (Student ID)
- Student 1: Enhao Wu (1003002289)
- Student 2: Hao Wang (1002275496)
- Student 3: Yian Wu (1002077236)
- Student 4: Quan Zhou (1002162492)

## Project Description:
This project is aimed to make an API that can give a clothing suggestion by given location and gendar of the user, the result should display on a webpage, in the form of picture or word.
We will use the infomation get from the API used in assignment1 to show the weather of a particular input city.

Strech goal: Let users be able to leave a comment on our suggestion, which may become a source for us to improve our suggestion. (as this is only the strech goal, it may not be able to finished before final demo)

## API Restfullness analysis:
A RESRful API should have following properities:
1) Easy to communicate
2) Architectural style 
3) REST technology
4) Sensible resource name

Our Choosing API also having those properities:
1) Easy to communicate
The API we choose providing an useful documentation on its website which helps us (develpoers) finding and accessing its data easily.

2) Architectural style 
From the aspect of data accessing, this API has well-orgainzed endpoint name (structure) that allows us get the specific information we want. For example, use (/api/location/(woeid)/) to get current weather of provided woeid - where on earth ID. Besides, its searching methods use a unique query parameter for each field, such as, using (/api/location/search/?query=(query)) to get the woeid of a city. 

From the data quality point of view, those data returns by this API is all in JSON format and relates to the information that mentiones in its endpoint name.

3) REST technology
Although, this API header it restricts us using methods other than GET, HEAD, OPTIONS, It still show the REST technology.
We can use these method to manipulate resources.

4) Sensible resource name
In this API, Resouces are in hierarchy via their URI names.

Therefore, this API is a qualified RESTful API.

## About how to use main.js
1) Run node main.js, you will get the whole list, one item and a random attribute of this item;
2) If you don't like the ''long'' result, you can follow the doc instruction, uncomment some code in our main.js (line 176 onwards) 




