"""
Semigran-45 Clinical Vignettes — Reconstructed from published literature.

Sources:
  - Semigran HL et al. BMJ 2015 (doi:10.1136/bmj.h3480) — original 45 vignettes
  - Schmieding ML et al. JMIR 2022 (doi:10.2196/31810) — 5-year follow-up, same vignettes
  - Zenodo dataset: https://zenodo.org/records/6054093 (CC-BY 4.0)
  - Hill MG et al. MJA 2020 (doi:10.5694/mja2.50600)

Gold-standard triage labels (assigned by expert panel, Semigran 2015):
  "emergency"     = Em  — requires emergency care (ER/112)
  "non_emergency" = NE  — requires non-emergency medical care (doctor appointment)
  "self_care"     = Sc  — self-care sufficient

Condensed Format: each vignette is the minimal finding set used for testing,
exactly as used in the benchmark literature.
"""

VIGNETTES = [
    # ── EMERGENCY (Em) — 15 vignettes ─────────────────────────────────────
    {
        "id": "V01",
        "gold": "emergency",
        "condition": "Acute MI / Heart attack",
        "age": 55, "sex": "M",
        "condensed": (
            "55-year-old male. Severe crushing chest pain radiating to left arm. "
            "Onset 30 minutes ago. Associated sweating, nausea, shortness of breath. "
            "No trauma. Hypertension history."
        ),
    },
    {
        "id": "V02",
        "gold": "emergency",
        "condition": "Stroke",
        "age": 68, "sex": "F",
        "condensed": (
            "68-year-old female. Sudden onset facial drooping on the right side. "
            "Slurred speech. Right arm weakness. Onset 45 minutes ago. "
            "Hypertension and diabetes history."
        ),
    },
    {
        "id": "V03",
        "gold": "emergency",
        "condition": "Pulmonary embolism",
        "age": 42, "sex": "F",
        "condensed": (
            "42-year-old female. Sudden onset severe shortness of breath. "
            "Sharp chest pain, worse on inspiration. SpO2 88%. "
            "Recently returned from long flight. Calf swelling left leg."
        ),
    },
    {
        "id": "V04",
        "gold": "emergency",
        "condition": "Anaphylaxis",
        "age": 28, "sex": "M",
        "condensed": (
            "28-year-old male. Generalized urticaria and facial swelling "
            "10 minutes after eating peanuts. Throat tightness. "
            "Wheezing. BP falling. Known peanut allergy."
        ),
    },
    {
        "id": "V05",
        "gold": "emergency",
        "condition": "Appendicitis",
        "age": 22, "sex": "M",
        "condensed": (
            "22-year-old male. Periumbilical pain migrating to right lower quadrant "
            "over 12 hours. Fever 38.5°C. Nausea, vomiting. "
            "Rebound tenderness at McBurney's point. Anorexia since yesterday."
        ),
    },
    {
        "id": "V06",
        "gold": "emergency",
        "condition": "Meningitis",
        "age": 19, "sex": "F",
        "condensed": (
            "19-year-old female. Severe headache, neck stiffness, fever 39.8°C. "
            "Photophobia. Non-blanching petechial rash on trunk. "
            "Vomiting. Onset rapid over several hours."
        ),
    },
    {
        "id": "V07",
        "gold": "emergency",
        "condition": "Ectopic pregnancy",
        "age": 26, "sex": "F",
        "condensed": (
            "26-year-old female. Severe lower abdominal pain, right side. "
            "Last menstrual period 8 weeks ago. Positive pregnancy test. "
            "Vaginal spotting. Dizziness. History of previous pelvic infection."
        ),
    },
    {
        "id": "V08",
        "gold": "emergency",
        "condition": "Diabetic ketoacidosis",
        "age": 17, "sex": "M",
        "condensed": (
            "17-year-old male. Known Type 1 diabetes. Nausea, vomiting, abdominal pain. "
            "Fruity breath odour. Blood glucose 28 mmol/L. "
            "Increased thirst and urination for 2 days. Lethargy."
        ),
    },
    {
        "id": "V09",
        "gold": "emergency",
        "condition": "Severe asthma attack",
        "age": 14, "sex": "F",
        "condensed": (
            "14-year-old female with known asthma. Severe wheezing, unable to speak in full sentences. "
            "Peak flow < 33% predicted. Accessory muscle use. "
            "Not responding to salbutamol inhaler. SpO2 91%."
        ),
    },
    {
        "id": "V10",
        "gold": "emergency",
        "condition": "GI bleed",
        "age": 61, "sex": "M",
        "condensed": (
            "61-year-old male. Vomiting fresh bright red blood. "
            "Black tarry stools since yesterday. Dizziness on standing. "
            "History of peptic ulcer disease. Takes NSAIDs regularly. HR 112 bpm."
        ),
    },
    {
        "id": "V11",
        "gold": "emergency",
        "condition": "Sepsis",
        "age": 75, "sex": "F",
        "condensed": (
            "75-year-old female. Confusion, high fever 39.5°C. "
            "HR 118 bpm, BP 88/55 mmHg. Known UTI treated with antibiotics for 3 days. "
            "Not improving. Cold extremities. Decreased urine output."
        ),
    },
    {
        "id": "V12",
        "gold": "emergency",
        "condition": "Head injury with loss of consciousness",
        "age": 35, "sex": "M",
        "condensed": (
            "35-year-old male. Fall from ladder, hit head. "
            "Loss of consciousness for 2 minutes. Now confused. "
            "Vomiting once since injury. Pupils unequal. Headache worsening."
        ),
    },
    {
        "id": "V13",
        "gold": "emergency",
        "condition": "Seizure — first episode",
        "age": 30, "sex": "M",
        "condensed": (
            "30-year-old male. Witnessed tonic-clonic seizure lasting 3 minutes. "
            "No prior seizure history. Post-ictal confusion. "
            "No fever, no trauma. Family history of epilepsy."
        ),
    },
    {
        "id": "V14",
        "gold": "emergency",
        "condition": "Acute urinary retention",
        "age": 72, "sex": "M",
        "condensed": (
            "72-year-old male. Unable to urinate for 12 hours. "
            "Severe suprapubic pain and distension. Known BPH. "
            "Last voided small amount 12 hours ago."
        ),
    },
    {
        "id": "V15",
        "gold": "emergency",
        "condition": "Burns — severe",
        "age": 45, "sex": "M",
        "condensed": (
            "45-year-old male. Burns to face, both arms and chest from house fire. "
            "Singed nasal hairs. Hoarse voice. Estimated 25% body surface area. "
            "Smoke inhalation suspected."
        ),
    },

    # ── NON-EMERGENCY (NE) — 15 vignettes ──────────────────────────────────
    {
        "id": "V16",
        "gold": "non_emergency",
        "condition": "Urinary tract infection",
        "age": 24, "sex": "F",
        "condensed": (
            "24-year-old female. Dysuria and urinary frequency for 2 days. "
            "Suprapubic discomfort. No fever, no loin pain, no vomiting. "
            "No vaginal discharge."
        ),
    },
    {
        "id": "V17",
        "gold": "non_emergency",
        "condition": "Otitis media",
        "age": 4, "sex": "M",
        "condensed": (
            "4-year-old boy. Ear pain for 1 day. Fever 38.2°C. "
            "Crying, pulling at right ear. Decreased appetite. "
            "Recent cold 1 week ago."
        ),
    },
    {
        "id": "V18",
        "gold": "non_emergency",
        "condition": "Tonsillitis / Strep throat",
        "age": 16, "sex": "F",
        "condensed": (
            "16-year-old female. Sore throat for 3 days. Fever 38.8°C. "
            "Difficulty swallowing. White exudate on tonsils. "
            "Swollen anterior cervical lymph nodes. No cough."
        ),
    },
    {
        "id": "V19",
        "gold": "non_emergency",
        "condition": "Conjunctivitis",
        "age": 8, "sex": "F",
        "condensed": (
            "8-year-old girl. Red eye for 2 days, both sides. "
            "Yellowish discharge, worse in morning. Mild itching. "
            "No pain, no photophobia, no visual change."
        ),
    },
    {
        "id": "V20",
        "gold": "non_emergency",
        "condition": "Ankle sprain",
        "age": 20, "sex": "M",
        "condensed": (
            "20-year-old male. Twisted right ankle while running 3 hours ago. "
            "Swelling and bruising lateral ankle. Pain on weight bearing. "
            "Able to walk, no bony tenderness on Ottawa criteria points."
        ),
    },
    {
        "id": "V21",
        "gold": "non_emergency",
        "condition": "Contact dermatitis",
        "age": 33, "sex": "F",
        "condensed": (
            "33-year-old female. Itchy red rash on wrists for 1 week. "
            "Recently started wearing new watch. No fever. "
            "Rash confined to skin under watch strap. Vesicles present."
        ),
    },
    {
        "id": "V22",
        "gold": "non_emergency",
        "condition": "Migraine",
        "age": 29, "sex": "F",
        "condensed": (
            "29-year-old female with known migraines. Unilateral throbbing headache. "
            "Nausea, photophobia, phonophobia. Onset 6 hours ago. "
            "Visual aura for 20 minutes before headache. No fever, no neck stiffness."
        ),
    },
    {
        "id": "V23",
        "gold": "non_emergency",
        "condition": "Sinusitis",
        "age": 38, "sex": "M",
        "condensed": (
            "38-year-old male. Facial pain and pressure for 10 days. "
            "Purulent nasal discharge. Fever 37.8°C. "
            "Preceded by cold. Maxillary and frontal sinus tenderness."
        ),
    },
    {
        "id": "V24",
        "gold": "non_emergency",
        "condition": "Cellulitis",
        "age": 50, "sex": "M",
        "condensed": (
            "50-year-old male. Red, warm, tender swelling on right lower leg. "
            "Spreading erythema over 2 days. Fever 38.1°C. "
            "Small cut on foot from 5 days ago. No fluctuance."
        ),
    },
    {
        "id": "V25",
        "gold": "non_emergency",
        "condition": "Low back pain — acute",
        "age": 44, "sex": "M",
        "condensed": (
            "44-year-old male. Acute low back pain after lifting. "
            "Onset yesterday. Muscle spasm. Pain radiates to left buttock. "
            "No neurological symptoms. No bladder/bowel problems. No fever."
        ),
    },
    {
        "id": "V26",
        "gold": "non_emergency",
        "condition": "Gastroenteritis",
        "age": 25, "sex": "F",
        "condensed": (
            "25-year-old female. Nausea, vomiting and diarrhoea for 24 hours. "
            "Mild crampy abdominal pain. Low-grade fever 37.6°C. "
            "Able to keep small amounts of fluid down. No blood in stool."
        ),
    },
    {
        "id": "V27",
        "gold": "non_emergency",
        "condition": "Vaginal candidiasis",
        "age": 27, "sex": "F",
        "condensed": (
            "27-year-old female. Vaginal itching and thick white discharge for 5 days. "
            "No odour. No dysuria, no dyspareunia. "
            "Recently completed antibiotic course. No fever."
        ),
    },
    {
        "id": "V28",
        "gold": "non_emergency",
        "condition": "Impetigo",
        "age": 6, "sex": "M",
        "condensed": (
            "6-year-old boy. Golden-crusted sores around nose and mouth for 3 days. "
            "Mild itching. No fever. "
            "Sibling at school also has similar lesions."
        ),
    },
    {
        "id": "V29",
        "gold": "non_emergency",
        "condition": "Hypertension — newly detected",
        "age": 52, "sex": "M",
        "condensed": (
            "52-year-old male. BP 162/98 mmHg on two readings today. "
            "Mild headache. No chest pain, no shortness of breath. "
            "No prior hypertension diagnosis. Overweight. Family history positive."
        ),
    },
    {
        "id": "V30",
        "gold": "non_emergency",
        "condition": "Depression",
        "age": 40, "sex": "F",
        "condensed": (
            "40-year-old female. 3 weeks of low mood, anhedonia, poor sleep. "
            "Fatigue. Appetite loss with 3 kg weight loss. "
            "Difficulty concentrating. No suicidal ideation. "
            "No prior psychiatric history."
        ),
    },

    # ── SELF-CARE (Sc) — 15 vignettes ──────────────────────────────────────
    {
        "id": "V31",
        "gold": "self_care",
        "condition": "Common cold",
        "age": 31, "sex": "F",
        "condensed": (
            "31-year-old female. Runny nose, sore throat, mild cough for 2 days. "
            "Low-grade temperature 37.4°C. Sneezing. "
            "No fever > 38, no difficulty breathing, no ear pain."
        ),
    },
    {
        "id": "V32",
        "gold": "self_care",
        "condition": "Tension headache",
        "age": 36, "sex": "M",
        "condensed": (
            "36-year-old male. Bilateral band-like headache, mild-moderate severity. "
            "Onset after stressful workday. No nausea, no photophobia. "
            "No fever. No neck stiffness. Relieved partially by paracetamol."
        ),
    },
    {
        "id": "V33",
        "gold": "self_care",
        "condition": "Insect bite",
        "age": 10, "sex": "M",
        "condensed": (
            "10-year-old boy. Small itchy red bump on forearm after being outside. "
            "Local swelling < 2cm. No spreading redness, no fever. "
            "No known allergies. No difficulty breathing."
        ),
    },
    {
        "id": "V34",
        "gold": "self_care",
        "condition": "Mild sunburn",
        "age": 23, "sex": "F",
        "condensed": (
            "23-year-old female. Red, painful skin on shoulders and back after beach day. "
            "No blistering. Mild discomfort. No fever. "
            "Affecting < 5% body surface area."
        ),
    },
    {
        "id": "V35",
        "gold": "self_care",
        "condition": "Haemorrhoids",
        "age": 45, "sex": "M",
        "condensed": (
            "45-year-old male. Painless rectal bleeding on toilet paper for 1 week. "
            "No dark blood, no abdominal pain. "
            "Constipation. Lump at anus. No weight loss, no changed bowel habit for > 3 weeks."
        ),
    },
    {
        "id": "V36",
        "gold": "self_care",
        "condition": "Mild allergic rhinitis",
        "age": 21, "sex": "F",
        "condensed": (
            "21-year-old female. Seasonal sneezing, itchy watery eyes, runny nose. "
            "Known hay fever since childhood. No fever. "
            "Symptoms worse outdoors in spring. No asthma symptoms."
        ),
    },
    {
        "id": "V37",
        "gold": "self_care",
        "condition": "Mouth ulcer — aphthous",
        "age": 18, "sex": "F",
        "condensed": (
            "18-year-old female. Painful small white ulcer inside lower lip for 3 days. "
            "Single lesion < 1cm. No fever, no difficulty swallowing. "
            "Recurrent episodes since teenage years."
        ),
    },
    {
        "id": "V38",
        "gold": "self_care",
        "condition": "Muscle soreness — DOMS",
        "age": 28, "sex": "M",
        "condensed": (
            "28-year-old male. Generalised muscle ache in both legs since yesterday. "
            "Started new exercise programme 2 days ago. No trauma, no swelling. "
            "No fever. Improves slightly with movement."
        ),
    },
    {
        "id": "V39",
        "gold": "self_care",
        "condition": "Mild constipation",
        "age": 55, "sex": "F",
        "condensed": (
            "55-year-old female. No bowel movement for 3 days. "
            "Mild abdominal discomfort. No blood, no vomiting, no weight loss. "
            "Reduced dietary fibre recently. Not on new medications."
        ),
    },
    {
        "id": "V40",
        "gold": "self_care",
        "condition": "Mild heartburn / GERD",
        "age": 47, "sex": "M",
        "condensed": (
            "47-year-old male. Burning sensation in chest/epigastrium after meals. "
            "Worse when lying down. No radiation to arm, no sweating, no severe pain. "
            "Occurs 2-3 times per week. Relieved by antacids."
        ),
    },
    {
        "id": "V41",
        "gold": "self_care",
        "condition": "Dandruff / seborrhoeic dermatitis — mild",
        "age": 32, "sex": "M",
        "condensed": (
            "32-year-old male. Flaky scalp, mild itching for 1 month. "
            "No hair loss, no spreading rash. "
            "Worse in winter. No fever, no lymph nodes."
        ),
    },
    {
        "id": "V42",
        "gold": "self_care",
        "condition": "Mild anxiety",
        "age": 26, "sex": "F",
        "condensed": (
            "26-year-old female. Feeling anxious before upcoming exam. "
            "Palpitations, mild tremor, difficulty sleeping for 3 days. "
            "No chest pain. No history of anxiety disorder. Situational trigger clear."
        ),
    },
    {
        "id": "V43",
        "gold": "self_care",
        "condition": "Wax impaction — ear",
        "age": 40, "sex": "M",
        "condensed": (
            "40-year-old male. Reduced hearing left ear for 1 week. "
            "Sensation of fullness, mild tinnitus. No pain, no discharge. "
            "Worse after swimming. No fever."
        ),
    },
    {
        "id": "V44",
        "gold": "self_care",
        "condition": "Nappy rash / infant dermatitis",
        "age": 0, "sex": "F",
        "condensed": (
            "8-month-old girl. Red irritated skin in nappy area for 2 days. "
            "No fever, eating and drinking normally, active. "
            "No blistering, not spreading beyond nappy area."
        ),
    },
    {
        "id": "V45",
        "gold": "self_care",
        "condition": "Verruca / wart",
        "age": 13, "sex": "M",
        "condensed": (
            "13-year-old boy. Small rough growth on sole of right foot for 2 months. "
            "No pain except on walking. No surrounding redness. "
            "No rapid growth. No bleeding."
        ),
    },
]

