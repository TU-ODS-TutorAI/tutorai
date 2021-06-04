class Module {
    static getModules(html) {
        const regex = /<a href=".*?nummer=(\d*).*?version=(\d*)" title="Modulbeschreibung anzeigen">(.*?)<\/a>/g
        let results = []
        let result = regex.exec(html)
        while (result) {
            results.push({ number: parseInt(result[1]), version: parseInt(result[2]), title: result[3] })
            result = regex.exec(html)
        }

        results.sort((a, b) => {
            const numberDiff = a.number - b.number;
            if (numberDiff == 0)
                return a.version - a.version;
            return numberDiff
        })

        results = results.filter(module => {
            for (const otherModule of results) {
                if (otherModule.number == module.number && otherModule.version > module.version)
                    return false
            }
            return true
        })

        return results
    }

    static getTitle(html, language) {
        const regex = language == 1 ? /<h1>([\s\S]*?)<\/h1>/ : /<small><span style="font-size: x-large;">([\s\S]*?)<\/span>\s*<\/small>/
        return getFirstGroupOfRegex(regex, html)

    }

    static getLearningOutcomes(html, language) {
        const regex = language == 1 ?
            /Lernergebnisse<\/h3>\s*<\/div>\s*<div class="col-xs-12">\s*<span class="preformatedTextarea">([\s\S]*?)<\/span>/ :
            /Learning Outcomes<\/h3>\s*<\/div>\s*<div class="col-xs-12">\s*<span class="preformatedTextarea">([\s\S]*?)<\/span>/
        return getFirstGroupOfRegex(regex, html)
    }

    static getContent(html, language) {
        const regex = language == 1 ?
            /Lehrinhalte<\/h3>\s*<\/div>\s*<div class="col-xs-12">\s*<span class="preformatedTextarea">([\s\S]*?)<\/span>/ :
            /Content<\/h3>\s*<\/div>\s*<div class="col-xs-12">\s*<span class="preformatedTextarea">([\s\S]*?)<\/span>/
        return getFirstGroupOfRegex(regex, html)
    }

    static getTeachingAndLearningMethods(html, language) {
        const regex = language == 1 ?
            /Beschreibung der Lehr- und Lernformen<\/h3>\s*<\/div>\s*<div class="col-xs-12">\s*<span class="preformatedTextarea">([\s\S]*?)<\/span>/ :
            /Description of Teaching and Learning Methods<\/h3>\s*<\/div>\s*<div class="col-xs-12">\s*<span class="preformatedTextarea">([\s\S]*?)<\/span>/
        return getFirstGroupOfRegex(regex, html)
    }

    static getDesirablePrerequisites(html, language) {
        const regex = language == 1 ?
            /Wünschenswerte Voraussetzungen für die Teilnahme an den <strong>Lehrveranstaltungen<\/strong>\s*:\s*<\/h4>\s*<span class="preformatedTextarea">([\s\S]*?)<\/span>/ :
            /Desirable prerequisites for participation in the\s*<strong>courses<\/strong>\s*:\s*<\/h4>\s*<span class="preformatedTextarea">([\s\S]*?)<\/span>/
        return getFirstGroupOfRegex(regex, html)
    }

    static getMandatoryRequirements(html, language) {
        const regex = language == 1 ?
            /Verpflichtende Voraussetzungen für die <strong>Modulprüfungsanmeldung<\/strong>:<\/h4>\s*<div id="j_idt106:j_idt577" class="ui-messages ui-widget" aria-live="polite"><\/div>\s*<div class="row">([\s\S]*?)<\/div>\s*<\/div>\s*<\/div>\s*<\/span>/ :
            /Mandatory requirements for the <strong>module test application<\/strong>:<\/h4>\s*<div id="j_idt106:j_idt577" class="ui-messages ui-widget" aria-live="polite"><\/div>\s*<div class="row">([\s\S]*?)<\/div>\s*<\/div>\s*<\/div>\s*<\/span>/
        return getFirstGroupOfRegex(regex, html)
    }

    static getGrading(html, language) {
        const regex = language == 1 ? /Benotung<\/h4>([\s\S]*?)</ : /Grading<\/h4>([\s\S]*?)</
        return getFirstGroupOfRegex(regex, html)
    }

    static getTypeOfExam(html, language) {
        const regex = language == 1 ? /Prüfungsform<\/h4>([\s\S]*?)</ : /Type of exam<\/h4>([\s\S]*?)</
        return getFirstGroupOfRegex(regex, html)
    }

    static getTypeOfPortfolioExamination(html, language) {
        const regex = language == 1 ? /Art der Portfolioprüfung<\/h4>([\s\S]*?)</ : /Type of portfolio examination<\/h4>([\s\S]*?)</
        return getFirstGroupOfRegex(regex, html)
    }

    static getLanguage(html, language) {
        const regex = language == 1 ? /Sprache<\/h4>([\s\S]*?)</ : /Language<\/h4>([\s\S]*?)</
        return getFirstGroupOfRegex(regex, html)
    }

    static getDuration(html, language) {
        const regex = language == 1 ? /Dauer\/Umfang:\s*<\/h4>\s*<span class="preformatedTextarea">([\s\S]*?)<\/span>/ : /Duration\/Extent:\s*<\/h4>\s*<span class="preformatedTextarea">([\s\S]*?)<\/span>/
        return getFirstGroupOfRegex(regex, html)
    }

    static getTestDescription(html, language) {
        const regex = language == 1 ?
            /Prüfungsbeschreibung \(Abschluss des Moduls\)\s*<\/h4>\s*<span class="preformatedTextarea">([\s\S]*?)<\/span>/ :
            /Test description \(Module completion\)\s*<\/h4>\s*<span class="preformatedTextarea">([\s\S]*?)<\/span>/
        return getFirstGroupOfRegex(regex, html)
    }

    static getDurationOfTheModule(html, language) {
        const regex = language == 1 ?
            /Dauer des Moduls<\/h3>\s*<\/div>\s*<div class="col-xs-12">([\s\S]*?)<\/div>/ :
            /Duration of the Module<\/h3>\s*<\/div>\s*<div class="col-xs-12">([\s\S]*?)<\/div>/
        return getFirstGroupOfRegex(regex, html)
    }

    static getMaximumNumberOfParticipants(html, language) {
        const regex = language == 1 ?
            /Maximale teilnehmende Personen<\/h3>\s*<\/div>\s*<div class="col-xs-12">([\s\S]*?)<\/div>/ :
            /Maximum Number of Participants<\/h3>\s*<\/div>\s*<div class="col-xs-12">([\s\S]*?)<\/div>/
        return getFirstGroupOfRegex(regex, html)
    }

    static getRegistrationProcedures(html, language) {
        const regex = language == 1 ?
            /Anmeldeformalitäten<\/h3>\s*<\/div>\s*<div class="col-xs-12">([\s\S]*?)<\/div>/ :
            /Registration Procedures<\/h3>\s*<\/div>\s*<div class="col-xs-12">([\s\S]*?)<\/div>/
        return getFirstGroupOfRegex(regex, html)
    }

    static getLectureNotes(html, language) {
        const regex = language == 1 ?
            /Skript in Papierform<\/h4>\s*Verfügbarkeit:([\s\S]*?)<\/div>/ :
            /Lecture notes<\/h4>\s*Availability:([\s\S]*?)<\/div>/
        return getFirstGroupOfRegex(regex, html)
    }

    static getElectronicalLectureNotes(html, language) {
        const regex = language == 1 ?
            /Skript in elektronischer Form<\/h4>\s*Verfügbarkeit:([\s\S]*?)<\/div>/ :
            /Electronical lecture notes <\/h4>\s*Availability:([\s\S]*?)<\/div>/
        return getFirstGroupOfRegex(regex, html)
    }

    static getLiterature(html, language) {
        const regex = language == 1 ?
            /Empfohlene Literatur<\/th>\s*<\/tr>\s*<tr>([\s\S]*?)<\/tr>/ :
            /Recommended literature<\/th>\s*<\/tr>\s*<tr>([\s\S]*?)<\/tr>/
        return getFirstGroupOfRegex(regex, html)
    }

    static getFaculty(html) {
        const regex = /Fakultät:<\/label>[\s\S]*?\/>(.*)/
        return getFirstGroupOfRegex(regex, html)
    }

    static getOffice(html) {
        const regex = /Sekretariat:<\/label>[\s\S]*?\/>(.*)/
        return getFirstGroupOfRegex(regex, html)
    }

    static getInstitute(html) {
        const regex = /Institut:<\/label>[\s\S]*?\/>(.*)/
        return getFirstGroupOfRegex(regex, html)
    }

    static getAreaOfExpertise(html) {
        const regex = /Fachgebiet:<\/label>[\s\S]*?\/>(.*)/
        return getFirstGroupOfRegex(regex, html)
    }

    static getResponsiblePerson(html) {
        const regex = /Verantwortliche Person:<\/label>[\s\S]*?\/>(.*)/
        return getFirstGroupOfRegex(regex, html)
    }

    static getContactPerson(html) {
        const regex = /Ansprechpartner:<\/label>[\s\S]*?\/>(.*)/
        return getFirstGroupOfRegex(regex, html)
    }

    static getEmail(html) {
        const regex = /E-Mail-Adresse:<\/label>[\s\S]*?\/>(.*)/
        return getFirstGroupOfRegex(regex, html)
    }

    static getCredits(html) {
        const regex = /Leistungspunkte:<\/label>[\s\S]*?<span[\s\S]*?>(\d*)/
        return getFirstGroupOfRegex(regex, html)
    }

    static getWebsite(html) {
        const regex = /Webseite:<\/label>[\s\S]*?<a href="([\s\S]*?)"/
        return getFirstGroupOfRegex(regex, html)
    }
}

function getFirstGroupOfRegex(regex, data) {
    const result = regex.exec(data)
    if (result && result.length > 1)
        return cleanMatch(result[1])
    return ""
}

function cleanMatch(match) {
    const html = /<.*?>/g // this will remove html like: <span>, </div> etc.
    const multipleNewLines = /[\r\n ]*\n[\r\n ]*/g // this will remove multiple newlines and spaces in between
    const multipleSpaces = /  +/g // this will remove multiple spaces
    return match.replace(html, ' ').replace(multipleNewLines, '\n').replace(multipleSpaces, ' ').trim()
}

module.exports = Module