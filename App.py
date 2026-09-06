import streamlit as st
from gtts import gTTS
import os
import subprocess
from PIL import Image, ImageDraw

st.title("🎬 AI Video & Funny Meme Maker Pro")
st.write("টপিক লিখে বা ছবি আপলোড করে ফ্রিতে সেরা কোয়ালিটির ভিডিও তৈরি করুন।")

# মেমোরি লিক এবং লোডিং সমস্যা দূর করতে কাস্টম স্টেট সেটআপ
if 'video_ready' not in st.session_state:
    st.session_state.video_ready = False

video_type = st.radio("ভিডিওর ধরন বেছে নিন (Select Video Type):", ["Text to Video (সাধারণ টপিক)", "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)"])

topic = st.text_input("ভিডিওর টপিক বা স্ক্রিপ্ট (Topic/Script)", placeholder="Example: Funny Cats, Moon, Success...")
language = st.selectbox("ভাষা (Language)", ["English", "Bengali"])

uploaded_image = None
if video_type == "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)":
    # ক্লিয়ার ইন্টারফেস লোডিং ফিক্স
    uploaded_image = st.file_uploader("আপনার ছবি বা ফানি ট্রল পিকচার আপলোড করুন (Upload Image):", type=["png", "jpg", "jpeg"], key="user_meme_uploader")

if st.button("Generate Full Video 🚀"):
    if not topic.strip():
        st.error("Please enter a valid topic or script!")
    elif video_type == "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)" and uploaded_image is None:
        st.error("Please upload an image first!")
    else:
        with st.spinner("আপনার চমৎকার ভিডিওটি তৈরি হচ্ছে, অনুগ্রহ করে একটু অপেক্ষা করুন..."):
            try:
                # ডাইনামিক স্ক্রিপ্ট লজিক (একই স্পিচ বারবার আসা বন্ধ করার ফিক্স)
                if language == "Bengali":
                    script_text = f"স্বাগতম! আজকে আমরা কথা বলব {topic} নিয়ে। এটি এমন একটি চমৎকার বিষয় যা সবাইকে সত্যিই আনন্দিত এবং গভীরভাবে অনুপ্রাণিত করে।"
                    lang_code = 'bn'
                else:
                    script_text = f"Welcome! Today we are exploring {topic}. This is a highly interesting topic that brings immense joy and inspiration to everyone."
                    lang_code = 'en'
                
                # নতুন নতুন ফাইলের নাম ব্যবহার করা যেন ব্রাউজার পুরাতন ক্যাশ ফাইল না দেখায়
                import time
                timestamp = int(time.time())
                audio_path = f"voiceover_{timestamp}.mp3"
                img_path = f"processed_bg_{timestamp}.png"
                video_path = f"final_output_{timestamp}.mp4"
                
                # ভয়েস ওভার তৈরি (MP3)
                tts = gTTS(text=script_text, lang=lang_code, slow=False)
                tts.save(audio_path)
                
                # ইমেজ সাইজ অপটিমাইজেশন (লোডিং আটকে যাওয়া বন্ধ করার ফিক্স)
                if video_type == "Upload Image (ছবি দিয়ে ফানি/কাস্টম ভিডিও)" and uploaded_image is not None:
                    user_img = Image.open(uploaded_image)
                    user_img = user_img.convert('RGB')
                    user_img = user_img.resize((720, 1280), Image.Resampling.LANCZOS)
                    user_img.save(img_path, "PNG", quality=85)
                else:
                    img = Image.new('RGB', (720, 1280), color = (74, 20, 140))
                    d = ImageDraw.Draw(img)
                    d.text((80, 600), f"AI VIDEO PRO\nTopic: {topic}\nLang: {language}", fill=(255, 255, 255))
                    img.save(img_path)

                # শক্তিশালী এবং দ্রুততম FFmpeg কম্পিলেশন
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
                
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # স্ক্রিনে আউটপুট দেখানো
                st.subheader("AI Script:")
                st.write(script_text)
                
                st.subheader("Final AI Video:")
                
                with open(video_path, "rb") as file:
                    video_bytes = file.read()
                    
                st.download_button(
                    label="📥 সরাসরি মোবাইলে ডাউনলোড করুন (Download Video to Gallery)",
                    data=video_bytes,
                    file_name=f"ai_video_{timestamp}.mp4",
                    mime="video/mp4"
                )
                
                st.video(video_bytes)
                st.success("ভিডিওটি সফলভাবে তৈরি হয়েছে! যদি মোবাইল ব্রাউজারে ভিডিও দেখতে সমস্যা হয়, তবে ওপরের ডাউনলোড বাটনে ক্লিক করে গ্যালারিতে সেভ করে নিন।")
                
                # তৈরি শেষ হলে পুরনো ক্যাশ ফাইলগুলো সার্ভার থেকে ক্লিনআপ বা মুছে দেওয়া
                if os.path.exists(audio_path): os.remove(audio_path)
                if os.path.exists(img_path): os.remove(img_path)
                
            except Exception as e:
                st.error(f"System Error: {str(e)}")
