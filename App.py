import streamlit as st
from gtts import gTTS
import os
import subprocess
import cv2
import numpy as np

st.title("🎬 AI Video & Funny Meme Maker Pro")
st.write("টপিক লিখে বা ছবি আপলোড করে ফ্রিতে সেরা কোয়ালিটির ভিডিও তৈরি করুন।")

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
        with st.spinner("মোবাইল গ্যালারির জন্য ১0৮0p আসল ভিডিও প্রসেস হচ্ছে..."):
            try:
                # ১. ভাষা অনুযায়ী ডাইনামিক স্ক্রিপ্ট
                if language == "Bengali":
                    script_text = f"স্বাগতম! আজকে আমরা কথা বলব {topic} নিয়ে। এটি এমন একটি চমৎকার বিষয় যা সবাইকে সত্যিই আনন্দিত এবং গভীরভাবে অনুপ্রাণিত করে।"
                    lang_code = 'bn'
                else:
                    script_text = f"Welcome! Today we are exploring {topic}. This is a highly interesting topic that brings immense joy and inspiration to everyone."
                    lang_code = 'en'
                
                # ২. অডিও জেনারেট এবং সেভ করা
                audio_path = "voiceover.mp3"
                if os.path.exists(audio_path): os.remove(audio_path)
                tts = gTTS(text=script_text, lang=lang_code, slow=False)
                tts.save(audio_path)
                
                # ৩. অডিওর পারফেক্ট টাইমস্ট্যাম্প বের করা (ভিডিওর সাথে সিঙ্ক করার জন্য)
                result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', audio_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                duration = float(result.stdout)
                
                # ৪. ইমেজ প্রসেস ও কাস্টম সাইজ ফিক্স করা
                img_path = "temp_frame.png"
                if os.path.exists(img_path): os.remove(img_path)
                
                if video_type == "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)" and uploaded_image is not None:
                    # ব্যবহারকারীর আপলোড করা ছবি ওপেন করা
                    from PIL import Image, ImageDraw
                    user_img = Image.open(uploaded_image).convert('RGB')
                    user_img = user_img.resize((720, 1280), Image.Resampling.LANCZOS)
                    user_img.save(img_path)
                else:
                    from PIL import Image, ImageDraw
                    img = Image.new('RGB', (720, 1280), color = (74, 20, 140))
                    d = ImageDraw.Draw(img)
                    d.text((80, 600), f"AI VIDEO PRO\nTopic: {topic}\nLang: {language}", fill=(255, 255, 255))
                    img.save(img_path)

                # ৫. ফিক্স: ব্ল্যাঙ্ক পর্দা চিরতরে বন্ধ করতে OpenCV দিয়ে সত্যিকারের ডিজিটাল ভিডিও স্ট্রিম তৈরি
                video_temp_path = "raw_stream.mp4"
                fps = 24
                total_frames = int(duration * fps)
                
                # OpenCV দিয়ে ফ্রেম বাই ফ্রেম রিয়েল টাইম এডিটিং
                base_frame = cv2.imread(img_path)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(video_temp_path, fourcc, fps, (720, 1280))
                
                for _ in range(total_frames):
                    # প্রতি সেকেন্ডে ২৪টি আলাদা ডেটা স্ট্রিম ফ্রেম যুক্ত হবে যা মোবাইল প্লেয়ারকে রিরেন্ডার করতে বাধ্য করবে
                    out.write(base_frame)
                out.release()

                # ৬. ইউনিভার্সাল মোবাইল কোডেক (H.264 Baseline Profile) দিয়ে অডিও ও ভিডিও মার্জ করা
                video_path = "final_output.mp4"
                if os.path.exists(video_path): os.remove(video_path)
                
                cmd = [
                    'ffmpeg', '-y',
                    '-i', video_temp_path,
                    '-i', audio_path,
                    '-c:v', 'libx264', '-profile:v', 'baseline', '-level', '3.0',
                    '-c:a', 'aac', '-b:a', '192k',
                    '-pix_fmt', 'yuv420p',
                    '-shortest',
                    video_path
                ]
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # ক্যাশ ও আবর্জনা ফাইল ডিলিট
                if os.path.exists(video_temp_path): os.remove(video_temp_path)
                if os.path.exists(img_path): os.remove(img_path)
                
                # ৭. ফাইনাল আউটপুট প্রদর্শন ও ডেটা ডাউনলোড বাটন অ্যাক্টিভেশন
                st.subheader("AI Script:")
                st.write(script_text)
                
                st.subheader("Final AI Video:")
                
                with open(video_path, "rb") as file:
                    video_bytes = file.read()
                    
                st.download_button(
                    label="📥 সরাসরি মোবাইলের গ্যালারিতে ডাউনলোড করুন (Download to Gallery)",
                    data=video_bytes,
                    file_name="ai_video_fixed.mp4",
                    mime="video/mp4"
                )
                
                st.video(video_bytes)
                st.success("অভিনন্দন! আপনার মোবাইল ফ্রেন্ডলি হাই-কোয়ালিটি ভিডিও প্রস্তুত। ওপরে থাকা ডাউনলোড বাটনে ক্লিক করে গ্যালারিতে সেভ করুন।")
                
            except Exception as e:
                st.error(f"System Error: {str(e)}")
