# IPL-DataAnalysis


## Match Prediction

### Problem Statment
At the begining of the final over (19th Over) -- Can we predict the match result ?

In other words, Can we know which bowler will win us the match ?

### How do I do it?

#### Hypothesis
Can the team defend the score in the final over of the match ? -- This depends of multiple factors.
1. Runs to defend
2. Wickets in hand
3. The bowler
4. The batsman

The first two data points are easy to understand easy to capture. 

But how we actually represent the players skills and experience in data ? 

The bowlers skills can be represented as following data points:
- Runs (runs conceded)
- Overs / Balls bowled
- Economy (combination of the above 2)
- Wickets taken

We know from experience, that the over all statistics is not a true representation of what happens in the final overs of a match. 

We have seen several games where the tables turn in the last few overs.

So, we can further breakdown the statistics into following categories:
- End game statistics (last 5 overs)
- Life time statistics 
- Current form (last 5 match statistics)


Similarily, the batsman skills can also be represented as following data points:
- Runs scored
- Balls faced
- Strike rate (combination of the above)


#### DS Problem
This is an example of Classification Problem. We want to predict if the match will be Won or Lost.

I'm currently using Decision Tree classifier and Random Forest classifier. 

My approach is to try various techniques and see which combination gives the most accurate model.
