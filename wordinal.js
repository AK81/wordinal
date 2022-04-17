/*
  Copyright (c) Anand Krishnamoorthi
  Licensed under the MIT License.
*/

// Length of the solution word.
const WORD_LENGTH = 5;

// Check whether a word is valid
function isValid(word) {
    // The word must be of given length
    if (word.length != WORD_LENGTH)
	return false;

    // The word must contain only alphabet characters.
    if(name.search(/[^A-Za-z]/) != -1)
	return false;

    // Otherwise, it is a valid word.
    return true;
}

// Read a file form the server
function readFile(filePath) {
    const xhttp = new XMLHttpRequest();
    xhttp.open("GET", filePath, false);
    xhttp.send();
    return xhttp.responseText;
}

const SOLUTION_WORDS_FILE = "solution_words.txt"
const GUESS_WORDS_FILE = "guess_words.txt"

// Load words from a given file.
function loadWords(filePath) {
    var lines = readFile(filePath).split("\n")
    var words = [];
    lines.forEach( (word) => {
	if (isValid(word))
	    words.push(word.toUpperCase())
    })

    return words
}

var solutionWords = loadWords(SOLUTION_WORDS_FILE).sort()
const guessWords = loadWords(GUESS_WORDS_FILE).sort()

const allWords = new Set(solutionWords + guessWords)

const Grade = {
    Correct : 'Green',
    Misplaced : 'Orange',
    Incorrect : 'Gray'
}

function gradeGuess(guess, solution) {
    var grades = Array.from({length:WORD_LENGTH}, _ => null)
    for (var i=0; i < guess.length; ++i){
	if (guess[i] == solution[i]) {
	    grades[i] = Grade.Correct
	    solution = solution.substring(0, i) + ' ' + solution.substring(i+1)
	}
    }

    for (var i=0; i < guess.length; ++i){
	if (grades[i] != Grade.Correct) {
	    var ch = guess[i]
	    var pos = solution.indexOf(ch)
	    if (pos != -1) {
		grades[i] = Grade.Misplaced
		solution = solution.substring(0, pos) + ' ' + solution.substring(pos+1)
	    } else {
		grades[i] = Grade.Incorrect
	    }
	}
    }
    return grades
}

function drawGuess(row, grade) {
    var guesses = document.getElementById("guesses");
    var guessDiv = document.children[row];
    for (var c=0; c < WORD_LENGTH; ++c) {
	guessDiv.children[c].style.backgroundColor = grade[c]
    }
}

function createGuessArea() {
    document.write("<strong>");
    document.write("<div style=\"margin-top:5pt; font-size:40pt;\"align=center id=\"answer\">");
    for (var i=0; i < WORD_LENGTH + 1; ++i) {
	document.write("<div style=\"margin-bottom:30pt;\">")
	for (var j=0; j < WORD_LENGTH; ++j) {
	    document.write("<span style=\"margin-right:10pt;padding: 8pt; border: 1pt solid black;\">H</span>")
	    document.write()
	}
	document.write("</div>")
    }
    document.write("</div>")
    document.write("</strong>");
}

function test() {
    var tbox = document.getElementById("text");
    tbox.firstChild.nodeValue = gradeGuess('haven', 'never')
}

test()

