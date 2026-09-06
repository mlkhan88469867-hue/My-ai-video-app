
import streamlit as st
from gtts import gTTS
import os
import moviepy.video.io.ImageSequenceClip as ImageSequenceClip
import moviepy.audio.io.AudioFileClip as AudioFileClip
from PIL import Image, ImageDraw

st.title("🎬 AI Video & Funny Meme Maker Pro")
st.write("টপিক লিখে বা নিজের ছবি আপলোড করে ফ্রিতে সেরা কোয়ালিটির ফানি ভিডিও তৈরি করুন।")

# ভিডিওর টাইপ সিলেক্ট করার অপশন
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
                    script_text = f"স্বাগতম! এখানে {topic} সম্পর্কে একটি চমৎকার তথ্য রয়েছে। এটি এমন একটি অনন্য গল্প যা প্রত্যেককে গভীরভাবে অনুপ্রাণিত করে। নতুন কিছু শিখতে থাকুন এবং অন্বেষণ করতে থাকুন!"
                    lang_code = 'bn'
                else:
                    script_text = f"Welcome! Here is an amazing insight about {topic}. It holds a unique story that inspires everyone who explores it deeper. Keep learning and keep exploring!"
                    lang_code = 'en'
                
                # ২. ভয়েস ওভার তৈরি
                audio_path = "voiceover.mp3"
                if os.path.exists(audio_path): os.remove(audio_path)
                tts = gTTS(text=script_text, lang=lang_code, slow=False)
                tts.save(audio_path)
                
                # ৩. ছবি প্রসেস করা (ভিডিওর ভিজ্যুয়াল)
                img_path = "processed_bg.png"
                if os.path.exists(img_path): os.remove(img_path)
                
                if video_type == "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)" and uploaded_image is not None:
                    # ব্যবহারকারীর আপলোড করা ছবি প্রসেস করা
                    user_img = Image.open(uploaded_image)
                    # ভিডিও স্ট্যান্ডার্ড সাইজে (720x1280) রূপান্তর বা রিসাইজ করা
                    user_img = user_img.resize((720, 1280))
                    user_img.save(img_path)
                else:
                    # সাধারণ টেক্সট ভিডিওর জন্য ব্যাকগ্রাউন্ড
                    img = Image.new('RGB', (720, 1280), color = (74, 20, 140))
                    d = ImageDraw.Draw(img)
                    d.text((80, 600), f"AI VIDEO PRO\nTopic: {topic}\nLang: {language}", fill=(255, 255, 255))
                    img.save(img_path)
                
                # ৪. অডিও দৈর্ঘ্য নির্ধারণ
                audio_clip = AudioFileClip.AudioFileClip(audio_path)
                duration = audio_clip.duration
                
                # ৫. প্রতি সেকেন্ডে ২৪ ফ্রেমে ভিডিও সিকোয়েন্স তৈরি
                fps = 24
                total_frames = int(duration * fps)
                frames = [img_path] * total_frames
                
                # ৬. ভিডিও এবং অডিও মার্জ করা
                video_clip = ImageSequenceClip.ImageSequenceClip(frames, fps=fps)
                video_clip = video_clip.with_audio(audio_clip)
                
                video_path = "final_output.mp4"
                if os.path.exists(video_path): os.remove(video_path)
                
                # ভিডিও ফাইল রেন্ডারিং
                video_clip.write_videofile(video_path, codec="libx264", audio_codec="aac", fps=fps)
                
                audio_clip.close()
                video_clip.close()
                
                # ৭. স্ক্রিনে আউটপুট দেখানো
                st.subheader("AI Script:")
                st.write(script_text)
                
                st.subheader("Final AI Video:")
                st.video(video_path)
                
            except Exception as e:
                st.error(f"System Error: {str(e)}")
