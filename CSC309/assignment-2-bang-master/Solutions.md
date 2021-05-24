## Group Members:
- Student 1: Enhao Wu (1003002289)
- Student 2: Hao Wang (1002275496)
- Student 3: Yian Wu (1002077236)
- Student 4: Quan Zhou (1002162492)

## Features:
- This is a weather web application where we provide our users current weather, forecast information and clothing suggestions of a specific weather condition.

- General: 
    Users can type the city name they want to know the weather about in the search bar. After clicked the search button on the right of the search bar, if the city name is correctly entered, it will bring users to the page of current day's weather, where one can get the detailed weather infomation such as sunrise and sunset time, current wind speed and direction, humidity and pressure besides temperatures. Keep scrolling down, users can see a 7-days-forecast. We provide the basic information on conditon and temperatures for each day. The special feature of our web application is that we also provide clothing suggestion for our users. We realized that there are people having a bit trouble deciding how much to wear by just looking at pure numbers. What we do in clothing suggestion is that it will give a general idea of how much layers should users wear base on that day's weather. This includes remainding users to bring umbralla if that day might rain, etc. We also devided this section into "For Men" and "For Women" (for now). This is intended for users can choose their own preferences.

- User experience: This is what we care the most!
  We mocked a lot of situations of how users are going to use our product when designing and implementing a new feature.
  Example: 
    At first, the search action can only be triggled by mouse click the search button. After several observations, we found that it will be better if we enable users to start search by hitting the enter key, more over, it will be exelent if we could predict what they want to search. 

    So, now we have multiple ways to triggle the search action: 
    	1. Old fashioned way: user type, and then click search button. Like most grandgrandma do.
    	2. Type full city name, press Enter. emmmm, grandma way.
    	3. We used auto-complete, any time you finish typing a letter, it will give you a list of cities predicted based on what you typed.
    	   You can click on or use up/down key to select the city you want.
    	   If you find the first element on the drop-down list is what you like, just hit Enter, then you have everything!  Lazy but nice, right?

- Design: flexible and extendable
  When designing our web page and code structure, we not only just foucused on what we want to show "now", but also think more about other possible changes this product may have in the future. Our goal is when changes happen, the places we need to changed in our source code is as less as possible.
  For examples: 1. Right now we are displaying forecast for 7days, if we want to change it to 5 days, what we need to do is just change 7 to 5 in our code, in 2 places.
                2. When showing the clothing suggestions, we could have multiple ways to display suggestions for men and women: flex, block, etc. The reason why we choose to our current strategy, that is, showing contents by selected gender tab, is we want to make it extendable. If one day we want to add some other group, like "kids", or we want to provide a set of new groups, like "worl", "school", "travel",etc. we only need to add some tabs.

- All these views can be navigated by clicking relative buttons on the top.

- We use media queries to define css rules so that the web page can be applied on different devices with sone characteristics, relative display and using
  percentage on size and demention properties to strengthen this point.

- Errors:
    If nothing typed but searche button clicked, an error message "Nothing to search" will pop up. 
	If users entered a city that there's no weather information provided by Yahoo, an error message "No weather information of this city" will show up on the screen.
	If you accidentally hit the Enter button half way on your typing, no error message, that's too rude, we will provide you the first element on the drop down predicted cities.
  If users clicked search, but network accidentally down, an error box with "abnormal network connection" will pop up.



