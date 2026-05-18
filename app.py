import streamlit as str
from openai import OpenAI
from audio_recorder_component import audio_recorder

# 1. Αρχικοποίηση OpenAI
client = OpenAI(api_key=str.secrets["OPENAI_API_KEY"])

str.title("🎙️ Global AI Phone Note Taker")
str.write("Πατήστε το μικρόφωνο για να ξεκινήσει η καταγραφή της κλήσης σας.")

# 2. Προσθήκη του Live Audio Recorder στην οθόνη
audio_bytes = audio_recorder(
    text="Πατήστε για εγγραφή",
    recording_color="#e74c3c",
    neutral_color="#34495e",
    icon_name="microphone",
    icon_size="2x"
)

if audio_bytes:
    # Μόλις σταματήσει η εγγραφή, το AI ξεκινάει αμέσως
    with str.spinner("🤖 Το AI επεξεργάζεται την κλήση σας live..."):
        try:
            # Αποθήκευση του ήχου σε προσωρινό αρχείο για το Whisper
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_bytes)
            
            with open("temp_audio.wav", "rb") as audio_file:
                # ΒΗΜΑ A: Μετατροπή ομιλίας σε κείμενο
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
            
            text_result = transcript.text
            
            # ΒΗΜΑ B: Δημιουργία Περίληψης
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are an expert assistant. Analyze the phone call transcript. "
                            "Provide a structured summary containing: "
                            "1) Client Name & Contact Info, "
                            "2) Main Topic/Request, "
                            "3) Action Items / To-Do List. "
                            "Always reply in the same language used in the transcript."
                        )
                    },
                    {"role": "user", "content": text_result}
                ]
            )
            
            ai_summary = response.choices[0].message.content

            # Εμφάνιση αποτελεσμάτων
            str.success("Η ανάλυση ολοκληρώθηκε!")
            str.subheader("📝 Σύνοψη & Εκκρεμότητες (AI Summary)")
            str.write(ai_summary)
            
            with str.expander("Δείτε όλο το γραπτό κείμενο (Full Transcript)"):
                str.write(text_result)
                
        except Exception as e:
            str.error(f"Προέκυψε σφάλμα: {e}")

