<p align="center">
    <img alt="Messenger Insights" src="https://user-images.githubusercontent.com/35405685/72289479-3802a080-3619-11ea-91a2-e74b6f39aba5.png" width="250" />
</p>
<h1 align="center">
  Messenger Insights
</h1>

CLI tool and web app to calculate and display cool stats about your messenger history 👀

## CLI Tool

A Python program that can process and graph cool trends in your Messenger usage based on parameters you provide through the CLI.

Examples:

![messenger-cli](https://user-images.githubusercontent.com/35405685/71392995-5eb05700-25d8-11ea-8257-7d536fd77516.gif)
![image](https://user-images.githubusercontent.com/35405685/71393067-b6e75900-25d8-11ea-83cf-f869c1492f9b.png)

![active_times](https://user-images.githubusercontent.com/35405685/71400004-7e08ad80-25f3-11ea-972b-c8b0b396e223.gif)
![image](https://user-images.githubusercontent.com/35405685/71400035-8eb92380-25f3-11ea-9273-0a45d8c584bf.png)

### Usage

1. [Download your Facebook Messenger data](https://www.zapptales.com/en/download-facebook-messenger-chat-history-how-to/). Extract the files to a directory of your choice. After you're done, your directory should have the following structure:
```
D:/your/path/to/facebook-data
├── archived_threads
├── filtered_threads
├── inbox
├── message_requests
├── stickers_used
```

2. Clone the repo to a directory of your choice and install dependencies. Make sure you are using Python version **3.7.x**

```
git clone https://github.com/austichen/messenger-insights.git
cd messenger-insights
pip install -r requirements.txt
```

3. In the `utils/constants.py` file, change the `FB_DATA_DIRECTORY` variable to be the absolute path to the directory you specified in step 1. Using my example in step 1, I would update it to `FB_DATA_DIRECTORY='D:/your/path/to/facebook-data'`

4. In the root directory of `messenger-insights`, run
```
python setup.py
```
This script takes the raw JSON message data and converts them to a set of unpartitioned and partitioned (by year and chat type) CSV files. Your messenger data folder should be updated with two new folders, `raw` and `partitioned`:
```
D:/your/path/to/facebook-data
├── archived_threads
├── filtered_threads
├── inbox
├── message_requests
├── stickers_used
├── raw
├── partitioned
```

5. Again in the root directory of `messenger-insights`, run
```
python insights-cli.py
```

Enter the appropriate commands to view the data you want to see!

## Web App

In the `web-app` folder, there is also a Gatsby web app that visualizes a portion of the processed data in a "Spotify Year in Review" style slideshow, as seen in [this demo](https://messenger-insights-demo.netlify.com/).

### Usage

1. If you haven't done so already, do steps 1-4 in the Usage section for the CLI Tool.

2. In the root directory of `messenger-insights`, run
```
python setup-webapp.py
```
This script calculates a couple of metrics on your Messenger usage, and stores the results in a JSON file in `web-app/src/data/stats`. At buildtime, Gatsby will use GraphQL to query this JSON data and inject it into the web pages.

3. Install dependencies and start the web app! Make sure you are running Node version **10.16.x**
```
cd web-app
npm install
npm run develop
```
Navigate to `localhost:8000` and view enjoy
