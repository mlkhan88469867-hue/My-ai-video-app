import streamlit as st
from gtts import gTTS
import os
import subprocess
import time
import base64
from PIL import Image

st.set_page_config(page_title="AI Video Maker Pro", layout="centered")

st.title("🎬 AI Video & Funny Meme Maker Pro")
st.write("টপিক লিখে বা ছবি আপলোড করে ফ্রিতে সেরা কোয়ালিটির ভিডিও তৈরি করুন।")

video_type = st.radio("ভিডিওর ধরন বেছে নিন:", ["Text to Video (সাধারণ টপিক)", "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)"])

topic = st.text_input("ভিডিওর টপিক বা স্ক্রিপ্ট (Topic/Script)", placeholder="Example: Funny Cats, Moon, Success...")
language = st.selectbox("ভাষা (Language)", ["English", "Bengali"])

uploaded_image = None
if video_type == "Upload Image (ছবি দিয়ে ফানি/কাস্টম/মেমে ভিডিও)":
    uploaded_image = st.file_uploader("আপনার ছবি আপলোড করুন:", type=["png", "jpg", "jpeg"])

if st.button("Generate Full Video 🚀"):
    if not topic.strip():
        st.error("Please enter a valid topic!")
    elif video_type == "Upload Image (ছবি দিয়ে ফানি/কাস্টম/মেমে ভিডিও)" and uploaded_image is None:
        st.error("Please upload an image first!")
    else:
        with st.spinner("ভিডিও তৈরি হচ্ছে, অনুগ্রহ করে একটু অপেক্ষা করুন..."):
            try:
                # ১. প্রতিবার আলাদা স্পীচ নিশ্চিত করার লজিক (ক্যাশ মেমোরি ফিক্স)
                run_id = str(int(time.time()))
                if language == "Bengali":
                    script_text = f"স্বাগতম! আজকে আমরা কথা বলব {topic} নিয়ে। এটি অত্যন্ত চমৎকার একটি বিষয় যা সবাইকে সত্যিই আনন্দিত করে।"
                else:
                    script_text = f"Welcome! Today we are exploring {topic}. This is a highly interesting topic that brings immense joy to everyone."
                
                audio_path = f"voice_{run_id}.mp3"
                img_path = f"frame_{run_id}.png"
                video_path = f"video_{run_id}.mp4"
                
                # ২. ভয়েস ওভার তৈরি
                tts = gTTS(text=script_text, lang='bn' if language == "Bengali" else 'en', slow=False)
                tts.save(audio_path)
                
                # ৩. ইমেজ সাইজ প্রসেসিং ও ফিক্স
                if video_type == "Upload Image (ছবি দিয়ে ফানি/কাস্টম/মেমে ভিডিও)" and uploaded_image is not None:
                    user_img = Image.open(uploaded_image).convert('RGB')
                    user_img = user_img.resize((720, 1280), Image.Resampling.LANCZOS)
                    user_img.save(img_path)
                else:
                    # সাধারণ মোডের জন্য সুন্দর ডিফল্ট রঙিন ব্যাকগ্রাউন্ড
                    from PIL import ImageDraw
                    img = Image.new('RGB', (720, 1280), color = (74, 20, 140))
                    d = ImageDraw.Draw(img)
                    d.text((80, 600), f"AI VIDEO PRO\nTopic: {topic}\nLang: {language}", fill=(255, 255, 255))
                    img.save(img_path)

                # ৪. ইউনিভার্সাল মোবাইল ফ্রেন্ডলি FFmpeg কমান্ড (কালো পর্দা চিরতরে ফিক্স)
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
                
                # ৫. ফিক্সড HTML5 কাস্টম ভিডিও স্ট্রিমিং লেআউট
                with open(video_path, "rb") as file:
                    video_bytes = file.read()
                
                b64_video = base64.b64encode(video_bytes).decode()
                video_html = f'''
                    <video width="100%" controls playsinline style="border-radius:10px; background-color:#000;">
                        <source src="data:video/mp4;base64,{b64_video}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                '''
                
                st.subheader("AI Script:")
                st.write(script_text)
                
                st.subheader("Final AI Video:")
                st.markdown(video_html, unsafe_html=True)
                
                # গ্যালারিতে সরাসরি ডাউনলোডের জন্য মেমোরি বাটন
                st.download_button(
                    label="📥 সরাসরি মোবাইলে ডাউনলোড করুন (Download Video)",
                    data=video_bytes,
                    file_name=f"ai_video_{run_id}.mp4",
                    mime="video/mp4"
                )
                st.success("ভিডিও সফলভাবে তৈরি হয়েছে!")
                
                # ক্ষণস্থায়ী টেম্প ফাইল মুছে ফেলা
                if os.path.exists(audio_path): os.remove(audio_path)
                if os.path.exists(img_path): os.remove(img_path)
                if os.path.exists(video_path): os.remove(video_path)
                
            except Exception as e:
                st.error(f"System Error: {str(e)}")
