var SPREADSHEET = PropertiesService.getScriptProperties().getProperty('spreadsheet');
var DATAPLATTFORM_INGEST_APIKEY = PropertiesService.getScriptProperties().getProperty('dataplattform_ingest_apikey');
var DATAPLATTFORM_INGEST_URL = PropertiesService.getScriptProperties().getProperty('dataplattform_ingest_url');

function doGet(e) {
  var formId = e['parameter']['formId'];
  var action = e['parameter']['action'];
  switch (action) {
    case 'add':
      var isValidForm = getAccessToForm(formId);
      if (!isValidForm) {
        return HtmlService.createHtmlOutput('We could not find your form :( Please check that the Id is correct and that it is not a quiz!');
      }
      if (formExists(SPREADSHEET, formId)) {
        return HtmlService.createHtmlOutput('Your form is already in the platform and can\'t be added again!');
      }
      writeToSpreadsheet(SPREADSHEET, formId);
      return HtmlService.createHtmlOutput('Your form has been added to the dataplatform and will now be polled for new responses indefintely :)!');
    case 'remove':
      if (removeForm(SPREADSHEET, formId)) {
        return HtmlService.createHtmlOutput('Responses will no longer be collected from your form!');
      }
      return HtmlService.createHtmlOutput('Could not find your form, are you sure it\'s been added to the dataplatform already? :)');
    default:
      return HtmlService.createHtmlOutput('That\'s not a valid action! Valid actions are \'add\' or \'remove\'');
  }
}

function onInstall(e) {
  onOpen(e);
}

// Add a custom menu to the active form, including a separator and a sub-menu.
function onOpen(e) {
  FormApp.getUi()
    .createMenu('Dataplattform')
    .addItem('Start collecting data from this form', 'showQuestionsToInclude')
    .addItem('Stop collecting data from this form', 'stopCollectingData')
    .addToUi();
}

function showQuestionsToInclude() {
  var html = HtmlService.createTemplateFromFile('Filters').evaluate();
  FormApp.getUi().showModalDialog(html, 'Start collecting data to the dataplatform.');
}

function getFormQuestions() {
  return FormApp.getActiveForm().getItems()
}

function processForm(formObject) {
  var questionsToInclude = [];
  for (var key in formObject) {
    questionsToInclude.push(formObject[key]);
  }
  result = addToPlatform(questionsToInclude)
  return result;
}

function addToPlatform(questionsToInclude) {
  var formId = FormApp.getActiveForm().getId();

  var isValidForm = getAccessToForm(formId);
  if (!isValidForm) {
    var output = 'We could not find your form :( Please check that the Id is correct and that it is not a quiz!';
  }
  else if (formExists(SPREADSHEET, formId)) {
    var output = 'Your form is already in the platform and can\'t be added again!';
  }
  else {
    writeToSpreadsheet(SPREADSHEET, formId, questionsToInclude);
    var output = 'Your form has been added to the dataplatform and will now be polled for new responses indefintely :)!';
  }
  return output;
}

function stopCollectingData() {
  var formId = FormApp.getActiveForm().getId();

  if (removeForm(SPREADSHEET, formId)) {
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

function getAccessToForm(formId) {
  try {
    var form = FormApp.openById(formId);
    if (form.isQuiz()) {
      return false;
    }
    return true;
  }
  catch (e) {
    return false;
  }
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
  var result = Sheets.Spreadsheets.Values.append(valueRange, spreadsheetId, 'A:C', {
    valueInputOption: 'RAW'
  });
}

function removeForm(spreadsheetId, formId) {
  // Don't allow removal of a form the user does not have access to
  if (formExists(spreadsheetId, formId) && getAccessToForm(formId)) {
    Sheets.Spreadsheets.batchUpdate({
      "requests":
        [{
          "deleteDimension": {
            "range": {
              "dimension": "ROWS",
              "startIndex": row,
              "endIndex": row + 1
            }
          }
        },
        ],
    }, spreadsheetId);
    return true;
  }
  return false;
}

function runAtInterval() {
  readDataFromSpreadsheet(SPREADSHEET)
}

function readDataFromSpreadsheet(spreadsheetId) {
  var response = Sheets.Spreadsheets.Values.get(spreadsheetId, 'A:C');
  var formId;
  var timestamp;
  var questions;
  for (row in response.values) {
    row = parseInt(row);
    // Skip headers
    if (row == 0) {
      continue;
    }
    formId = response.values[row][0];
    timestamp = new Date(response.values[row][1]);
    questionsToInclude = response.values[row][2].split(",");
    postFormDataToIngest(formId, timestamp, questionsToInclude, row + 1);
  }
}

function postFormDataToIngest(formId, timestamp, questionsToInclude, rowToUpdate) {
  var file = DriveApp.getFileById(formId);
  var form = FormApp.openById(formId);
  var formResponses = form.getResponses(timestamp);
  updateSpreadsheetTimestamp(SPREADSHEET, rowToUpdate, new Date());
  
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
          'headers': { 'x-api-key': DATAPLATTFORM_INGEST_APIKEY }
        };
        UrlFetchApp.fetch(DATAPLATTFORM_INGEST_URL, options);
      }
    }
  }
}

function updateSpreadsheetTimestamp(spreadsheetId, row, timestamp) {
  var values = [
    [timestamp]
  ];
  var valueRange = Sheets.newValueRange();
  valueRange.values = values;
  var range = "B" + row;
  var result = Sheets.Spreadsheets.Values.update(valueRange, spreadsheetId, range, {
    valueInputOption: 'RAW'
  });
}