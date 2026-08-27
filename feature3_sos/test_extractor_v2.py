from extractor_v2 import extract_sos_v2


tests = [

    "14 people including 8 month pregnant lady, old patient lady, 4 years old kid stranded without food.",

    "20-30 people stuck with no contact. Need food and water.",

    "4yr old child urgently needs oxygen. To be shifted from Edathwa to medical mission hospital Thiruvalla. Contact 9946265576.",

    "50 stranded people and one kid passed away. Location Vadakkekara. Contact 8129499346.",

    "Need urgent help. 4000 people trapped in North Paravoor. Most of them are children. 8089788023.",

    "A family of five including a 60 year old aunty is stranded at Kottayilkovilakam Road."
]


for i, message in enumerate(tests, 1):

    print("\n" + "=" * 80)
    print("TEST", i)
    print("MESSAGE:", message)

    result = extract_sos_v2(message)

    print("\nEXTRACTED:")
    print(result)