<<<<<<< HEAD
var SPREADSHEET = PropertiesService.getScriptProperties().getProperty('spreadsheet');
var DATAPLATTFORM_INGEST_APIKEY = PropertiesService.getScriptProperties().getProperty('dataplattform_ingest_apikey');
var DATAPLATTFORM_INGEST_URL = PropertiesService.getScriptProperties().getProperty('dataplattform_ingest_url');

=======
>>>>>>> googleforms-testing
function onInstall(e) {
  onOpen(e);
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
  var html = HtmlService.createTemplateFromFile('start_collection').evaluate();
  FormApp.getUi().showModalDialog(html, 'Start collecting data to the dataplatform.');
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
  Logger.log(formObject);
  Logger.log(questionsToInclude);
  if (questionsToInclude.length < 1) {
    return "You didn't select any questions!"
  }
  result = addToPlatform(questionsToInclude)
  return result;
}

function processAllDataForm(formObject) {
  var scriptProperties = PropertiesService.getScriptProperties()
  var formId = FormApp.getActiveForm().getId();
  var questionsToInclude = formObject["questions"]
  var timestamp = 0
  if (formObject['time'].length > 0) {
    timestamp = new Date(formObject['time'])
  }
  postFormDataToIngest(scriptProperties, formId, timestamp, questionsToInclude);
  return "All your data was added! Want to collect new data automatically? Turn on collection of data from this form as well!"
}

function addToPlatform(questionsToInclude) {
  var spreadsheetId = PropertiesService.getScriptProperties().getProperty('spreadsheet_Id');
  var formId = FormApp.getActiveForm().getId();

  if (FormApp.getActiveForm().isQuiz()) {
    var output = 'Your form is a quiz and cannot be added!';
  }
  else if (formExists(spreadsheetId, formId)) {
    var output = 'Your form is already in the platform and can\'t be added again! If you want to change questions being collected, remove and add the form again.';
  }
  else {
    writeToSpreadsheet(spreadsheetId, formId, questionsToInclude);
    var output = 'Your form has been added to the dataplatform and will now be polled for new responses indefintely :)!';
  }
  return output;
}

function stopCollectingData() {
  var spreadsheetId = PropertiesService.getScriptProperties().getProperty('spreadsheet_Id');
  var formId = FormApp.getActiveForm().getId();

  if (removeForm(spreadsheetId, formId)) {
    var output = 'Responses will no longer be collected from your form!';
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

function removeForm(spreadsheetId, formId) {
  var row = formExists(spreadsheetId, formId)
  if (row != false) {
    Sheets.Spreadsheets.batchUpdate({
      "requests":
        [{
          "deleteDimension": {
            "range": {
              "dimension": "ROWS",
              "startIndex": row,
              "endIndex": row+1
            }
          }
        },
        ],
    }, spreadsheetId);
    return true;
  }
  return false;
}

function formExists(spreadsheetId, formId) {
  var response = Sheets.Spreadsheets.Values.get(spreadsheetId, 'A:A');
  for (row in response.values) {
    if (response.values[row][0] == formId) {
      return parseInt(row);
    }
  }
  return false;
}

function writeToSpreadsheet(spreadsheetId, formId, questionsToInclude) {
  var values = [
    [formId, new Date(), questionsToInclude.toString()]
  ];
  var valueRange = Sheets.newRowData();
  valueRange.values = values;
  var appendRequest = Sheets.newAppendCellsRequest();
  appendRequest.sheetId = spreadsheetId;
  appendRequest.rows = [valueRange];
  Sheets.Spreadsheets.Values.append(valueRange, spreadsheetId, 'A:C', {
    valueInputOption: 'RAW'
  });
}

function runAtInterval() {
  var scriptProperties = PropertiesService.getScriptProperties()
  readDataFromSpreadsheet(scriptProperties) 
  
}

function readDataFromSpreadsheet(scriptProperties) {
  var spreadsheetId = scriptProperties.getProperty('spreadsheet_Id')
  var response = Sheets.Spreadsheets.Values.get(spreadsheetId, 'A:C');
  var formId;
  var timestamp;
  for (row in response.values) {
    row = parseInt(row);
    // Skip headers
    if (row == 0) {
      continue;
    }
    formId = response.values[row][0];
    timestamp = new Date(response.values[row][1]);
    questionsToInclude = response.values[row][2].split(",");
    postFormDataToIngest(scriptProperties, formId, timestamp, questionsToInclude);
    updateSpreadsheetTimestamp(spreadsheetId, row+1, new Date());
  }
}

function postFormDataToIngest(scriptProperties, formId, timestamp, questionsToInclude) {
  var apiKey = scriptProperties.getProperty('dataplattform_ingest_apikey');
  var url = scriptProperties.getProperty('dataplattform_ingest_url');
  try {
    var file = DriveApp.getFileById(formId);
    var form = FormApp.openById(formId);    
  
    if (timestamp == 0) {
      var formResponses = form.getResponses();
    }
    else {
      var formResponses = form.getResponses(timestamp);
    }
    for (var i = 0; i < formResponses.length; i++) {
      var formResponse = formResponses[i];
      var itemResponses = formResponse.getItemResponses();
      for (var j = 0; j < itemResponses.length; j++) {
        var itemResponse = itemResponses[j];
        if (questionsToInclude.indexOf(itemResponse.getItem().getId().toString()) > -1) {
          var data = {
            'formId': form.getId(),
            'formTitle': form.getTitle(),
            'formDescription': form.getDescription(),
            'formCreated': Math.floor(file.getDateCreated().valueOf() / 1000),
            'formOwner': file.getOwner().getName(),
            'formPublishedUrl': form.getPublishedUrl(),
            'responseId': formResponse.getId(),
            'responseTimestamp': Math.floor(formResponse.getTimestamp().valueOf() / 1000),
            'responseQuestion': itemResponse.getItem().getTitle(),
            'responseAnswer': itemResponse.getResponse(),
            'questionId': itemResponse.getItem().getId(),
            'questionType': itemResponse.getItem().getType().toString()
          };
          data = [data];
          var options = {
            'method': 'post',
            'contentType': 'application/json',
            'payload': JSON.stringify(data),
            'headers': { 'x-api-key': apiKey }
          };
          UrlFetchApp.fetch(url, options);
        }
      }
    }
  }
  catch (e) {
    console.error(e.name)
    console.error(e.name + ": " + e.message)
    console.error("formId: " + formId)
  }
}

function updateSpreadsheetTimestamp(spreadsheetId, row, timestamp) {
  var values = [
    [timestamp]
  ];
  var valueRange = Sheets.newValueRange();
  valueRange.values = values;
  var range = "B" + row;
  Sheets.Spreadsheets.Values.update(valueRange, spreadsheetId, range, {
    valueInputOption: 'RAW'
  });
}