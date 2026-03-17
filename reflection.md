# 💭 Reflection: Game Glitch Investigator

Guessed 8 (go higher) then 38 then 28 then 18 then 13 then 10 (said go lower every other time) and then 9 (said go higher?) but it still says I lost? ""Out of attempts! The secret was 41. Score: -15"" Not sure what was the actual answer. So, higher/lower suggestion is broken (shows opposite)
New Game button doesnt work
The secret keeps changing, not sure what its even doing
Not sure why the show hint checkbox is really there

"""#Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while #you worked. This is about your process, not trying to sound perfect."""

## 1. What was broken when you started?

(1) New Game button wasn't working, Hint was broken, developer hints were backwards. Higher/lower suggestion is broken (shows opposite)
(2) Was even accepting 0 as guessing value and negative scores
(3) Easy, medium, difficult levels dont seem to work sensibily, (the difficulty=Hard range is set to 1-50 instead of 500) Everything is medium level. Says we have value range of 1 to 100 only but there's no restriction of it in the game
(4) I noticed that when I play the first guess it should say 0th attempt but its saying 1st attempt


Show Hint checkbox randomly changes the number of attempts left and the score as well.
Its adding 5 points for every even number of attempts, no negative numbers
Refactoring needed from app to logic_utils; there are state problems


"""
- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
"""
---

## 2. How did you use AI as a teammate?

Claude
- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

(1) Used Claude 
(2) Example of Bug (1) and (2) above:
Bug found: status is never reset so impossible to play anew game (new game handler) 
Fix that worked: Add st.session_state.status = "playing" to the handler.
Suggested by claude: status change to "playing and cleared history. 
Fix that worked: new game session button worked/fixed
Verified result by testing on streamlit and playing guess iteratively. It was giving 100% correct answers so thats when I chose to decide the bug is fixed - testing_new_game.py

###- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

Scoring logic summary before writing tests:

Win: points = 100 - 10 * (attempt + 1), floored at 10. Attempt 1→80pts, attempt 8→10pts, attempt 9+→10pts (floor kicks in).
Too High, even attempt: +5; odd attempt: −5
Too Low: −5
Unknown outcome: score unchanged

The win formula was awarding points even when it shouldnt floor at 10 and the Too High branch was not correctly distinguishing even vs. odd attempts — both were fixed in update_score().
Running test_new_game.py confirmed that status was never reset to "playing" on new game, which meant the game was stuck after a win/loss until I added st.session_state.status = "playing" to the handler
###

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
Ran test case file. Rechecked on streamlit by trying multiple cases of games playing it personally. When I tried enough games and it gave higher/lower suggestion as it should 100% of the times, I concluded that bug was fixed.

- Describe at least one test you ran (manual or using pytest)  
Manual - tested by trying numbers lower and higher around hint answer. It showed that code was buggy in the sense that it should have said go higher but said go lower instead.


  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
No?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

Every time the user interacted with the app, Streamlit re-ran the entire script from top to bottom, calling random.randint() again. This generated a fresh secret number on each rerun, making it impossible to guess correctly.


- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit re-executes your whole script every time a user clicks a button or types input — like refreshing the page constantly. Session state is a special dictionary that persists values across those reruns, so data you store there survives instead of resetting.


- What change did you make that finally gave the game a stable secret number?

The change that fixed it:
Instead of assigning secret_number = random.randint(...) directly, the number is only generated once and stored in st.session_state. On subsequent reruns, the existing value is reused rather than regenerated.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.


