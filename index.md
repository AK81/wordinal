---
---
<!---
  Copyright (c) Anand Krishnamoorthi
  Licensed under the MIT License.
--->

## WORDle on your termINAL

This is a Javascript implementation of Wordinal - WORDle on your Terminal.
[https://github.com/AK81/wordinal](https://github.com/AK81/wordinal)

## Guess the word

<div style="font-family:Consolas,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New, monospace;">
<div align=center style="font-size:15pt;" id="guesses">

<div>
 <span></span>
 <span></span>
 <span></span>
 <span></span>
 <span></span> 
</div>
<div>
 <span></span>
 <span></span>
 <span></span>
 <span></span>
 <span></span> 
</div>
<div>
 <span></span>
 <span></span>
 <span></span>
 <span></span>
 <span></span> 
</div>
<div>
 <span></span>
 <span></span>
 <span></span>
 <span></span>
 <span></span> 
</div>
<div>
 <span></span>
 <span></span>
 <span></span>
 <span></span>
 <span></span> 
</div>
<div>
 <span></span>
 <span></span>
 <span></span>
 <span></span>
 <span></span> 
</div>
</div>
 
<div id="keyboard">
 <div>
 <span id="Q">Q</span>
 <span id="W">W</span>
 <span id="E">E</span>
 <span id="R">R</span>
 <span id="T">T</span>
 <span id="Y">Y</span>
 <span id="U">U</span>
 <span id="I">I</span>
 <span id="O">O</span>
 <span id="P">P</span> 
</div>

<div>
 <span id="A">A</span>
 <span id="S">S</span>
 <span id="D">D</span>
 <span id="F">F</span>
 <span id="G">G</span>
 <span id="H">H</span>
 <span id="J">J</span>
 <span id="K">K</span>
 <span id="L">L</span>
</div>

<div>
 <span id="Z">Z</span>
 <span id="X">X</span>
 <span id="C">C</span>
 <span id="V">V</span>
 <span id="B">B</span>
 <span id="N">N</span>
 <span id="M">M</span>
 <span id="backspace">&#10007;</span>
 </div>
 
</div>

</div>

<div align=center>
<a align=center href="whatsapp://send?text=This is WhatsApp sharing example using link"       data-action="share/whatsapp/share"  
 target="_blank"> Share to WhatsApp </a>
</div>
 <script type="text/javascript">

 // Length of the solution word.
 const WORD_LENGTH = 5;
 const NUM_GUESSES = WORD_LENGTH + 1;

 function isAlpha(s) {
     if (s.search(/[^A-Za-z]/) != -1)
	 return false
     return true
 }

 // Check whether a word is valid
 function isValid(word) {
     // The word must be of given length
     if (word.length != WORD_LENGTH)
	 return false;

     // The word must contain only alphabet characters.
     if (!isAlpha(word))
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

 const allWords = new Set(solutionWords.concat(guessWords))

 const Grade = {
     Correct : 'lightgreen',
     Misplaced : 'orange',
     Incorrect : 'lightgray'
 }

 function gradeGuess(guess, solution) {
     var grades = Array.from({length:WORD_LENGTH}, _ => null)
     for (var i=0; i < guess.length; ++i){
	 if (guess[i] == solution[i]) {
	     grades[i] = Grade.Correct
	     solution = solution.substring(0, i) + ' ' + solution.substring(i+1, solution.length)
	 }
     }

     for (var i=0; i < guess.length; ++i){
	 if (grades[i] != Grade.Correct) {
	     var ch = guess[i]
	     var pos = solution.indexOf(ch)
	     if (pos != -1) {
		 grades[i] = Grade.Misplaced
		 solution = solution.substring(0, pos) + ' ' + solution.substring(pos+1, solution.length)
	     } else {
		 grades[i] = Grade.Incorrect
	     }
	 }
     }
     return grades
 }

 var guesses = document.getElementById("guesses");

 function clearGuess(row) {
     var div = guesses.children[row];
     div.style.fontSize = "3px"
     div.style.width='fit-content'
     div.style.marginBottom = "5pt"
     for (var c=0; c < WORD_LENGTH; ++c) {
	 div.children[c].style.backgroundColor = '';
	 div.children[c].textContent = '\u2003\u2003\u2003';
	 div.children[c].style.fontSize = "22pt"
	 div.children[c].style.borderRadius='0.25em'
	 div.children[c].style.border='2px solid grey'	 
	 div.children[c].style.textShadow = '1px 1px gray'
     }
 }


 function drawGrade(row, grade) {
     var guessDiv = guesses.children[row];
     for (var c=0; c < WORD_LENGTH; ++c) {
	 setTimeout(function (c) {
	     guessDiv.children[c].style.backgroundColor = grade[c]
	     if (grade[c] == Grade.Incorrect)
		 guessDiv.children[c].style.textShadow = ''
	 },  (c+1)*175, c)
     }
 }

 var keyboard = document.getElementById("keyboard");

 function resetKeyboard() {
     keyboard.style.marginTop = "20pt"
     keyboard.style.fontSize = "20pt"
     keyboard.align = "center"
     keyboard.style.fontSize = "10pt"
     for (var i=0; i < keyboard.children.length; ++i) {
	 var row = keyboard.children[i];
	 row.style.marginBottom="15pt"
	 row.style.fontSize = "8px"
	 for (var j=0; j < row.children.length; ++j) {
	     var key = row.children[j]
	     if (i == 0)
		 key.style.fontSize = "22pt"
	     else
		 key.style.fontSize = "24pt"
	     key.style.border = "1px outset grey"
	     key.style.padding = "2pt"
	     key.style.visibility = "visible"
	     key.style.backgroundColor = 'ghostwhite'
	     key.style.borderRadius =  '1em'
	 }
     }
 }
 
 function updateKeyboard(guess, grade) {
     for (var i=0; i < guess.length; ++i) {
	 if (grade[i] == Grade.Incorrect) {
	     var key = document.getElementById(guess[i])
	     key.style.visibility = "hidden"
	 }	          
     }
     for (var i=0; i < guess.length; ++i) {
	 if (grade[i] == Grade.Correct) {
	     var key = document.getElementById(guess[i])
	     key.style.visibility = "visible"
	     key.style.backgroundColor = grade[i]
	 }	          
     }
     for (var i=0; i < guess.length; ++i) {
	 if (grade[i] == Grade.Misplaced) {
	     var key = document.getElementById(guess[i])
	     key.style.visibility = "visible"
	     key.style.backgroundColor = grade[i]
	 }	          
     }
 }

 var row = 0;
 var col = 0;
 var guess = '';
 var solution = 'UNDEF'
 var newGame = false

 function processKey(key) {
     if (newGame){
	 newGame = false
	 game()
	 return
     }
     if (key.length == 1 && isAlpha(key) && guess.length < WORD_LENGTH) {
	 key = key.toUpperCase()
	 
	 var keybox = document.getElementById(key)
	 if (keybox.style.visibility == 'hidden')
	     return
	 
	 guesses.children[row].children[col].textContent = '\u2003' + key + '\u2003'
	 guess += key
	 if (++col >= WORD_LENGTH) {
	     if (!allWords.has(guess)) {
		 return
	     }
	     var grade = gradeGuess(guess, solution)
	     drawGrade(row, grade)
	     setTimeout(updateKeyboard, (WORD_LENGTH+2)*150, guess, grade)
	     for (var i=0 ; i < WORD_LENGTH; ++i) {
		 if (grade[i] != Grade.Correct) {
		     guess = ''
		     row += 1
		     col = 0;
		     if (row >= NUM_GUESSES) {
			 newGame = true
			 setTimeout(function () {
			     alert("You lost! Word was " + solution);
			 }, (WORD_LENGTH+2)*150)
		     }
		     return;
		 }
	     }

	     newGame = true
	     setTimeout(function () {
		 alert("You Won!")
	     }, (WORD_LENGTH+2)*150)
	 }
     }
     else if((key == 'Backspace' || key == '\u2717') && col > 0) {
	 guesses.children[row].children[--col].textContent = '\u2003\u2003\u2003';
	 guess = guess.substring(0, guess.length-1)
     }
 }
 
 function processKeyEvent(event) {
     var key = event.key;
     processKey(key)
 }

 function processTouchEvent(evt) {
     evt.preventDefault()
     const touches = evt.changedTouches;
     var element = document.elementFromPoint(touches[0].clientX, touches[0].clientY)
     if (keyboard.contains(element))
	 processKey(element.textContent.trim())
 }

 function processMouseUpEvent(evt) {
     evt.preventDefault()
     var element = document.elementFromPoint(evt.clientX, evt.clientY)
     if (keyboard.contains(element))
	 processKey(element.textContent.trim())
 }
 
 function game() {
     row = 0;
     col = 0;
     guess = '';
     solution = solutionWords[Math.floor(Math.random() * solutionWords.length)]

     for (var r=0; r < NUM_GUESSES; ++r)
	 clearGuess(r)

     resetKeyboard()

     document.body.addEventListener('keydown', processKeyEvent)
     document.body.addEventListener('touchend', processTouchEvent)
     document.body.addEventListener('mouseup', processMouseUpEvent)
     guesses.focus()
 }


 game()

 var replayStr = window.location.search
 if (replayStr != "") {
     var words = atob(replayStr.substring(1)).split('|')
     solution = words[0]
     delay = 0
     for (var i=1; i < words.length; ++i) {
	 var word = words[i]
	 for (var j=0; j < word.length; ++j) {
	     setTimeout(processKey, delay, word[j])
	     delay += 300
	 }
	 delay += (WORD_LENGTH + 5) * 150
     }
 }

 </script>
