# Line-Tracking
Get the lines, put them in the database.

# Python Files
GameLines: Has the classes and functions necessary for handling all your lines. Includes FullGameLine class for handling full games and their totals, spreads and moneylines. Also has some static functions for cleaning up team names

NcaabSqlHandler: Handles all interactions with database for NCAAB. Has functions for adding and selecting lines, as well as updating them to old. When you instatiate the class, a connection with the db is opened.

NcaabLineGetter: File that actually runs everything. Keeps track of how many consecutive exceptions there have been for each site. Could benefit from multithreading, but for now it's serial. 

Bookmaker: Gets lines from lines.bookmaker.eu. Parses XML. will get other sports lines if you replace the ID. Already switched from MLB to NCAAB just fine.

Bovada: Gets lines from bovada.lv. Using the same API that populates the page when you're on the site, rather than the documented (and delayed) API. To switch sports, you probably need the most work to switch to a different API, but it's probably the same format.

Dimes: Gets lines from 5Dimes.eu. First, does a get of the main live lines page, and then gets the href for every sport. Then posts to the .aspx for getting the HTML to populate the lines on the page. Then we use BeautifulSoup to parse out the numbers. It's kinda gross, but it's tight enough now that there aren't any serious issues. Lots of inline comments (for good reason)

ArchiveNcaabLines: Copies lines that are older than 1 week into the Archive table. Does not delete the lines
