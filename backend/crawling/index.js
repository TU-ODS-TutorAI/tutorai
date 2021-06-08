const express = require('express')
const mongoose = require('mongoose')

const config = require('./config')
const https = require('./https')
const Module = require('./Moses/Module')
const app = express()

mongoose.connect(config.network.mongoURI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    useFindAndModify: false,
    useCreateIndex: true
})

const MosesModule = mongoose.model('MosesModule', new mongoose.Schema({
    number: { type: Number },
    version: { type: Number },
    faculty: { type: String },
    office: { type: String },
    institute: { type: String },
    areaOfExpertise: { type: String },
    responsiblePerson: { type: String },
    contactPerson: { type: String },
    email: { type: String },
    credits: { type: Number },
    website: { type: String },
    german: {
        learningOutcomes: { type: String },
        content: { type: String },
        title: { type: String },
        teachingAndLearningMethods: { type: String },
        desirablePrerequisites: { type: String },
        mandatoryRequirements: { type: String },
        grading: { type: String },
        typeOfExam: { type: String },
        typeOfPortfolioExamination: { type: String },
        language: { type: String },
        duration: { type: String },
        testDescription: { type: String },
        durationOfTheModule: { type: String },
        maximumNumberOfParticipants: { type: String },
        registrationProcedures: { type: String },
        lectureNotes: { type: String },
        electronicalLectureNotes: { type: String },
        literature: { type: String }
    },
    english: {
        learningOutcomes: { type: String },
        content: { type: String },
        title: { type: String },
        teachingAndLearningMethods: { type: String },
        desirablePrerequisites: { type: String },
        mandatoryRequirements: { type: String },
        grading: { type: String },
        typeOfExam: { type: String },
        typeOfPortfolioExamination: { type: String },
        language: { type: String },
        duration: { type: String },
        testDescription: { type: String },
        durationOfTheModule: { type: String },
        maximumNumberOfParticipants: { type: String },
        registrationProcedures: { type: String },
        lectureNotes: { type: String },
        electronicalLectureNotes: { type: String },
        literature: { type: String }
    }
}))


let modules
https(config.resources.moses.getLinkToAllModules(), (data) => { modules = Module.getModules(data) })

app.get('/moses', (req, res) => {
    res.send({ modules: modules })
})

app.get('/moses/search/:property', (req, res) => {
    const property = req.params.property
    if (!property) {
        res.status(400).send({ err: "Bad request" })
        return
    }

    const query = req.query.q
    if (!query) {
        res.status(400).send({ err: "Bad request, no query" })
        return
    }

    let mongoQuery = {}
    mongoQuery[property] = new RegExp(query, 'i')
    MosesModule.find(mongoQuery, (err, doc) => {
        res.send(doc)
    })
})

app.get('/moses/:id', (req, res) => {
    const moduleNumber = parseInt(req.params.id)
    if (!moduleNumber) {
        res.status(400).send({ err: "Bad request" })
        return
    }
    const modulInfo = modules.find(e => e.number === moduleNumber)
    if (!modulInfo) {
        res.status(404).send({ err: "Wrong module number, not found" })
        return
    }
    findModuleWithModuleNumber(modulInfo, res)
})

function findModuleWithModuleNumber(modulInfo, res) {
    MosesModule.findOne({ 'number': modulInfo.number }, function (err, doc) {
        if (err || !doc) {
            console.log("no db entry found. crawling, saving in db and sending...")
            https(config.resources.moses.getFullLinkTo(modulInfo.number, modulInfo.version, 1), (germanData) => {
                https(config.resources.moses.getFullLinkTo(modulInfo.number, modulInfo.version, 2), (englishData) => {
                    let newModule = new MosesModule()
                    newModule = createModule(newModule, modulInfo, englishData, germanData)
                    res.send(newModule)
                })
            })
        } else if (modulInfo.version != doc.version) {
            console.log("db entry outdated. crawling, saving in db and sending...")
            https(config.resources.moses.getFullLinkTo(modulInfo.number, modulInfo.version, 1), (germanData) => {
                https(config.resources.moses.getFullLinkTo(modulInfo.number, modulInfo.version, 2), (englishData) => {
                    let newModule = createModule(doc, modulInfo, englishData, germanData)
                    res.send(newModule)
                })
            })
        } else {
            console.log("sending data from db...")
            res.send(doc)
        }
    })
}

