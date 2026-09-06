import streamlit as st
from gtts import gTTS
import os
import subprocess
import time
from PIL import Image, ImageDraw

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
        with st.spinner("সার্ভারে মোবাইল ফ্রেন্ডলি হাই-কোয়ালিটি ভিডিও প্রসেস হচ্ছে..."):
            try:
                # ১. ভাষা অনুযায়ী ডাইনামিক স্ক্রিপ্ট ও ভয়েস ওভার তৈরি (পুরাতন ক্যাশ স্পিচ ফিক্স)
                if language == "Bengali":
                    script_text = f"স্বাগতম! আজকে আমরা কথা বলব {topic} নিয়ে। এটি এমন একটি চমৎকার বিষয় যা সবাইকে সত্যিই আনন্দিত এবং গভীরভাবে অনুপ্রাণিত করে।"
                    lang_code = 'bn'
                else:
                    script_text = f"Welcome! Today we are exploring {topic}. This is a highly interesting topic that brings immense joy and inspiration to everyone."
                    lang_code = 'en'
                
                timestamp = int(time.time())
                audio_path = f"voice_{timestamp}.mp3"
                img_path = f"frame_{timestamp}.png"
                video_path = f"output_{timestamp}.mp4"
                
                tts = gTTS(text=script_text, lang=lang_code, slow=False)
                tts.save(audio_path)
                
                # ২. ইমেজ প্রসেসিং ও সাইজ ফিক্স (কোনো ব্ল্যাঙ্ক স্ক্রিন হবে না)
                if video_type == "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)" and uploaded_image is not None:
                    user_img = Image.open(uploaded_image).convert('RGB')
                    user_img = user_img.resize((720, 1280), Image.Resampling.LANCZOS)
                    user_img.save(img_path)
                else:
                    img = Image.new('RGB', (720, 1280), color = (74, 20, 140))
                    d = ImageDraw.Draw(img)
                    d.text((80, 600), f"AI VIDEO PRO\nTopic: {topic}\nLang: {language}", fill=(255, 255, 255))
                    img.save(img_path)

                # ৩. এরর-ফ্রি শক্তিশালী ইউনিভার্সাল FFmpeg কমান্ড (সরাসরি ভিডিওর ফ্রেম রেন্ডারিং)
                cmd = [
                    'ffmpeg', '-y',
                    '-loop', '1', '-r', '24', '-i', img_path,
                    '-i', audio_path,
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                    '-preset', 'ultrafast', '-tune', 'stillimage',
                    '-c:a', 'aac', '-b:a', '192k',
                    '-shortest',
                    video_path
                ]
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # ৪. স্ক্রিনে আউটপুট প্রদর্শন
                st.subheader("AI Script:")
                st.write(script_text)
                
                st.subheader("Final AI Video:")
                
                with open(video_path, "rb") as file:
                    video_bytes = file.read()
                    
                # গ্যালারিতে সরাসরি ডাউনলোডের জন্য বাটন
                st.download_button(
                    label="📥 সরাসরি মোবাইলে ডাউনলোড করুন (Download to Gallery)",
                    data=video_bytes,
                    file_name=f"ai_video_{timestamp}.mp4",
                    mime="video/mp4"
                )
                
                st.video(video_bytes)
                st.success("অভিনন্দন! আপনার মোবাইল ফ্রেন্ডলি হাই-কোয়ালিটি ভিডিও প্রস্তুত। ওপরে থাকা ডাউনলোড বাটনে ক্লিক করে গ্যালারিতে সেভ করুন।")
                
                # পুরনো টেম্পোরারি ফাইল ক্লিনআপ
                if os.path.exists(audio_path): os.remove(audio_path)
                if os.path.exists(img_path): os.remove(img_path)
                if os.path.exists(video_path): os.remove(video_path)
                
            except Exception as e:
                st.error(f"System Error: {str(e)}")
