import streamlit as st
from gtts import gTTS
import os
import moviepy.editor as mp
from PIL import Image, ImageDraw

st.title("🎬 AI Video & Funny Meme Maker Pro")
st.write("টপিক লিখে বা নিজের ছবি আপলোড করে ফ্রিতে সেরা কোয়ালিটির ভিডিও তৈরি করুন।")

video_type = st.radio("ভিডিওর ধরন বেছে নিন (Select Video Type):", ["Text to Video (সাধারণ টপিক)", "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)"])

topic = st.text_input("ভিডিওর টপিক বা স্ক্রিপ্ট (Topic/Script)", placeholder="Example: Funny Cats, Moon, Success...")
language = st.selectbox("ভাষা (Language)", ["English", "Bengali"])

uploaded_image = None
if video_type == "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)":
    uploaded_image = st.file_uploader("আপনার ছবি বা ফানি ট্রল পিকচার আপলোড করুন (Upload Image):", type=["png", "jpg", "jpeg"])

if st.button("Generate Full Video 🚀"):
    if not topic.strip():
        st.error("Please enter a valid topic or script!")
    elif video_type == "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)" and uploaded_image is None:
        st.error("Please upload an image first!")
    else:
        with st.spinner("আপনার চমৎকার ভিডিওটি তৈরি হচ্ছে, অনুগ্রহ করে একটু অপেক্ষা করুন..."):
            try:
                # ১. ভাষা অনুযায়ী স্ক্রিপ্ট তৈরি
                if language == "Bengali":
                    script_text = f"স্বাগতম! এখানে {topic} সম্পর্কে একটি চমৎকার তথ্য রয়েছে। এটি এমন একটি অনন্য গল্প যা প্রত্যেককে গভীরভাবে অনুপ্রাণিত করে।"
                    lang_code = 'bn'
                else:
                    script_text = f"Welcome! Here is an amazing insight about {topic}. It holds a unique story that inspires everyone who explores it deeper."
                    lang_code = 'en'
                
                # ২. ভয়েস ওভার তৈরি
                audio_path = "voiceover.mp3"
                if os.path.exists(audio_path): os.remove(audio_path)
                tts = gTTS(text=script_text, lang=lang_code, slow=False)
                tts.save(audio_path)
                
                # ৩. ছবি প্রসেস করা
                img_path = "processed_bg.png"
                if os.path.exists(img_path): os.remove(img_path)
                
                if video_type == "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)" and uploaded_image is not None:
                    user_img = Image.open(uploaded_image)
                    user_img = user_img.resize((720, 1280)) # মোবাইল স্ট্যান্ডার্ড সাইজ
                    user_img.save(img_path)
                else:
                    # টেক্সট মোডের জন্য সুন্দর কালার ও টেক্সট
                    img = Image.new('RGB', (720, 1280), color = (74, 20, 140))
                    d = ImageDraw.Draw(img)
                    d.text((80, 600), f"AI VIDEO PRO\nTopic: {topic}\nLang: {language}", fill=(255, 255, 255))
                    img.save(img_path)
                
                # ৪. অডিও ক্লিপ লোড করা
                audio_clip = mp.AudioFileClip(audio_path)
                duration = audio_clip.duration
                
                # ৫. ভিডিওর মোবাইল-ফ্রেন্ডলি ফরম্যাট তৈরি
                video_clip = mp.ImageClip(img_path).set_duration(duration)
                video_clip = video_clip.set_audio(audio_clip)
                
                video_path = "final_output.mp4"
                if os.path.exists(video_path): os.remove(video_path)
                
                # লজিক ফিক্স: pix_fmt="yuv420p" যোগ করা হয়েছে যা সব মোবাইলে ভিডিও প্লে নিশ্চিত করে
                video_clip.write_videofile(
                    video_path, 
                    fps=24, 
                    codec="libx264", 
                    audio_codec="aac",
                    ffmpeg_params=["-pix_fmt", "yuv420p"],
                    temp_audiofile='temp-audio.m4a', 
                    remove_temp=True
                )
                
                audio_clip.close()
                video_clip.close()
                
                # ৬. স্ক্রিনে আউটপুট দেখানো
                st.subheader("AI Script:")
                st.write(script_text)
                
                st.subheader("Final AI Video:")
                st.video(video_path)
                
            except Exception as e:
                st.error(f"System Error: {str(e)}")



