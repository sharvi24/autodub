# autodub

Given a YouTube link, I've build a pipeline to create a fully automated dubbed video.

I have created a server that takes in a YouTube URL and returns an “auto-dubbed” video in the target language specified. The audio is reasonably aligned to the video(achieved by using time-stamped transcriptions and custom alignemnt function) and is as close as possible to the original. 

As we know that automated dubs can be flawed: incorrect transcriptions, mistranslations, and botty synthesis can make the result unnatural. In this work, I've not deeply focused on handling these imperfections. 

Dubbing a video requires 3 main steps: transcription, translation, and resynthesis. My pipeline used these steps to create a new “dubbed” audio track that will then be overlayed onto the video. 

Steps:
1. `youtube-transcripts-api`: Used python API to get the transcripts/subtitles for a given YouTube video along with timestamps of these transcriptions.

2. `googletrans`: Used this free Google Translate API for Python to get transciptions translated to the target language of dubbed video.

3. `ElevenLabs`: Used this API to generate realistic speech for given text snippets. It can a generate realistic audio for multiple langauges in various provided voices as well as required voices by passing few audio samples. The API service provides this for free for upto 10000 characters total of the texts.