function createModule(newModule, modulInfo, englishData, germanData) {
    newModule.number = modulInfo.number
    newModule.version = modulInfo.version
    newModule.german.title = Module.getTitle(germanData, 1)
    newModule.german.learningOutcomes = Module.getLearningOutcomes(germanData, 1)
    newModule.german.content = Module.getContent(germanData, 1)
    newModule.german.teachingAndLearningMethods = Module.getTeachingAndLearningMethods(germanData, 1)
    newModule.german.desirablePrerequisites = Module.getDesirablePrerequisites(germanData, 1)
    newModule.german.mandatoryRequirements = Module.getMandatoryRequirements(germanData, 1)
    newModule.german.grading = Module.getGrading(germanData, 1)
    newModule.german.typeOfExam = Module.getTypeOfExam(germanData, 1)
    newModule.german.typeOfPortfolioExamination = Module.getTypeOfPortfolioExamination(germanData, 1)
    newModule.german.language = Module.getLanguage(germanData, 1)
    newModule.german.duration = Module.getDuration(germanData, 1)
    newModule.german.testDescription = Module.getTestDescription(germanData, 1)
    newModule.german.durationOfTheModule = Module.getDurationOfTheModule(germanData, 1)
    newModule.german.maximumNumberOfParticipants = Module.getMaximumNumberOfParticipants(germanData, 1)
    newModule.german.registrationProcedures = Module.getRegistrationProcedures(germanData, 1)
    newModule.german.lectureNotes = Module.getLectureNotes(germanData, 1)
    newModule.german.electronicalLectureNotes = Module.getElectronicalLectureNotes(germanData, 1)
    newModule.german.literature = Module.getLiterature(germanData, 1)
    newModule.english.title = Module.getTitle(englishData, 2)
    newModule.english.learningOutcomes = Module.getLearningOutcomes(englishData, 2)
    newModule.english.content = Module.getContent(englishData, 2)
    newModule.english.teachingAndLearningMethods = Module.getTeachingAndLearningMethods(englishData, 2)
    newModule.english.desirablePrerequisites = Module.getDesirablePrerequisites(englishData, 2)
    newModule.english.mandatoryRequirements = Module.getMandatoryRequirements(englishData, 2)
    newModule.english.grading = Module.getGrading(englishData, 2)
    newModule.english.typeOfExam = Module.getTypeOfExam(englishData, 2)
    newModule.english.typeOfPortfolioExamination = Module.getTypeOfPortfolioExamination(englishData, 2)
    newModule.english.language = Module.getLanguage(englishData, 2)
    newModule.english.duration = Module.getDuration(englishData, 2)
    newModule.english.testDescription = Module.getTestDescription(englishData, 2)
    newModule.english.durationOfTheModule = Module.getDurationOfTheModule(englishData, 2)
    newModule.english.maximumNumberOfParticipants = Module.getMaximumNumberOfParticipants(englishData, 2)
    newModule.english.registrationProcedures = Module.getRegistrationProcedures(englishData, 2)
    newModule.english.lectureNotes = Module.getLectureNotes(englishData, 2)
    newModule.english.electronicalLectureNotes = Module.getElectronicalLectureNotes(englishData, 2)
    newModule.english.literature = Module.getLiterature(englishData, 2)
    newModule.faculty = Module.getFaculty(germanData)
    newModule.office = Module.getOffice(germanData)
    newModule.institute = Module.getInstitute(germanData)
    newModule.areaOfExpertise = Module.getAreaOfExpertise(germanData)
    newModule.responsiblePerson = Module.getResponsiblePerson(germanData)
    newModule.contactPerson = Module.getContactPerson(germanData)
    newModule.email = Module.getEmail(germanData)
    newModule.credits = Module.getCredits(germanData)
    newModule.website = Module.getWebsite(germanData)
    newModule.save()
    return newModule
}

app.listen(config.network.port, () => { console.log(`Backend listening at http://localhost:${config.network.port}`) })