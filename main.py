#!encoding=utf8

from contextlib import asynccontextmanager
import time
from fastapi import FastAPI, HTTPException, Query
import os
import json
from TikTokApi.flow import Flow
from TikTokApi.tiktok import TikTok
from TikTokApi.api import Api
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

from get_random_device import DEVICES_DIR, get_random_device


"""
Update this to use proxies

Example:

proxies={http:"http://user:password@proxyhost.com:port",https:"http://user:password@proxyhost.com:port"}

"""
proxies = None


def cleanup_old_files(days: int = 1):
    now = time.time()
    cutoff = now - (days * 86400)  # Convert days to seconds
    for filename in os.listdir(DEVICES_DIR):
        file_path = os.path.join(DEVICES_DIR, filename)
        if os.path.isfile(file_path) and filename.endswith(".json"):
            file_mtime = os.path.getmtime(file_path)
            if file_mtime < cutoff:
                os.remove(file_path)
                print(f"Removed stale devices: {file_path}")


async def background_device_register():
    try:
        cleanup_old_files(days=1)
        instance = TikTok(proxies=proxies, debug=False)
        flow = Flow(instance)
        await flow.device_register()
        device_id = instance.device["device_id"]
        file_path = os.path.join(DEVICES_DIR, f"{device_id}.json")
        del instance.device["proxies"]
        print("Device Registered")
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(instance.device, file, ensure_ascii=False, indent=4, sort_keys=True)
    except Exception as e:
        pass


def sync_background_device_register():
    asyncio.run(background_device_register())


def tiktok_api():
    instance = TikTok(debug=False)
    instance.device = get_random_device()
    instance.request.proxies = proxies
    api = Api(instance)
    return api


# Schedule the background task
scheduler = BackgroundScheduler()
# Register new device every x minutes and store it in devices dir
scheduler.add_job(sync_background_device_register, 'interval', minutes=5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await background_device_register()
    # Start the scheduler
    scheduler.start()
    yield
    scheduler.shutdown()
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def feed(cursor: int = Query(0, description="Cursor for pagination, defaults to 0 if not provided")):
    try:
        return await tiktok_api().aweme_v1.feed(max_cursor=cursor)
    except Exception as e:
        return HTTPException(status_code=500, detail="Internal Server Error")

"""
Video Endpoints
"""


@app.get("/video/{video_id}")
async def video_detail(video_id: str):
    try:
        return await tiktok_api().aweme_v1.aweme_detail(video_id)
    except Exception as e:
        return HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/video/search/{keyword}")
async def search_video(keyword: str, cursor: int = Query(0, description="Cursor for pagination, defaults to 0 if not provided")):
    try:
        return await tiktok_api().aweme_v1.search_item(keyword, offset=cursor)
    except Exception as e:
        return HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/video/{aweme_id}/comments")
async def video_comments(aweme_id: str, cursor: int = Query(0, description="Cursor for pagination, defaults to 0 if not provided")):
    try:

        return await tiktok_api().aweme_v1.comment_list(aweme_id=aweme_id, cursor=cursor)
    except Exception as e:
        return HTTPException(status_code=500, detail="Internal Server Error")


"""
User Endpoints
"""


@app.get("/user/search/{username}")
async def search_user(username: str, cursor: int = Query(0, description="Cursor for pagination, defaults to 0 if not provided")):
    try:
        return await tiktok_api().aweme_v1.user_search(username, cursor=cursor)
    except Exception as e:
        return HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/user/{user_id}")
async def user_detail(user_id: str):
    try:
        return await tiktok_api().aweme_v1.user_profile_other(user_id=user_id)
    except Exception as e:
        return HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/user/{user_id}/posts")
async def user_videos(user_id: str, cursor: int = Query(0, description="Cursor for pagination, defaults to 0 if not provided")):
    try:
        return await tiktok_api().aweme_v1.aweme_post(user_id=user_id, max_cursor=cursor)
    except Exception as e:
        return HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/user/{user_id}/followers")
async def user_followers(user_id: str, cursor: int = Query(0, description="Cursor for pagination, defaults to 0 if not provided")):
    try:
        return await tiktok_api().aweme_v1.user_follower_list(user_id=user_id, max_time=cursor)
    except Exception as e:
        return HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/user/{user_id}/following")
async def user_followings(user_id: str, cursor: int = Query(0, description="Cursor for pagination, defaults to 0 if not provided")):
    try:

        return await tiktok_api().aweme_v1.user_following_list(user_id=user_id, max_time=cursor)
    except Exception as e:
        return HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/user/{user_id}/likes")
async def user_likes(user_id: str, cursor: int = Query(0, description="Cursor for pagination, defaults to 0 if not provided")):
    try:
        return await tiktok_api().aweme_v1.user_likes(user_id=user_id, max_cursor=cursor)
    except Exception as e:
        return HTTPException(status_code=500, detail="Internal Server Error")

"""
Challenge
"""


@app.get("/challenge/{challenge_id}/posts")
async def challenge_posts(challenge_id: str, cursor: int = Query(0, description="Cursor for pagination, defaults to 0 if not provided")):
    try:
        return await tiktok_api().aweme_v1.challenge_aweme(ch_id=challenge_id, cursor=cursor)
    except Exception as e:
        return HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/challenge/search/{keyword}")
async def search_challenge(keyword: str, cursor: int = Query(0, description="Cursor for pagination, defaults to 0 if not provided")):
    try:
        return await tiktok_api().aweme_v1.search_challenge(keyword, cursor=cursor)
    except Exception as e:
        return HTTPException(status_code=500, detail="Internal Server Error")

"""
Music
"""


@app.get("/music/{music_id}")
async def music_detail(music_id: str):
    try:
        return await tiktok_api().aweme_v1.music_detail(music_id=music_id)
    except Exception as e:
        return HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/music/{music_id}/posts")
async def music_posts(music_id: str, cursor: int = Query(0, description="Cursor for pagination, defaults to 0 if not provided")):
    try:
        return await tiktok_api().aweme_v1.music_aweme(music_id=music_id, cursor=cursor)
    except Exception as e:
        return HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/music/search/{keyword}")
async def search_music(keyword: str, cursor: int = Query(0, description="Cursor for pagination, defaults to 0 if not provided")):
    try:
        return await tiktok_api().aweme_v1.search_music(keyword, cursor=cursor)
    except Exception as e:
        return HTTPException(status_code=500, detail="Internal Server Error")
"""

Start ASGI Server

uvicorn main:app --reload --host 0.0.0.0 --port 8100
 
"""
