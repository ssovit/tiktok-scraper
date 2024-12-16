# Unofficial TikTok Scraper API library for Python

**Full source code without any external API server or subscription dependent.**

Includes device registration, activation and all required header and request body generation algorithms.

[![IPRoyal](assets/proxy.jpg)](https://iproyal.com/?r=ttproxy)

# Installation
- `pip install -r requirements.txt`
- `uvicorn main:app --host 0.0.0.0 --port 8100` to uvicorn ASGI server

# Docker?
`docker-compose up --build`

# API Endpoints

### For You Feed
 - / - Get trending tiktok video feed

### Video
- /video/`video_id` - Get video data for TikTok video by video id
- /video/search/`keyword` - Search video by keyword
	 - *cursor* (default: `0`)(parameter) - Pagination cursor
- /video/`video_id`/comments - Get video comments
	 - *cursor* (default: `0`)(parameter) - Pagination cursor


### User 
- /user/`user_id` - Get TikTok user info by user id
- /user/search/`keyword`/feed - Search user by keyword
	- *cursor* (default: `0`)(parameter)
- /user/`user_id`/followers - Get user followers list
	- *cursor* (default: `0`)(parameter)
- /user/`user_id`/following - Get user following list
	- *cursor* (default: `0`)(parameter)
- /user/`user_id`/likes - Get user liked video *(Likes must be public)*
	- *cursor* (default: `0`)(parameter)

### Challenge
- /challenge/`challenge_id` - Get challenge detail by challenge ID
- /challenge/`challenge_id`/posts - Get challenge/tag video feed
	- *cursor* (default: `0`)(parameter) 
- /challenge/search/`keyword` - Search challenge by keyword
	- *cursor* (default: `0`)(parameter) 

### Music
- /music/`music_id` - Get music detail
- /music/`music_id`/posts - Get music video feed
	- *cursor* (default: `0`)(parameter) 
- /music/search/`keyword` - Search challenge by keyword
	- *cursor* (default: `0`)(parameter) 

**Need more endpoints? Let me know.**

# Proxy Support
[![IPRoyal](assets/proxy.jpg)](https://iproyal.com/?r=ttproxy)

Proxies can be configured in `main.py`
```
proxies={http:"http://user:password@proxyhost.com:port",https:"http://user:password@proxyhost.com:port"}
```
It's highly recommended that you use proxy to prevent your IP from getting banned.

It's highly recommended to use Proxy service if you are making lots of requests in short interval of time. [IPRoyal](https://iproyal.com/?r=ttproxy) is good.


# Price?
- Full Scraper API including device registration source code for just USD 400. 
- No Bullshit, I will give you your personalized demo personally.
- No Dependency on extrenal servers or any subscriptions that adds latency to your project. Or even better if using python, could use the functions within your code.
- Pure code that you can run and host for you own. 

# Need more or have a gig?
- Lets talk! contact informations below. 

# Contact
- [Telegram](https://t.me/sovitt)
- [Email](mailto:sovit.tamrakar@gmail.com)
