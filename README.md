# NBAPlayerMatchUp
 An experiment to  visualize and analyze player match-ups against specific NBA teams throughout their careers.

Completed Goals.

-Scrape all NBA gamelogs from now til 2010 from each active players with more than 10 minutes.

    -In order for the correct gamelogs to be searched without having to manually search and do more calculations, I will pull the players from my mongodb database with their respective url and have it as a list. (Completed, September 20,2019)

    -Go through each gamelog pages for each season up to 2010 if possible. ("Completed", Forgot to add the 2010 requirement so I scraped all the gamelogs instead, September 20,2019)

-Scrape all active NBA players who played at least 10 minutes career wise. (Completed,September 19,2019)

-Scrape all NBA teams currently active with their abbreviations. (Completed,September 19,2019)

- Verify the correct type of data is there (Completed, September 22,2019)

- Graph Lebron James points scored against all 30 teams on the x axis with dots or teams respective logos. (Moved to a Javascript implementation,22,2019)

Current Goals:
- Verify the data is correct with some PyTest
- Implement a NodeJS with Chart.js implementation for the data.
