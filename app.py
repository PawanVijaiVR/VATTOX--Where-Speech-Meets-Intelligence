import os
import json
import unicodedata
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Optional: set OPENAI_API_KEY in your environment to enable live AI responses.
# No secret key is stored in this project.
API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

# Verified Saurashtra word list collected from the user's supplied reference screenshots.
# These entries are kept as a reference phrasebook for the app and are presented as
# dictionary-style entries rather than as unverified AI-generated content.
VERIFIED_PHRASES = [
    {"topic": "Saurashtra dictionary", "saurashtra": "pollo", "english": "fruit", "tamil": "பழம்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "mottappan", "english": "leadership", "tamil": "மூத்த பதவி", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "betki", "english": "female", "tamil": "பெண்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "ambat", "english": "sour", "tamil": "புளிப்பு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "foljat", "english": "after", "tamil": "பின்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "kaam", "english": "job", "tamil": "வேலை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "bhonno", "english": "pot", "tamil": "குடம்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "lubhim", "english": "gooseberry pickles", "tamil": "நெல்லிக்காய் ஊறுகாய்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "tinvo", "english": "third", "tamil": "மூன்றாவது", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "nadini", "english": "granddaughter", "tamil": "பேத்தி", "verified": True, "note": "Reference dictionary entry"},
  
    {"topic": "Saurashtra dictionary", "saurashtra": "dado", "english": "elder brother", "tamil": "மூத்த சகோதரன்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "tham", "english": "place", "tamil": "இடம்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "stiti", "english": "status", "tamil": "நிலை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "dracca pollo", "english": "grapes", "tamil": "திராட்சை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "catuqeri", "english": "suddenly", "tamil": "திடீரென", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "bedko", "english": "son", "tamil": "மகன்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "qappo", "english": "drum", "tamil": "முழவு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "kadale", "english": "ground nut", "tamil": "வேர்க்கடலை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "chullo", "english": "oven", "tamil": "சுடுகல்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "bench", "english": "bench", "tamil": "palagai", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "d3end3am", "english": "holy thread", "tamil": "புனித நூல்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "bad3d3i", "english": "greens", "tamil": "பச்சை காய்கறிகள்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "chelmo", "english": "river spring", "tamil": "ஆற்றின் மூலநீர்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "janni", "english": "broom stick", "tamil": "தூசு தட்டி குச்சி", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "kavaad", "english": "door", "tamil": "கதவு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "chokkaai", "english": "shirt", "tamil": "ஷர்ட்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "chinta", "english": "anklet", "tamil": "காலணிக் காப்பு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "angili", "english": "finger", "tamil": "கை விரல்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "haed", "english": "take", "tamil": "எடு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "vinkhar", "english": "weaver", "tamil": "தறி செய்பவர்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "ghadi", "english": "throat", "tamil": "தொண்டை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "reak kaad", "english": "make to write", "tamil": "எழுதச் செய்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "pillo", "english": "child", "tamil": "குழந்தை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "poja", "english": "worship", "tamil": "பூஜை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "pi:t", "english": "wall", "tamil": "சுவர்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "phille", "english": "to wear", "tamil": "அணிய", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "solophar", "english": "morning", "tamil": "மதியம்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "bhoundi", "english": "daughter-in-law", "tamil": "மகள் மருமகள்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "tandu", "english": "rice", "tamil": "அரிசி", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "dekki", "english": "to meet", "tamil": "சந்திக்க", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "stidi", "english": "status", "tamil": "நிலை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "dhaqqe", "english": "send", "tamil": "அனுப்பு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "catukeri", "english": "suddenly", "tamil": "திடீரென", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "dunqum", "english": "drum", "tamil": "முழவு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "kaqale tel", "english": "ground nut oil", "tamil": "வேர்க்கடலை எண்ணெய்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "cumbi", "english": "pinch", "tamil": "சின்ன மடிப்பு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "benc", "english": "bench", "tamil": "பெஞ்ச்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "kud3al", "english": "white", "tamil": "வெள்ளை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "chenno", "english": "parched Bengal grain seasoned with tumeri", "tamil": "துமரி சேர்த்து பதப்படுத்திய வங்காள அரிசி", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "d3agatte", "english": "conceal", "tamil": "மறை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "kaccamba pollo", "english": "mango", "tamil": "மாம்பழம்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "gaaldee", "english": "scold", "tamil": "கடிந்து பேசு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "gullejar", "english": "jaggery", "tamil": "வெல்லம்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "gul lu pongal", "english": "sugar rice", "tamil": "சர்க்கரை அரிசி", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "kho[ti", "english": "bag", "tamil": "பை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "ghoqo", "english": "horse", "tamil": "குதிரை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "paqi", "english": "yarn", "tamil": "சணல் நூல்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "pa:jmpo:t", "english": "worship", "tamil": "வழிபாடு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "pa[ar", "english": "wantonly", "tamil": "மோசமாக", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "kobbo", "english": "when", "tamil": "எப்போது", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "phonni", "english": "comb", "tamil": "சீப்பு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "a.fis", "english": "office", "tamil": "அலுவலகம்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "tinvi:s", "english": "sixty", "tamil": "அறுபது", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "nattini", "english": "granddaughter", "tamil": "பேத்தி", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "divajo", "english": "second", "tamil": "இரண்டாவது", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "thandu", "english": "rice", "tamil": "அரிசி", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "sthiram", "english": "stable", "tamil": "நிலையான", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "udhar", "english": "loan", "tamil": "கடன்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "bot tu", "english": "mangalasutra", "tamil": "மாங்கல்யம்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "tun du", "english": "towel", "tamil": "துண்டு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "cum[tti", "english": "transcription illegible", "tamil": "எழுத்துப்பதிவு புரியவில்லை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "jomayi", "english": "son-in-law", "tamil": "மருமகன்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "bod3d3ak", "english": "jealousy", "tamil": "பொறாமை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "d3aqani", "english": "husband's elder brother's wife", "tamil": "கணவனின் மூத்த சகோதரியின் மனைவி", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "kavaad", "english": "door", "tamil": "கதவு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "cekki", "english": "to cut", "tamil": "வெட்டு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "gulle", "english": "sweeter", "tamil": "இனிப்பு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "kokoo", "english": "cock", "tamil": "கோழி", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "kad3d3u", "english": "sore, ulcer", "tamil": "புண், காயம்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "couli", "english": "jacket", "tamil": "ஜாக்கெட்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "d3eqbulo", "english": "head ornament", "tamil": "தலை அலங்காரம்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "chelladam", "english": "underwear", "tamil": "உடை உள்துறை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "d3eqani", "english": "brother", "tamil": "சகோதரன்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "ogur", "english": "bitter gourd", "tamil": "பாகல்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "vikku", "english": "poison", "tamil": "விஷம்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "khandur", "english": "shoulder", "tamil": "தொடை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "guddi", "english": "blow", "tamil": "அடி", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "saŋgi", "english": "to say", "tamil": "சொல்லு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "khoulo", "english": "niche", "tamil": "குழி", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "khalotho jaman ", "english": "toy", "tamil": "சொந்த விளையாட்டு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "tappat", "english": "boil", "tamil": "காய்ச்சல்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "botto", "english": "cloth", "tamil": "துணி", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "hibbat", "english": "stop", "tamil": "நிறுத்து", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "phonis pollo", "english": "jackfruit", "tamil": "பலாப்பழம்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "dobbi", "english": "push", "tamil": "தள்ளு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "tukki", "english": "carry, lift", "tamil": "சுமந்து செல்லு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "natte", "english": "grand son", "tamil": "பேரன்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "dallo", "english": "husband", "tamil": "கணவர்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "theki", "english": "obstruct", "tamil": "தடுத்து நிறுத்து", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "dhumpan", "english": "tobacco", "tamil": "புகையிலை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "att:ale", "english": "shelf", "tamil": "அலமாரி", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "kuqi", "english": "hen", "tamil": "முட்டை இடும் கோழி", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "kokkai", "english": "shirt", "tamil": "ஷர்ட்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "vincu", "english": "scorpion", "tamil": "மகரந்தம்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "d3eket", "english": "sift, sieve", "tamil": "கூடுதல்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "kad3al", "english": "syetex (illegible)", "tamil": "அறியப்படாத", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "chekkur", "english": "wheel", "tamil": "சக்கரம்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "d3ago", "english": "close", "tamil": "மூடு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "konqo", "english": "bran", "tamil": "தானிய சீப்பை", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "nekku", "english": "nail", "tamil": "கூம்பு நகம்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "gonam", "english": "skirt", "tamil": "கைநெசவு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "vangi", "english": "brinjal (illegible)", "tamil": "பிரிஞ்சல்", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "khalle", "english": "take", "tamil": "எடு", "verified": True, "note": "Reference dictionary entry"},
    {"topic": "Saurashtra dictionary", "saurashtra": "ghelo", "english": "neck", "tamil": "கழுத்து", "verified": True, "note": "Reference dictionary entry"}
]

# Hindi aliases bridge common dictionary meanings to the Saurashtra entries supplied
# by the user. Hindi wording is a convenience index, not a separately verified source.
HINDI_ALIASES = {
    "फल": "fruit",
    "नेतृत्व": "leadership",
    "महिला": "female",
    "खट्टा": "sour",
    "बाद": "after",
    "कार्यालय": "office",
    "बर्तन": "pot",
    "आंवले का अचार": "gooseberry pickles",
    "तीसरा": "third",
    "पोती": "granddaughter",
    "देवर": "husband's younger brother",
    "बड़ा भाई": "elder brother",
    "स्थान": "place",
    "स्थिति": "status",
    "अंगूर": "grapes",
    "अचानक": "suddenly",
    "बेटा": "son",
    "ढोल": "drum",
    "मूंगफली": "ground nut",
    "ओवन": "oven",
    "बेंच": "bench",
    "पवित्र धागा": "holy thread",
    "साग": "greens",
    "झरना": "river spring",
    "झाड़ू": "broom stick",
    "दरवाज़ा": "door",
    "दरवाजा": "door",
    "कमीज़": "shirt",
    "पायल": "anklet",
    "उंगली": "finger",
    "लेना": "take",
    "बुनकर": "weaver",
    "गला": "throat",
    "बच्चा": "child",
    "पूजा": "worship",
    "दीवार": "wall",
    "पहनना": "to wear",
    "सुबह": "morning",
    "बहू": "daughter-in-law",
    "चावल": "rice",
    "मिलना": "to meet",
    "भेजना": "send",
    "मूंगफली का तेल": "ground nut oil",
    "सफेद": "white",
    "आम": "mango",
    "डांटना": "scold",
    "गुड़": "jaggery",
    "घोड़ा": "horse",
    "धागा": "yarn",
    "कब": "when",
    "कंघी": "comb",
    "साठ": "sixty",
    "दूसरा": "second",
    "स्थिर": "stable",
    "ऋण": "loan",
    "तौलिया": "towel",
    "दामाद": "son-in-law",
    "ईर्ष्या": "jealousy",
    "काटना": "to cut",
    "मुर्गा": "cock",
    "जैकेट": "jacket",
    "ज़हर": "poison",
    "जहर": "poison",
    "कंधा": "shoulder",
    "कहना": "to say",
    "खिलौना": "toy",
    "उबालना": "boil",
    "कपड़ा": "cloth",
    "रुकना": "stop",
    "कटहल": "jackfruit",
    "धक्का": "push",
    "पोता": "grand son",
    "पति": "husband",
    "तंबाकू": "tobacco",
    "मुर्गी": "hen",
    "बिच्छू": "scorpion",
    "छानना": "sift, sieve",
    "पहिया": "wheel",
    "बंद करना": "close",
    "चोकर": "bran",
    "कील": "nail",
    "नाखून": "nail",
    "स्कर्ट": "skirt",
    "बैंगन": "brinjal (illegible)",
    "गर्दन": "neck",
}

TAMIL_ALIASES = {
    "பழம்": "fruit",
    "பெண்": "female",
    "புளிப்பு": "sour",
    "அலுவலகம்": "office",
    "குடம்": "pot",
    "நெல்லிக்காய் ஊறுகாய்": "gooseberry pickles",
    "பேத்தி": "granddaughter",
    "மூத்த சகோதரன்": "elder brother",
    "இடம்": "place",
    "நிலை": "status",
    "திராட்சை": "grapes",
    "திடீரென": "suddenly",
    "மகன்": "son",
    "முரசு": "drum",
    "வேர்க்கடலை": "ground nut",
    "அடுப்பு": "oven",
    "பெஞ்ச்": "bench",
    "பூணூல்": "holy thread",
    "கீரைகள்": "greens",
    "ஊற்று": "river spring",
    "விளக்குமாறு": "broom stick",
    "கதவு": "door",
    "சட்டை": "shirt",
    "கொலுசு": "anklet",
    "விரல்": "finger",
    "எடு": "take",
    "நெசவாளர்": "weaver",
    "தொண்டை": "throat",
    "குழந்தை": "child",
    "வழிபாடு": "worship",
    "சுவர்": "wall",
    "அணி": "to wear",
    "காலை": "morning",
    "மருமகள்": "daughter-in-law",
    "அரிசி": "rice",
    "சந்திக்க": "to meet",
    "அனுப்பு": "send",
    "வேர்க்கடலை எண்ணெய்": "ground nut oil",
    "வெள்ளை": "white",
    "மாம்பழம்": "mango",
    "திட்டு": "scold",
    "வெல்லம்": "jaggery",
    "குதிரை": "horse",
    "நூல்": "yarn",
    "எப்போது": "when",
    "சீப்பு": "comb",
    "அறுபது": "sixty",
    "இரண்டாவது": "second",
    "நிலையான": "stable",
    "கடன்": "loan",
    "துண்டு": "towel",
    "மருமகன்": "son-in-law",
    "பொறாமை": "jealousy",
    "வெட்டு": "to cut",
    "சேவல்": "cock",
    "ஜாக்கெட்": "jacket",
    "நஞ்சு": "poison",
    "தோள்பட்டை": "shoulder",
    "சொல்": "to say",
    "பொம்மை": "toy",
    "கொதிக்க": "boil",
    "துணி": "cloth",
    "நிறுத்து": "stop",
    "பலாப்பழம்": "jackfruit",
    "தள்ளு": "push",
    "தூக்கு": "carry, lift",
    "பேரன்": "grand son",
    "கணவர்": "husband",
    "தடை": "obstruct",
    "புகையிலை": "tobacco",
    "கோழி": "hen",
    "தேள்": "scorpion",
    "சலிக்க": "sift, sieve",
    "சக்கரம்": "wheel",
    "மூடு": "close",
    "தவிடு": "bran",
    "ஆணி": "nail",
    "பாவாடை": "skirt",
    "கத்திரிக்காய்": "brinjal (illegible)",
    "கழுத்து": "neck",
}


def normalize_lookup_text(value):
    normalized = unicodedata.normalize("NFC", value).casefold().strip()
    return " ".join(normalized.split())


# These entries come from the user's reference images and have not been independently
# reviewed by a fluent speaker, so expose them as references rather than verified entries.
SOURASTRA_LOOKUP = {}
for entry in VERIFIED_PHRASES:
    entry["verified"] = False
    entry["note"] = "User-provided reference; fluent-speaker review pending"
    key = normalize_lookup_text(entry.get("saurashtra") or "")
    if key:
        SOURASTRA_LOOKUP[key] = entry

SYSTEM_PROMPT = """You are VathoX AI Companion, a friendly language-practice assistant.
The main language being taught is Saurashtra. English and Tamil may be used to explain
meanings and instructions, but they are not the learning target when the user chooses
Saurashtra practice.

Important accuracy rules:
- Do not invent Saurashtra vocabulary, grammar, spelling, transliteration, or pronunciation
  and claim it is correct.
- When asked for a direct Saurashtra translation or a word's Saurashtra equivalent, reply
  with only the Saurashtra word or phrase. Do not add labels, meanings, definitions,
  equals signs, or explanatory text unless the user asks for them.
- If a Saurashtra expression is not available in the reference word list or the user has
  not supplied it, clearly say that it needs verification by a fluent Saurashtra speaker.
- In conversation practice, the user wants Saurashtra output followed by an explanation in
  their selected language. Any sentence you compose is an experimental draft, not verified
  Saurashtra grammar. Label it clearly as an unverified draft and never present it as
  authoritative. Use supplied reference vocabulary where possible and explain uncertainty.
  When asked to practise a sentence pattern, try to provide one short Latin-transliterated
  draft using the selected reference word; if you cannot do so responsibly, say it needs
  fluent-speaker review rather than inventing a supposedly correct form.
- You may help with learning plans, conversation scenarios, practice structure, and
  explanations in English/Tamil without fabricating Saurashtra translations.
- Keep answers supportive, simple, and suitable for a beginner.
- Ask one clear follow-up question when useful.
- Do not claim to hear audio or know the user's pronunciation unless an audio assessment
  feature is actually connected.
"""


def lookup_word(query, source_language=None):
    if not query:
        return None
    raw = normalize_lookup_text(query)
    if not raw:
        return None
    match = SOURASTRA_LOOKUP.get(raw)
    if match:
        return match

    language = (source_language or "").strip().lower()
    if language in ("hindi", "tamil"):
        aliases = HINDI_ALIASES if language == "hindi" else TAMIL_ALIASES
        english_meaning = aliases.get(raw)
        if not english_meaning:
            return None
        raw = normalize_lookup_text(english_meaning)

    for entry in VERIFIED_PHRASES:
        fields = ("english",) if language else ("english", "tamil")
        for field in fields:
            value = normalize_lookup_text(entry.get(field) or "")
            candidates = [normalize_lookup_text(part) for part in value.split(",")]
            candidates.extend(candidate[3:] for candidate in tuple(candidates) if candidate.startswith("to "))
            if raw == value or raw in candidates:
                return entry
    return None

def local_demo_reply(message, target_language, mode, source_language="English", practice=None):
    msg = message.lower().strip()
    if mode == "conversation" and isinstance(practice, dict):
        entry = lookup_word(str(practice.get("saurashtra") or ""))
        if entry:
            meaning = entry.get("tamil") if target_language == "Tamil" else entry.get("english")
            return (
                f"Saurashtra reference word: {entry['saurashtra']}\n"
                f"{target_language} meaning: {meaning}\n"
                "Sentence draft: Sentence generation needs live AI and fluent-speaker review. "
                "This demo uses the reference word only."
            )
    match = lookup_word(message, source_language if mode == "translate" else None)
    if mode == "translate":
        if match and mode == "conversation":
            meaning = match.get("tamil") if target_language == "Tamil" else match.get("english")
            return (
                f"Saurashtra reference word: {match['saurashtra']}\n"
                f"{target_language} meaning: {meaning}\n"
                "This word is from the reference list; fluent-speaker review is pending."
            )
        if match:
            return match["saurashtra"]
        return (
            f"I couldn't find an exact {source_language} word match in the current "
            "Saurashtra dictionary. Try a single word or a dictionary meaning; full "
            "sentences are not supported yet."
        )
    if match:
        return match["saurashtra"]

    if mode == "lesson":
        return (
            "Let's practise step by step. Pick a word from the reference list, review it, "
            "and practise recalling it. Reference entries still need fluent-speaker review, "
            "and verified pronunciation recordings are not available yet."
        )
    if any(word in msg for word in ["hello", "greet", "greeting", "வணக்கம்"]):
        return (
            "We can practise greetings. For Saurashtra, VathoX needs a phrase and recording "
            "verified by a fluent speaker before presenting it as correct. I can help you "
            "structure the lesson in English or Tamil in the meantime."
        )
    if any(word in msg for word in ["translate", "meaning", "say in saurashtra"]):
        return (
            "I can help with the approved reference dictionary in this app. Try a specific "
            "word like 'nekku' or 'pollo' to look up its English meaning."
        )
    if mode == "conversation":
        if target_language == "Tamil":
            return (
                "இது டெமோ பயன்முறை; நேரடி AI பதில்கள் இயக்கப்படவில்லை. "
                "குறிப்புப் பட்டியலில் உள்ள சௌராஷ்டிரச் சொற்களைப் பயிற்சி செய்யலாம். "
                "வாக்கிய வரைவை உருவாக்கவும், தமிழில் விளக்கவும் API விசையுடன் நேரடி AI-ஐ இயக்கவும்."
            )
        if "family" in msg or "home" in msg or "relative" in msg:
            return (
                "Let's set up a family conversation. Who are you talking with, and what "
                "would you like to discuss? I can help plan the practice, but Saurashtra "
                "phrases must come from the reference list."
            )
        if "market" in msg or "shop" in msg or "shopping" in msg:
            return (
                "Let's set up a market conversation. Are you buying something or asking "
                "about a price? I can help structure the practice, but Saurashtra phrases "
                "must come from the reference list."
            )
        if "meet" in msg or "introduction" in msg:
            return (
                "Let's practise meeting someone. Is this a first introduction or a greeting "
                "with someone you know? I can help plan it without inventing Saurashtra phrases."
            )
    if mode == "roleplay":
        return (
            "Role-play scene ready. Tell me which part you want to practise first. I can "
            "guide the situation, and will use only Saurashtra words found in the reference list."
        )
    return (
        "Welcome to VathoX AI Companion! I can help plan Saurashtra practice, role-play "
        "everyday situations, and explain learning steps in English or Tamil. This is demo "
        "mode because no AI API key is configured, but the built-in dictionary entries are ready."
    )

def live_ai_reply(message, target_language, mode, practice=None):
    # Optional OpenAI Responses API integration. Uses the official SDK if installed.
    try:
        from openai import OpenAI
        client = OpenAI(api_key=API_KEY)
        prompt = f"User-selected explanation language: {target_language}. Practice mode: {mode}.\nUser message: {message}"
        if mode == "conversation":
            reference_words = [
                {
                    "saurashtra": entry["saurashtra"],
                    "english": entry["english"],
                    "tamil": entry["tamil"],
                }
                for entry in VERIFIED_PHRASES
            ]
            prompt += (
                "\nThe following complete word list comes from user-provided references. "
                "It has not been independently reviewed by a fluent speaker; use words as "
                "reference material, not proof of correct grammar or spelling. In conversation "
                "practice, provide a Saurashtra draft followed by an explanation in the "
                "selected language, and label any composed sentence as unverified.\n"
                f"Reference word list: {json.dumps(reference_words, ensure_ascii=False)}"
            )
            if isinstance(practice, dict):
                entry = lookup_word(str(practice.get("saurashtra") or ""))
                pattern_intents = {
                    "want": "Express a simple desire for the selected word.",
                    "where": "Ask where the selected word or item is.",
                    "request": "Make a polite request involving the selected word.",
                }
                pattern = pattern_intents.get(str(practice.get("pattern") or ""))
                if entry and pattern:
                    prompt += (
                        f"\nSelected reference word: {json.dumps(entry, ensure_ascii=False)}"
                        f"\nPractice intent: {pattern}"
                        "\nReturn a short Saurashtra sentence draft in Latin transliteration, "
                        f"then explain its intended meaning in {target_language}. Clearly label "
                        "the Saurashtra sentence as an unverified AI draft. Do not claim its "
                        "grammar is correct."
                    )
        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            input=prompt
        )
        return response.output_text
    except ImportError:
        return "AI API key is configured, but the OpenAI Python package is missing. Install the packages listed in requirements.txt."
    except Exception as exc:
        # Keep internal error details out of the UI.
        app.logger.exception("AI request failed")
        return "The AI service could not respond right now. Check the API key, model access, network connection, and server terminal."

@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/phrasebook")
def phrasebook_page():
    return render_template("phrasebook.html")


@app.route("/history")
def history_page():
    return render_template("history.html")


@app.route("/kids/<mascot>")
def kids_mascot(mascot):
    mascots = {
        "chota-bheem": {
            "name": "Chota Bheem",
            "image": "cartoons/chota-bheem.jpg",
        },
        "shinzo": {
            "name": "Shinzo",
            "image": "cartoons/shinzo.jpg",
        },
        "ninja-hattori": {
            "name": "Ninja Hattori",
            "image": "cartoons/ninja-hattori.jpg",
        },
    }
    selected = mascots.get(mascot)
    if not selected:
        return home(), 404
    return render_template("kids.html", mascot=selected)


@app.route("/")
def home():
    mode = request.args.get("mode", "conversation")
    if mode not in ("conversation", "lesson", "translate", "roleplay"):
        mode = "conversation"
    source_language = request.args.get("language", "English")
    if source_language not in ("English", "Tamil", "Hindi"):
        source_language = "English"
    query = request.args.get("q", "").strip()[:100]
    matches = []
    if query:
        normalized_query = normalize_lookup_text(query)
        matches = [
            entry for entry in VERIFIED_PHRASES
            if any(
                normalized_query in normalize_lookup_text(entry.get(field) or "")
                for field in ("saurashtra", "english", "tamil")
            )
        ][:50]
    return render_template(
        "index.html",
        mode=mode,
        target_language="English",
        source_language=source_language,
        message="",
        reply=None,
        error=None,
        lookup_query=query,
        lookup_matches=matches,
        response_mode=None,
    )


@app.route("/", methods=["POST"])
def submit_message():
    mode = request.form.get("mode", "conversation")
    if mode not in ("conversation", "lesson", "translate", "roleplay"):
        mode = "conversation"
    target_language = request.form.get("language", "English")
    if target_language not in ("English", "Tamil", "Hindi"):
        target_language = "English"
    source_language = request.form.get("source_language", "English")
    if source_language not in ("English", "Tamil", "Hindi"):
        source_language = "English"
    message = request.form.get("message", "").strip()
    error = None
    reply = None
    response_mode = None

    if not message:
        error = "Type a message first."
    elif len(message) > 4000:
        error = "Please keep each message under 4,000 characters."
    elif mode == "translate":
        reply = local_demo_reply(message, target_language, mode, source_language)
        response_mode = "Reference dictionary"
    elif API_KEY:
        reply = live_ai_reply(message, target_language, mode)
        response_mode = "AI companion"
    else:
        reply = local_demo_reply(message, target_language, mode)
        response_mode = "Demo mode"

    return render_template(
        "index.html",
        mode=mode,
        target_language=target_language,
        source_language=source_language,
        message=message,
        reply=reply,
        error=error,
        lookup_query="",
        lookup_matches=[],
        response_mode=response_mode,
    )

@app.route("/api/companion", methods=["POST"])
def companion():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    target_language = str(data.get("language", "English"))[:40]
    source_language = str(data.get("source_language", "English"))[:40]
    mode = str(data.get("mode", "conversation"))[:40]
    practice = data.get("practice")
    if not message:
        return jsonify({"reply": "Type a message first.", "mode": "demo"})
    if len(message) > 4000:
        return jsonify({"reply": "Please keep each message under 4,000 characters.", "mode": "demo"}), 400
    if mode == "translate":
        if source_language not in ("English", "Tamil", "Hindi"):
            return jsonify({"reply": "Choose English, Tamil, or Hindi as the source language.", "mode": "dictionary"}), 400
        return jsonify({
            "reply": local_demo_reply(message, target_language, mode, source_language),
            "mode": "dictionary"
        })
    if API_KEY:
        reply = live_ai_reply(message, target_language, mode, practice)
        return jsonify({"reply": reply, "mode": "ai"})
    return jsonify({
        "reply": local_demo_reply(message, target_language, mode, practice=practice),
        "mode": "demo",
    })

@app.route("/api/phrasebook", methods=["GET"])
def phrasebook():
    return jsonify({"phrases": VERIFIED_PHRASES})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/lookup", methods=["GET"])
def lookup_route():
    query = (request.args.get("q") or "").strip()
    source_language = (request.args.get("language") or "").strip()
    if not query:
        return jsonify({"error": "Please provide a word to look up."}), 400
    match = lookup_word(query, source_language)
    if not match:
        return jsonify({"result": None, "query": query})
    return jsonify({"result": match, "query": query})


@app.route("/api/translate", methods=["POST"])
def translate_route():
    data = request.get_json(silent=True) or {}
    text = str(data.get("text", "")).strip()
    source = str(data.get("source", "English")).strip()
    target = str(data.get("target", "Saurashtra")).strip()

    allowed_languages = {"English", "Tamil", "Hindi", "Saurashtra"}
    if not text:
        return jsonify({"error": "Enter text to translate."}), 400
    if len(text) > 200:
        return jsonify({"error": "Translation lookup supports up to 200 characters."}), 400
    if source not in allowed_languages or target not in allowed_languages:
        return jsonify({"error": "Unsupported language selection."}), 400
    if source == target:
        return jsonify({"error": "Choose two different languages."}), 400

    if source == "Saurashtra":
        match = lookup_word(text)
    elif source in ("English", "Tamil", "Hindi"):
        match = lookup_word(text, source)
    else:
        match = None

    if not match:
        return jsonify({
            "translated_text": None,
            "source": source,
            "target": target,
            "status": "not_found",
            "message": "This exact term is not in the reference phrasebook."
        }), 404

    target_field = {
        "Saurashtra": "saurashtra",
        "English": "english",
        "Tamil": "tamil",
        "Hindi": "english",
    }.get(target)
    translated_text = match.get(target_field) if target_field else None
    if not translated_text:
        return jsonify({
            "translated_text": None,
            "source": source,
            "target": target,
            "status": "not_found",
            "message": f"No {target} entry is available for this term."
        }), 404

    return jsonify({
        "translated_text": translated_text,
        "source": source,
        "target": target,
        "status": "reference",
        "reference": match,
        "notice": "Reference result; fluent-speaker review is pending."
    })

if __name__ == "__main__":
    print("\\nVathoX AI Companion is starting...")
    port = int(os.getenv("PORT", "5000"))
    print(f"Open http://127.0.0.1:{port}")
    if not API_KEY:
        print("Running in DEMO mode. Set OPENAI_API_KEY to enable live AI responses.")
    app.run(host="0.0.0.0", port=port, debug=False)
