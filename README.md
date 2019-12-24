# messenger-insights

CLI tool to calculate and display cool stats about your messenger history 👀

![messenger-cli](https://user-images.githubusercontent.com/35405685/71392995-5eb05700-25d8-11ea-8257-7d536fd77516.gif)
![image](https://user-images.githubusercontent.com/35405685/71393067-b6e75900-25d8-11ea-83cf-f869c1492f9b.png)
(^ fake data btw)

## Usage

1. [Download your Facebook Messenger data](https://www.zapptales.com/en/download-facebook-messenger-chat-history-how-to/). Extract the files to a directory of your choice. After you're done, your directory should have the following structure:
```
D:/your/path/to/facebook-data
├── archived_threads
├── filtered_threads
├── inbox
├── message_requests
├── stickers_used
```

2. Clone the repo

```
git clone https://github.com/austichen/messenger-insights.git
cd messenger-insights
```

3. In the `utils/constants.py` file, change the `FB_DATA_DIRECTORY` variable to be the absolute path to the directory you specified in step 1. Using my example in step 1, I would update it to `FB_DATA_DIRECTORY='D:/your/path/to/facebook-data'`

4. In the root directory of `messenger-insights`, run
```
python setup.py
```
Your messenger data folder should be updated with two new folders, `raw` and `partitioned`:
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
