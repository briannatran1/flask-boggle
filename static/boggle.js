"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  const response = await fetch(`/api/new-game`, {
    method: "POST",
  });
  const gameData = await response.json();

  gameId = gameData.gameId;
  let board = gameData.board;

  displayBoard(board);
}

/** Display board
 * Clear contents of board, and rebuild table elements from board
 * object
 */
function displayBoard(board) {
  // $table.remove(); #this messed things up...
  $table.empty();
  let $tbody = $('<tbody></tbody>');
  console.log(board);

  // loop over board and create the DOM tr/td structure
  for (let row of board){
    let $row = $("<tr></tr>");
    for (let cell of row){
      let $cell = $(`<td>${cell}</td>`)
      $row.append($cell);
    }
    $tbody.append($row);
  }
  $table.append($tbody)
}


// Handle form submit:
/**
 * Get submitted word (or non-word), then call requestScore
 * to send onto API
 * @param {*} evt
 */
function handleSubmit(evt){
  evt.preventDefault();
  let $input = $('#wordInput');
  let word = $input.val();
  //console.log('current value is', $input.val());

  // next step: send word to backend!
  // send to: '/api/score-word'
  // should receive: JSON of word
  // gameId is a JS variable of the same name:
  // test_not_on_board = {"gameId": game_id, "word": "DINNERS"}

  let request = {
    'gameId' : gameId,
    'word' : word
  };
  requestScore(request);
}

/**
 * With word and gameId, query api/score-word
 * Display result to DOM:
 * Successful words are added to a list
 * Non-words/words not on board will display an
 * error message.
 * @param {*} request
 */
async function requestScore(request){
  const response = await fetch(`/api/score-word`, {
    method: "POST",
    body: JSON.stringify(request),
    headers: {"Content-type" : "application/json" }
  });

  const scoreData = await response.json();
  const resultMsg = scoreData["result"];

  if (resultMsg === "ok"){ //If a legal word, add to list
    let $wordBullet = $(`<li>${request['word']}</li>`);
    $playedWords.append($wordBullet);
    $message.text("");
  } else { //if not a legal play, add to message
    $message.text(resultMsg);
  }
}

start();
$form.on('submit', handleSubmit);








// //Will need to refactor above
// if (+resultMsg != NaN){
//   //they scored
// } else {

// }