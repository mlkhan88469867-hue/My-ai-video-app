import streamlit as st
from gtts import gTTS
import os
import subprocess
import time
from PIL import Image

st.set_page_config(page_title="AI Video Maker Pro", layout="centered")

st.title("🎬 AI Video & Funny Meme Maker Pro")
st.write("টপিক লিখে বা ছবি আপলোড করে ফ্রিতে সেরা কোয়ালিটির ভিডিও তৈরি করুন।")

# কাস্টম রেডিও বাটনের ভ্যালু ফিক্স করা
video_type = st.radio("ভিডিওর ধরন বেছে নিন:", ["Text to Video (সাধারণ টপিক)", "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)"])

topic = st.text_input("ভিডিওর টপিক বা স্ক্রিপ্ট (Topic/Script)", placeholder="Example: Funny Cats, Moon, Success...")
language = st.selectbox("ভাষা (Language)", ["English", "Bengali"])

uploaded_image = None
if video_type == "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)":
    uploaded_image = st.file_uploader("আপনার ছবি আপলোড করুন:", type=["png", "jpg", "jpeg"])

if st.button("Generate Full Video 🚀"):
    if not topic.strip():
        st.error("Please enter a valid topic!")
    elif video_type == "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)" and uploaded_image is None:
        st.error("Please upload an image first!")
    else:
        with st.spinner("ভিডিও তৈরি হচ্ছে, অনুগ্রহ করে একটু অপেক্ষা করুন..."):
            try:
                run_id = str(int(time.time()))
                if language == "Bengali":
                    script_text = f"স্বাগতম! আজকে আমরা কথা বলব {topic} নিয়ে। এটি এমন একটি চমৎকার বিষয় যা সবাইকে সত্যিই আনন্দিত করে।"
                else:
                    script_text = f"Welcome! Today we are exploring {topic}. This is a highly interesting topic that brings immense joy to everyone."
                
                audio_path = f"voice_{run_id}.mp3"
                img_path = f"frame_{run_id}.png"
                video_path = f"video_{run_id}.mp4"
                
                # ১. ভয়েস ওভার তৈরি
                tts = gTTS(text=script_text, lang='bn' if language == "Bengali" else 'en', slow=False)
                tts.save(audio_path)
                
                # ২. ইমেজ প্রসেসিং
                if video_type == "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)" and uploaded_image is not None:
                    user_img = Image.open(uploaded_image).convert('RGB')
                    user_img = user_img.resize((720, 1280), Image.Resampling.LANCZOS)
                    user_img.save(img_path)
                else:
                    from PIL import ImageDraw
                    img = Image.new('RGB', (720, 1280), color = (74, 20, 140))
                    d = ImageDraw.Draw(img)
                    d.text((80, 600), f"AI VIDEO PRO\nTopic: {topic}\nLang: {language}", fill=(255, 255, 255))
                    img.save(img_path)

                # ৩. শক্তিশালী FFmpeg ইউনিভার্সাল ভিডিও জেনারেশন
                cmd = [
                    'ffmpeg', '-y',
                    '-loop', '1', '-r', '24', '-i', img_path,
                    '-i', audio_path,
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                    '-preset', 'ultrafast', '-tune', 'stillimage',
                    '-c:a', 'aac', '-b:a', '128k',
                    '-shortest',
                    video_path
                ]
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # ৪. স্ক্রিনে আউটপুট প্রদর্শন
                st.subheader("AI Script:")
                st.write(script_text)
                
                st.subheader("Final AI Video:")
                
                # ভিডিও ফাইল রিড করা
                with open(video_path, "rb") as file:
                    video_bytes = file.read()
                
                # গ্যালারিতে সরাসরি ডাউনলোডের জন্য বাটন
                st.download_button(
                    label="📥 সরাসরি মোবাইলে ডাউনলোড করুন (Download Video)",
                    data=video_bytes,
                    file_name=f"ai_video_{run_id}.mp4",
                    mime="video/mp4"
                )
                
                # ফিক্স: এরর-ফ্রি সরাসরি ভিডিও প্লেয়ার মডিউল (HTML5 এর বদলে সরাসরি স্ট্রিমিং)
                st.video(video_bytes, format="video/mp4")
                st.success("ভিডিও সফলভাবে তৈরি হয়েছে!")
                
                # ক্ষণস্থায়ী ফাইল মুছে ফেলা
                if os.path.exists(audio_path): os.remove(audio_path)
                if os.path.exists(img_path): os.remove(img_path)
                if os.path.exists(video_path): os.remove(video_path)
                
            except Exception as e:
                st.error(f"System Error: {str(e)}")
