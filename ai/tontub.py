"""
    une app pour repondre aux emails
"""

import streamlit as st
from openai import OpenAI

import ai.config as config

from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from urllib.parse import urlparse, parse_qs
import os
from pathlib import Path

# Setting the title of the Streamlit application
st.title(":material/videocam: TonTub")


st.markdown("Une AI qui te dévoile tout de **TonTub**, sans que tu aies besoin de te tortiller pour regarder dedans.")
st.markdown(""">    TonTub est un service innovant dédié à l\'analyse profonde de vidéos.
                    Grâce à son coloscope boosté à l'intelligence artificielle, 
                    il rapporte ce qu'il voit, segmente les zones d'intérêt et génère un rapport détaillé et précis. 
                    Une solution fiable pour optimiser les diagnostics et gagner en efficacité.""")


if not st.session_state.openai_api_key.startswith('sk-'):
    st.warning(f"Tu as besoin d'une clef API OpenAI !", icon='⚠')
    st.page_link(config.settings_page, label="SVP configure ta clef dans la page ⚙️ Settings")
    st.stop()  # This stops further execution of the script

if not st.session_state.youtube_api_key:
    st.warning(f"TonTub a besoin d'une clef API !", icon='⚠')
    st.page_link(config.settings_page, label="SVP configure ta clef dans la page ⚙️ Settings")
    st.stop()  # This stops further execution of the script

client = OpenAI(api_key=st.session_state.openai_api_key)




def extract_video_id(url):
    """Extract the video ID from a YouTube URL"""
    parsed_url = urlparse(url)
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    return None





def get_video_transcript(video_id, langs=['fr']):
    """Get the transcript of a YouTube video"""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=langs)
        transcript_text = ' '.join([item['text'] for item in transcript_list])
        return transcript_text
    except TranscriptsDisabled:
        return "Transcript is not available for this video."
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"





def get_video_comments(video_id, api_key, max_results=100):
    """Get comments from a YouTube video"""
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Get comment threads
        comments = []
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            textFormat="plainText"
        )

        while request:
            response = request.execute()
            
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'author': comment['authorDisplayName'],
                    'text': comment['textDisplay'],
                    'likes': comment['likeCount'],
                    'published_at': comment['publishedAt']
                })
            
            # Check if there are more comments
            if 'nextPageToken' in response:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=max_results,
                    textFormat="plainText",
                    pageToken=response['nextPageToken']
                )
            else:
                break

        return comments
    except Exception as e:
        return f"Error fetching comments: {str(e)}"




def analyze_youtube_video(video_url, api_key):
    """Main function to analyze a YouTube video"""
    video_id = extract_video_id(video_url)
    if not video_id:
        return "Invalid YouTube URL"

    # Get transcript
    print("Fetching transcript...")
    transcript = get_video_transcript(video_id)

    # Get comments
    print("Fetching comments...")
    comments = get_video_comments(video_id, api_key)

    return {
        'video_id': video_id,
        'transcript': transcript,
        'comments': comments
    }


with st.form("video"):
    video_url = st.text_input("Url de Ton Tube")
    submit = st.form_submit_button("Démarer l'analyse")
    gen = False

    if submit:
        if not video_url  :
            st.warning(f"Indiques l'url de TonTub sous la forme https://www.youtube.com/watch?v=xxxxxxx !", icon='⚠')
        else:
            gen = True


if gen:

    video_id = extract_video_id(video_url)
    if not video_id:
       st.error(f"TOops ton url est toute pourrie", icon='⚠')
       st.stop()
    
    transcript = get_video_transcript(video_id, langs=['fr'])
    comments = get_video_comments(video_id, st.session_state.youtube_api_key, st.session_state.tontub_max_comments)

    st.markdown("### Réponse :")

    current_dir = os.path.dirname(os.path.abspath(__file__))

    pattern = f"{current_dir}/patterns/extract_wisdom"
    with open(f'{pattern}/system.md', 'r') as file:
         systempattern = file.read()

    with open(f'{pattern}/user.md', 'r') as file:
         userpattern= file.read()

    #st.write(systempattern + userpattern +  transcript  )
    #st.stop()
    stream = client.chat.completions.create(
                                messages=[ {"role": "system", "content": systempattern},
                                           {"role": "user", "content": userpattern + "\n" +  transcript + str(comments) }  ],  
                                model = st.session_state.openai_model,
                                temperature = st.session_state.openai_temperature,
                                stream = True
            )
    response = st.write_stream(stream)
    

