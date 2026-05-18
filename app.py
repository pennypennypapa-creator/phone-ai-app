import streamlit as str
from openai import OpenAI

# 1. Ασφαλής ανάγνωση του API Key από τα Secrets του Streamlit Cloud
client = OpenAI(api_key=str.secrets["OPENAI_API_KEY"])

str.title("🎙️ Global AI Phone Note Taker")
str.write("Ανεβάστε την ηχογράφηση της κλήσης σας (σε οποιαδήποτε γλώσσα).")

# 2. Στοιχείο για ανέβασμα αρχείου ήχου
uploaded_file = str.file_uploader("Επιλέξτε αρχείο ήχου...", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    # Ξεκινάει αυτόματα η ανάλυση μόλις μπει το αρχείο
    with str.spinner("🤖 Το AI επεξεργάζεται την κλήση σας live..."):
        try:
            # ΒΗΜΑ A: Μετατροπή ομιλίας σε κείμενο (Speech-to-Text)
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=uploaded_file
            )
            
            text_result = transcript.text
            
            # ΒΗΜΑ B: Δημιουργία Περίληψης και To-Do με LLM
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
            
            # Διορθώθηκε: Προστέθηκε το [0] που έλειπε στο πρώτο κομμάτι του κώδικά σας
            ai_summary = response.choices[0].message.content

            # Εμφάνιση αποτελεσμάτων στην οθόνη
            str.success("Η ανάλυση ολοκληρώθηκε!")
            
            str.subheader("📝 Σύνοψη & Εκκρεμότητες (AI Summary)")
            str.write(ai_summary)
            
            with str.expander("Δείτε όλο το γραπτό κείμενο της κλήσης (Full Transcript)"):
                str.write(text_result)
                
        except Exception as e:
            str.error(f"Προέκυψε σφάλμα: {e}")

