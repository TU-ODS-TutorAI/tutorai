#!/usr/bin/python3

GERMAN_KEYS = {
                'title': 'Titel des Moduls',
                'credits': 'Leistungspunkte',
                'number': 'Modulnummer',
                'version': 'Version',
                'faculty': 'Fakultät',
                'office': 'Sekretariat',
                'institute': 'Institut',
                'areaOfExpertise': 'Fachgebiet',
                'responsiblePerson': 'Verantwortliche Person',
                'contactPerson': 'Ansprechpartner',
                'email': 'E-Mail-Adresse',
                'website': 'Webseite',
                'learningOutcomes': 'Lernergebnisse',
                'content': 'Lehrinhalte',
                'teachingAndLearningMethods': 'Beschreibung der Lehr-und Lernformen',
                'mandatoryRequirements': 'Voraussetzungen für die Teilnahme / Prüfung',
                'desirablePrerequisites': 'Wünschenswerte Vorrausetzungen',
                'grading': 'Benotung',
                'typeOfExam': 'Prüfungsform',
                'typeOfPortfolioExamination': 'Art der Portfolioprüfung',
                'language': 'Sprache',
                'duration': 'Dauer/Umfang',
                'testDescription': 'Prüfungsbeschreibung',
                'durationOfTheModule': 'Dauer des Moduls',
                'maximumNumberOfParticipants': 'Maximale teilnehmende Personen',
                'registrationProcedures': 'Anmeldeformalitäten',
                'lectureNotes': 'Skript in Papierform',
                'electronicalLectureNotes': 'Skript in elektronischer Form',
                'literature': 'Literatur'
            }

def translateKeys(data):
    data_with_german_keys = {}
    for key, value in data.items():
        german_key = GERMAN_KEYS[key]
        data_with_german_keys[german_key] = value

    return data_with_german_keys

