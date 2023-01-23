# Inspector_Bot

***Inspector bot*** - _Telegram_-bot, which is designed to optimize
and automate inspection control at production as much as possible.

### What the bot is capable of:
1. The bot parses the data recorded in a Google spreadsheet and processes them.
Google spreadsheet serves as a database, it is very convenient and easy for
ordinary users who want to update data in the bot.
2. Writes the data to a ***Json*** file and then works with it to avoid having to deal with each request
to parsing sheets.
2. The bot works with data and step by step based on the selected one
of the precinct, the user goes through the inspection checklist
and calculates the points scored by the station and recorded deviations.
3. At the end, the bot issues a ready message about the results of the inspector's control
and recorded deviations and forwards these messages to the working chat dedicated for this.
4. After forwarding the message, the bot records the results of the inspection in a Google table
from where you can conveniently collect statistics and process data.

#### Step-by-step work with the bot:
- We send the command ***/start*** in response to which the bot checks whether
the user has access to the bot.
![Access_id](./Media/Знімок%20екрана%202023-01-21%20о%2023.04.26.png)
In all subsequent steps, each subsequent message replaces the previous one.
- Location selection;
- Floor selection:
   - (the number of floors depends on the selected site)
- Selection of the district:
   - (depends on the selected floor)
- Choice of workplace
![Location](./Media/Знімок%20екрана%202023-01-21%20о%2023.07.35.png)
- Then there is a selection of a line of devices - a device - a project from which the device is composed

![Device](./Media/Знімок%20екрана%202023-01-20%20о%2023.21.14.png)
- Selection of the responsible manager for detected deviations at his station.
![Sp](./Media/Знімок%20екрана%202023-01-21%20о%2023.19.21.png)
- The next step is to go through the previously planned precinct inspection checklist
on compliance with the set processes. Chapters and questions in each chapter can
be a random number.
![Checklist](./Media/Знімок%20екрана%202023-01-21%20о%2023.22.06.png)
- After going through the checklist and fixing deviations (deviations include
unique photo/video description up to 10 pcs. and the precinct deviation generator) the bot issues ready-made messages
which can be automatically redirected to the work chat.
![Chat](./Media/Знімок%20екрана%202023-01-21%20о%2023.24.28.png)
- After forwarding the messages, the inspection results are automatically recorded in the table
where all the data selected in the previous steps and the points scored with the time spent on the inspection are indicated.
![Print](./Media/Знімок%20екрана%202023-01-21%20о%2023.26.02.png)
![Print](./Media/Знімок%20екрана%202023-01-21%20о%2023.28.52.png)
### An example of the work of the bot for replacing the location:
Change team leaders, installers and the list of devices.
![gif](./Media/_____-________-_-____.gif)