import streamlit as st
from gtts import gTTS
import os
from moviepy.editor import ImageClip, AudioFileClip
from PIL import Image, ImageDraw

st.title("🎬 AI Full Video Maker Pro")
st.write("টপিক লিখে জেনারেট করুন এবং সরাসরি .mp4 ভিডিও ফাইল ডাউনলোড করুন।")

topic = st.text_input("Topic", placeholder="Example: Moon, Cats, Success...")
language = st.selectbox("Language", ["English", "Bengali"])

if st.button("Generate Full Video 🚀"):
    if not topic.strip():
        st.error("Please enter a valid topic!")
    else:
        with st.spinner("ভিডিও তৈরি হচ্ছে, অনুগ্রহ করে একটু অপেক্ষা করুন..."):
            try:
                script_text = f"Welcome! Here is an amazing insight about {topic}. It holds a unique story that inspires everyone who explores it deeper. Keep learning and keep exploring!"
                
                lang_code = 'bn' if language == "Bengali" else 'en'
                tts = gTTS(text=script_text, lang=lang_code, slow=False)
                audio_path = "voiceover.mp3"
                if os.path.exists(audio_path): os.remove(audio_path)
                tts.save(audio_path)
                
                img = Image.new('RGB', (720, 1280), color = (30, 30, 50))
                d = ImageDraw.Draw(img)
                d.text((50, 600), f"AI Video about:\n{topic}", fill=(255, 255, 255))
                img_path = "background.png"
                img.save(img_path)
                
                audio_clip = AudioFileClip(audio_path)
                video_duration = audio_clip.duration
                
                video_clip = ImageClip(img_path).set_duration(video_duration)
                final_video = video_clip.set_audio(audio_clip)
                
                video_path = "final_output.mp4"
                if os.path.exists(video_path): os.remove(video_path)
                
                final_video.write_videofile(video_path, fps=15, codec="libx264", audio_codec="aac")
                
                audio_clip.close()
                video_clip.close()
                
                st.subheader("AI Script:")
                st.write(script_text)
                
                st.subheader("Final AI Video:")
                st.video(video_path)
                
            except Exception as e:
                st.error(f"System Error: {str(e)}")
