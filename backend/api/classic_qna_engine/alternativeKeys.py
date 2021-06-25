#!/usr/bin/python3

ALT_KEYS = {
            'Titel des Moduls': ["heißt das Modul", "Name des Moduls"],
            'Leistungspunkte': ["LP"],
            'Modulnummer': ["Nummer des Moduls"],
	    'Version': ["Version des Moduls"],	
            'Fakultät': ["FAK"],
            'Sekretariat': ["Büros"],
            'Ansprechpartner': ["Kontaktperson", "bei Fragen", "kontaktieren", "an wenden"],
            'E-Mail-Adresse': ["email"],
            'Webseite': ["website"],
            'Lernergebnisse': ["Ziele", "Erfahrungen"],
            'Lehrinhalte': ["Stoff", "Themen", "befassen", "lernen"],
            'Beschreibung der Lehr-und Lernformen': ["Aufteilung des Moduls", "Teile des Moduls", "Ablauf des Moduls"],
            'Voraussetzungen für die Teilnahme / Prüfung': ["Hausaufgabenkriterium", "kriterium", "Bedingungen"],
            'Prüfungsform': ["Prüfungsart", "Art von Prüfung"],
            'Dauer/Umfang':["Dauer Prüfung", "Dauer Klausur", "Länge der Prüfung", "Länge der Klausur", "Prüfungslänge", "Klausurlänge"],
	    'Prüfungsbeschreibung': ["Notenschlüssel"],
            'Maximale teilnehmende Personen': ["viele teilnehmen", "Anzahl Teilnehmer"],
            'Anmeldeformalitäten': ["Anmeldung", "anmelden"],
            'Literatur': ["Bücher", "zusätzliche Unterlagen"],
	    'title': ["module called", "name of module"],
	    'credits': ["LP", "credit points"],
	    'number': ["number of module"],
	    'version': ["version of module"],
	    'faculty': ["FAC"],
	    'office': ["secrtary"],
	    'areaOfExpertise': ["field of activity", "subject area"],
	    'contactPerson': [],
	    'website': ["homepage"],
	    'learningOutcomes': ["goals", "experiences", "learn"],
	    'content': ["module about", "themes"],
	    'teachingAndLearningMethods': ["parts of module"],
	    'mandatoryRequirements': ["criterias", "conditions"],
	    'desirablePrerequisites': ["prior knowledge"],
	    'duration': ["duration of exam", "time in exam", "long is exam"],
	    'testDescription': ["grading key"],
	    'maximumNumberOfParticipants': ["many take part", "amount of participants"],
	    'registrationProcedures': ["enroll"],
	    'lectureNotes': ["written script"],
	    'electronicalLectureNotes': ["electronical script", "online script"],
	    'literature': ["books", "additional material"]
            }

def getAlternativeKeys(key):
    keys = ALT_KEYS.get(key)
    if(keys == None):
        return []
    else:
        return keys