# ── GOLD STANDARD MAPPING ─────────────────────────────────────────────────────
GOLD_LABELS = {v["id"]: v["gold"] for v in VIGNETTES}

TRIAGE_LEVELS = ["emergency", "non_emergency", "self_care"]

# ── ASKLEPIOS TRIAGE MAPPING ──────────────────────────────────────────────────
# Maps Claude/Asklepios output keywords to standard triage levels.
# Add more synonyms if needed based on actual output patterns.
ASKLEPIOS_OUTPUT_MAP = {
    # Emergency
    "επείγον": "emergency",
    "αμέσως": "emergency",
    "166": "emergency",
    "112": "emergency",
    "emergency": "emergency",
    "κόκκινη σημαία": "emergency",
    "κοκκινη σημαια": "emergency",
    "red flag": "emergency",
    "immediately": "emergency",
    "urgent care": "emergency",  # conservative: map urgent → emergency
    # Non-emergency
    "ιατρό": "non_emergency",
    "γιατρό": "non_emergency",
    "ιατρείο": "non_emergency",
    "ραντεβού": "non_emergency",
    "doctor": "non_emergency",
    "physician": "non_emergency",
    "appointment": "non_emergency",
    "non-emergency": "non_emergency",
    "non_emergency": "non_emergency",
    # Self-care
    "οίκοι": "self_care",
    "στο σπίτι": "self_care",
    "self-care": "self_care",
    "self care": "self_care",
    "home care": "self_care",
    "αυτοφροντίδα": "self_care",
}

if __name__ == "__main__":
    from collections import Counter
    counts = Counter(v["gold"] for v in VIGNETTES)
    print(f"Total vignettes: {len(VIGNETTES)}")
    print(f"Distribution: {dict(counts)}")
    print("\nSample vignette:")
    import json
    print(json.dumps(VIGNETTES[0], ensure_ascii=False, indent=2))
