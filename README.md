# Two Hong Kong controversies and their impact on foreign companies' reputation on Reddit

Welcome to our seminar's repository ! 

## The project 
We chose to study the Hong Kong controversies and their impact on foreign countries' reputation. 
To do so, we scrapped the reddit social network in relation with two tech companies : 
* Apple : a mapping app map used by Hong Kong's protestors to map the repression was withdraw from the App Store (see https://www.theguardian.com/technology/2019/oct/10/tim-cook-apple-hong-kong-mapping-app-removal). 
* Blizzard : an award-winning taiwanese professional game player was fired from Blizzard's esport contest price after 
publicly supporting Hong Kong protestors (see : https://www.pcgamer.com/taiwanese-hearthstone-caster-fired-after-hong-kong-controversy-says-he-still-doesnt-know-why/)
The project's findings are detailed in the powerpoint presentation (Reports/Final_Presentation.pptx) and in the final report (Report/Seminar_Thesis.pdf). 

## The code 
This project led to scrapping both cases (see jupyter notebooks : Apple_case_analysis.ipynb for the Apple case and 
Blizzard_case_analysis.ipynb for the Blizzard case). 
### Run the code
You need to use the packages specified in the requirements.txt file. 
To scrap more data, go to Data/ and open the jupyter notebook that will create two new csv for you. 
To analyse these csvs, you can look into Apple_case_analysis.ipynb and Blizzard_case_analysis.ipynb. 

## The main interesting findings from our project : 
* The Apple's news are so numerous that the case did not have a lot of influence on Apple's reddit thread.
Nor the opinion, nor the number of removed posts are changing after the event. We then believe that its reputation
has not collapsed because of this choice to remove the app from the app store. 

* The Blizzard's thread, however, was much impacted by the case. The event can clearly be seen 
thanks to the number of removed posts and the number of posts that have no title. 
The people were using posts with a single image and no text to override automatic censorship. 

* The opinion analysis carried out permits to map the positivity or negativity of the posts. The influence of the events on the 
hate in the posts was rather hard to measure, it didn't move for Apple thread and increased with Blizzard. This seems odd, we believe it to be impacted by the moderation and the supporting messages. 

Enjoy ! 