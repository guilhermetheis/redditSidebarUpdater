# redditSidebarUpdater

This is an updater for the [r/bostonceltics](reddit.com/r/bostonceltics). It uses a combination of [pandas](https://pandas.pydata.org/) and [praw](https://praw.readthedocs.io/en/stable/) to get firstly markdown formatted tables from [ESPN](https://www.espn.com/nba/team/_/name/bos/boston-celtics) and then finally to paste those files into reddit. Then [github actions](https://github.com/features/actions) to deploy the code every day, scheduled at given time you can find it on [.github/worklows](https://github.com/guilhermetheis/redditSidebarUpdater/tree/main/.github/workflows).

# Installation and usage

To install and use the code first please install the dependencies through `src/requirements.txt`. You might need to add `pywin32` manually if running locally on a windows machine. Please be aware that this is configured to be ran by github actions and thus it uses `load_dotenv()` and [github secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets). If running locally you might want to set the `reddit` instance of praw in `praw.ini` as following the [documentation](https://praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html). The script also has four different LUTs, please be aware that if running something similar for a western conference team you'd need to change the `LUT_Standings_newRed` and `LUT_Standings_oldRed`.

## Further changes based on different subreddits

We use the `styles` variable to set the different color schemes for the widgets. Please note that the color codes can be easily found when you set manually the widgets on the subreddit. Further, we use a file called `restOfSidebar.md` found in `outputs/` that is the rest of the markdown required for the old reddit setup, please add yours accordingly. Finally, be aware to run locally praw and indentify if your widgets are properly assigned, in our case we have a fixed rules widget which occupies the position `widgets.sidebar[0]` so we have schedule, roster and standings to be placed at the positions [1], [2], [3] respectively. 

## Constant updates

In order to keep your repo actions running you need to constantly update the repo. Maximum 3 months without updates are allowed.

# License

This project is under the GNU General Public License v3.0. 