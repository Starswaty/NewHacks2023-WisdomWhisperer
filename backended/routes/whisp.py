# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import json

from flask import Blueprint, jsonify, request, make_response
import openai
import os
import shutil
from dotenv import load_dotenv
import re
import redis

whisp = Blueprint('whisp', __name__)

from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import (
    OpenAIWhisperParser,
)
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY
PROCESSED_DB_HOST = os.getenv('PROCESSED_DB_HOST')
PROCESSED_DB_PORT = os.getenv('PROCESSED_DB_PORT')
PROCESSED_DB_PASSWORD = os.getenv('PROCESSED_DB_PASSWORD')


# @whisp.route('/transcribe', methods=['POST'])
def transcribe(yturl):
    return_text = ""
    try:
        # data = request.get_json()
        # yturl = data.get('yturl')
        urls = [yturl]
        regex = "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?$"
        uuid = re.search(regex, yturl, re.IGNORECASE).group(6)
        try:
            # Directory to save audio files
            save_dir = "../Downloads/YouTube"
            # https://stackoverflow.com/questions/19377262/regex-for-youtube-url

            # Transcribe the videos to text
            loader = GenericLoader(YoutubeAudioLoader(urls, save_dir), OpenAIWhisperParser())
            docs = loader.load()
            try:
                for video in docs:
                    print(video.page_content)
                    return_text += " " + video.page_content
                for filename in os.listdir(save_dir):
                    file_path = os.path.join(save_dir, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
                response = {"transcription": str(return_text), "uuid": uuid, "response": 200}
                return response
            except:
                return jsonify({"message": "We hit an error", "response": 500})
        except:
            return jsonify({"message": "Error transcribing", "response": 500})
    except:
        return jsonify({"message": "Error with URL", "response": 500})

@whisp.route('/add', methods=['POST'])
def add():
    try:
        data = request.get_json()
        yturl = data.get('yturl')
        regex = "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?$"
        uuid = re.search(regex, yturl, re.IGNORECASE).group(6)
        redis_client = redis.Redis(
            host=PROCESSED_DB_HOST,
            port=PROCESSED_DB_PORT,
            password=PROCESSED_DB_PASSWORD)
        # https://redis-py.readthedocs.io/en/stable/commands.html#redis.commands.core.CoreCommands.sismember
        if not redis_client.sismember("uuid", uuid) == 0:
            return jsonify("Video has already been processed"), 400
        else:
            try:
                transcription = transcribe(yturl)
                print(transcription)
                if transcription['response'] == 200:
                    return transcription
                else:
                    return jsonify("We hit an error"), 500
            # except:
            #     return jsonify("We hit an error"), 500
            except Exception as error:
                # return jsonify("Error with URL"), 400
                return jsonify("Error with URL", error), 400
    # except:
    except Exception as error:
        # return jsonify("Error with URL"), 400
        return jsonify("Error with URL", error), 400

# except Exception as error: