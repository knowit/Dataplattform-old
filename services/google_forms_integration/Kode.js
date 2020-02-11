<<<<<<< HEAD
var SPREADSHEET = PropertiesService.getScriptProperties().getProperty('spreadsheet');
var DATAPLATTFORM_INGEST_APIKEY = PropertiesService.getScriptProperties().getProperty('dataplattform_ingest_apikey');
var DATAPLATTFORM_INGEST_URL = PropertiesService.getScriptProperties().getProperty('dataplattform_ingest_url');

=======
>>>>>>> googleforms-testing
function onInstall(e) {
  onOpen(e);
  PropertiesService.getUserProperties().setProperty('scriptActivated', 'false')
}

// Add a custom menu to the active form, including a separator and a sub-menu.
function onOpen(e) {
  FormApp.getUi()
    .createMenu('Dataplattform')
    .addItem('Start collecting data from this form', 'showQuestionsToInclude')
    .addItem('Stop collecting data from this form', 'stopCollectingData')
    .addItem('Send all data from this form', 'sendAllData')
    .addItem('Delete data related to this form from the platform', 'removeAllData')
    .addToUi();
}

function removeAllData() {
  var scriptProperties = PropertiesService.getScriptProperties()
  var apiKey = scriptProperties.getProperty('dataplattform_ingest_apikey');
  var url = scriptProperties.getProperty('dataplattform_ingest_url');
  var formId = FormApp.getActiveForm().getId();
  data = [{
    'deletionProcedure': true, 
    'formId': formId
  }];
  var options = {
    'method': 'post',
    'contentType': 'application/json',
    'payload': JSON.stringify(data),
    'headers': { 'x-api-key': apiKey }
  };
  UrlFetchApp.fetch(url, options);

  var htmlOutput = HtmlService
    .createHtmlOutput("All data related to your form has been removed from the dataplatform! Remember to also stop collection of new data if relevant!")
    .setWidth(250)
    .setHeight(300);
  FormApp.getUi().showModalDialog(htmlOutput, 'Result');
}

function showQuestionsToInclude() {
  var valid_form = false;
  if (form.isQuiz()) {
    var valid_form = 'Your form is a quiz and cannot be added!';
  }
  else if (userProps.getProperty('scriptActivated') == 'true') {
    var valid_form = 'Collection is already active on your form! If you want to change questions being collected, remove and add the form again.';
  }
  if (valid_form == false) {
    var html = HtmlService.createTemplateFromFile('start_collection').evaluate();
    FormApp.getUi().showModalDialog(html, 'Start collecting data to the dataplatform.');
  }
  else {
    var htmlOutput = HtmlService
    .createHtmlOutput(valid_form)
    .setWidth(250)
    .setHeight(300);
    FormApp.getUi().showModalDialog(htmlOutput, 'Result');
  }
}

function sendAllData() {
  var html = HtmlService.createTemplateFromFile('send_all_data').evaluate();
  FormApp.getUi().showModalDialog(html, 'Send all your data');
}

function getFormQuestions() {
  return FormApp.getActiveForm().getItems()
}

function processCollectionForm(formObject) {
  var questionsToInclude = formObject["questions"]
  if (questionsToInclude.length < 1) {
    return "You didn't select any questions!"
  }
  var userProps = PropertiesService.getUserProperties();
  var form = FormApp.getActiveForm();
  userProps.setProperty('questionsToInclude', questionsToInclude.toString())
  userProps.setProperty('scriptActivated', 'true')
  ScriptApp.newTrigger('triggerDataCollection')
    .forForm(form)
    .onFormSubmit()
    .create()
  return 'Success! New form data will now be collected indefinitely! :)';
}

