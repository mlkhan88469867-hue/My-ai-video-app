import streamlit as st
from gtts import gTTS
import os
import subprocess
from PIL import Image, ImageDraw

st.title("🎬 AI Video & Funny Meme Maker Pro")
st.write("টপিক লিখে বা ছবি আপলোড করে ফ্রিতে সেরা কোয়ালিটির ভিডিও তৈরি করুন।")

video_type = gr = st.radio("ভিডিওর ধরন বেছে নিন (Select Video Type):", ["Text to Video (সাধারণ টপিক)", "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)"])

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
                # ১. স্ক্রিপ্ট তৈরি
                if language == "Bengali":
                    script_text = f"স্বাগতম! এখানে {topic} সম্পর্কে একটি চমৎকার তথ্য রয়েছে। এটি এমন একটি অনন্য গল্প যা প্রত্যেককে গভীরভাবে অনুপ্রাণিত করে।"
                    lang_code = 'bn'
                else:
                    script_text = f"Welcome! Here is an amazing insight about {topic}. It holds a unique story that inspires everyone who explores it deeper."
                    lang_code = 'en'
                
                # ২. ভয়েস ওভার তৈরি (MP3)
                audio_path = "voiceover.mp3"
                if os.path.exists(audio_path): os.remove(audio_path)
                tts = gTTS(text=script_text, lang=lang_code, slow=False)
                tts.save(audio_path)
                
                # ৩. ইমেজ প্রসেস ও রিসাইজ করা
                img_path = "processed_bg.png"
                if os.path.exists(img_path): os.remove(img_path)
                
                if video_type == "Upload Image (ছবি দিয়ে ফানি/কাস্টম/মেমে ভিডিও)" and uploaded_image is not None:
                    user_img = Image.open(uploaded_image)
                    user_img = user_img.resize((720, 1280))
                    user_img.save(img_path)
                else:
                    img = Image.new('RGB', (720, 1280), color = (74, 20, 140))
                    d = ImageDraw.Draw(img)
                    d.text((80, 600), f"AI VIDEO PRO\nTopic: {topic}\nLang: {language}", fill=(255, 255, 255))
                    img.save(img_path)

                # ৪. FFmpeg এর মাধ্যমে অডিওর ডিউরেশন অনুযায়ী পারফেক্ট মোবাইল ফ্রেন্ডলি MP4 ভিডিও তৈরি
                video_path = "final_output.mp4"
                if os.path.exists(video_path): os.remove(video_path)
                
                # শক্তিশালী কোডেক কমান্ড যা মোবাইল ব্রাউজারে ব্ল্যাঙ্ক স্ক্রিন হওয়া বন্ধ করে
                cmd = [
                    'ffmpeg', '-y',
                    '-loop', '1', '-i', img_path,
                    '-i', audio_path,
                    '-c:v', 'libx264', '-tune', 'stillimage',
                    '-c:a', 'aac', '-b:a', '192k',
                    '-pix_fmt', 'yuv420p',
                    '-shortest',
                    video_path
                ]
                
                # কমান্ডটি ব্যাকএন্ডে রান করা
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # ৫. স্ক্রিনে আউটপুট দেখানো
                st.subheader("AI Script:")
                st.write(script_text)
                
                st.subheader("Final AI Video:")
                
                # ভিডিও ফাইলটি সরাসরি বাইনারি মোডে রিড করা
                with open(video_path, "rb") as file:
                    video_bytes = file.read()
                    
                # গ্যালারিতে সরাসরি ডাউনলোডের জন্য বাটন
                st.download_button(
                    label="📥 সরাসরি মোবাইলে ডাউনলোড করুন (Download Video to Gallery)",
                    data=video_bytes,
                    file_name="ai_video.mp4",
                    mime="video/mp4"
                )
                
                # ফাইনাল ভিডিও প্লেয়ার
                st.video(video_bytes)
                
                st.success("ভিডিওটি সফলভাবে তৈরি হয়েছে! যদি প্লেয়ার লোড হতে সময় নেয়, তবে ওপরে থাকা ডাউনলোড বাটনে ক্লিক করে এটি আপনার মোবাইলে সেভ করে নিন।")
                
            except Exception as e:
                st.error(f"System Error: {str(e)}")
