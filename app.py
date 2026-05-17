import streamlit as str
from openai import OpenAI

# 1. Αρχικοποίηση του OpenAI Client (Χρειάζεται το API Key σας)
# Μπορείτε να το βάλετε απευθείας εδώ ή ως περιβαλλοντική μεταβλητή
client = OpenAI(api_key="OPENAI_API_KEY")

str.title("🎙️ Global AI Phone Note Taker")
str.write("Ανεβάστε την ηχογράφηση της κλήσης σας (σε οποιαδήποτε γλώσσα).")

# 2. Στοιχείο για ανέβασμα αρχείου ήχου (mp3, wav, m4a)
uploaded_file = str.file_uploader("Επιλέξτε αρχείο ήχου...", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    str.audio(uploaded_file, format="audio/mp3")
    
    if str.button("🤖 Ανάλυση Κλήσης με AI"):
        with str.spinner("Το AI επεξεργάζεται την κλήση..."):
            try:
                # ΒΗΜΑ A: Μετατροπή ομιλίας σε κείμενο (Speech-to-Text)
                # Το Whisper καταλαβαίνει αυτόματα τη γλώσσα του ήχου!
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=uploaded_file
                )
                
                text_result = transcript.text
                
                # ΒΗΜΑ B: Δημιουργία Περίληψης και To-Do με LLM
                # Ζητάμε από το AI να απαντήσει στη γλώσσα που έγινε η κλήση
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

                # Εμφάνιση αποτελεσμάτων στην οθόνη
                str.success("Η ανάλυση ολοκληρώθηκε!")
                
                str.subheader("📝 Σύνοψη & Εκκρεμότητες (AI Summary)")
                str.write(ai_summary)
                
                with str.expander("Δείτε όλο το γραπτό κείμενο της κλήσης (Full Transcript)"):
                    str.write(text_result)
                    
            except Exception as e:
                str.error(f"Προέκυψε σφάλμα: {e}")