function processAllDataForm(formObject) {
  var questionsToInclude = formObject["questions"]
  if (questionsToInclude.length < 1) {
    return "You didn't select any questions!"
  }
  var timestamp = 0
  if (formObject['time'].length > 0) {
    timestamp = new Date(formObject['time'])
  }
  var scriptProperties = PropertiesService.getScriptProperties()
  var apiKey = scriptProperties.getProperty('dataplattform_ingest_apikey');
  var url = scriptProperties.getProperty('dataplattform_ingest_url');
  var form = FormApp.getActiveForm();
  var file = DriveApp.getFileById(form.getId());
  if (form.isQuiz()) {
    return 'Your form is a quiz, which is not supported!';
  }
  if (timestamp == 0) {
    var formResponses = form.getResponses();
  }
  else {
    var formResponses = form.getResponses(timestamp);
  }
  for (var i = 0; i < formResponses.length; i++) {
    postFormDataToIngest(apiKey, url, file, form, formResponses[i], questionsToInclude)
  }
  return "All your data was added! Want to collect new data automatically? Turn on collection of data from this form as well!"
}

function triggerDataCollection(e) {
  var userProps = PropertiesService.getUserProperties();
  var scriptProperties = PropertiesService.getScriptProperties();
  var apiKey = scriptProperties.getProperty('dataplattform_ingest_apikey');
  var url = scriptProperties.getProperty('dataplattform_ingest_url');
  var form = e.source
  var formResponse = e.response
  var questionsToInclude = userProps.getProperty('questionsToInclude').split(",");
  var file = DriveApp.getFileById(form.getId());
  postFormDataToIngest(apiKey, url, file, form, formResponse, questionsToInclude)
}

function postFormDataToIngest(apiKey, url, file, form, formResponse, questionsToInclude) {
  var itemResponses = formResponse.getItemResponses();
  var data = [];
  var formId = form.getId();
  var formTitle = form.getTitle();
  var formDescription = form.getDescription();
  var formCreated = Math.floor(file.getDateCreated().valueOf() / 1000);
  var formOwner = file.getOwner().getName();
  var formPublishedUrl = form.getPublishedUrl();
  var responseId = formResponse.getId();
  var responseTimestamp = Math.floor(formResponse.getTimestamp().valueOf() / 1000);
  for (var j = 0; j < itemResponses.length; j++) {
    var itemResponse = itemResponses[j];
    var responseQuestion = itemResponse.getItem()
    var responseAnswer = itemResponse.getResponse().toString();
    if (responseAnswer.length == 0) {
      continue;
    }
    if (questionsToInclude.indexOf(responseQuestion.getId().toString()) > -1) {
      data.push({
        'formId': formId,
        'formTitle': formTitle,
        'formDescription': formDescription,
        'formCreated': formCreated,
        'formOwner': formOwner,
        'formPublishedUrl': formPublishedUrl,
        'responseId': responseId,
        'responseTimestamp': responseTimestamp,
        'responseQuestion': responseQuestion.getTitle(),
        'responseAnswer': responseAnswer,
        'questionId': responseQuestion.getId(),
        'questionType': responseQuestion.getType().toString()
      });
    }
  }
  var options = {
    'method': 'post',
    'contentType': 'application/json',
    'payload': JSON.stringify(data),
    'headers': { 'x-api-key': apiKey }
  };
  try {
    UrlFetchApp.fetch(url, options);
  }
  catch (e) {
    console.error(e.name)
    console.error(e.name + ": " + e.message)
    console.error("formId: " + form.getId())
  }
}

function stopCollectingData() {
  var userProps = PropertiesService.getUserProperties();
  if (userProps.getProperty('scriptActivated') == 'true') {
    var output = 'Responses will no longer be collected from your form!';
    userProps.setProperty('scriptActivated', 'false');
    userProps.deleteProperty('questionsToInclude');
    // A trigger is never created twice, therefore we know there's only 1 trigger and we can remove this trigger if script was active. 
    ScriptApp.deleteTrigger(ScriptApp.getUserTriggers(FormApp.getActiveForm())[0])
  } 
  else {
    var output = 'Could not find your form, are you sure it\'s been added to the dataplatform already? :)';
  }
  var htmlOutput = HtmlService
    .createHtmlOutput(output)
    .setWidth(250)
    .setHeight(300);
  FormApp.getUi().showModalDialog(htmlOutput, 'Result');
}
