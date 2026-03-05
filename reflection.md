# 💭 Reflection: Game Glitch Investigator

Guessed 8 (go higher) then 38 then 28 then 18 then 13 then 10 (said go lower every other time) and then 9 (said go higher?) but it still says I lost? ""Out of attempts! The secret was 41. Score: -15"" Not sure what was the actual answer.
New Game doesnt work
Not sure why the show hint checkbox is really there

"""#Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while #you worked. This is about your process, not trying to sound perfect."""

## 1. What was broken when you started?

New Game button wasnt working, Hint was broken, developer hints were backwards
Easy, medium, difficult levels dont work. Everything is medium level.
Show Hint checkbox randomly changes the number of attempts left and the score as well.

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

For new game handler- bugs found: status is never reset so impossible to play anew game. Fix: Add st.session_state.status = "playing" to the handler.
Suggested: status change to "playing and cleared history. 
Worked: new game session worked/fixed
Verified result by testing on streamlit - testing_new_game.py

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).


Scoring logic summary before writing tests:

Win: points = 100 - 10 * (attempt + 1), floored at 10. Attempt 1→80pts, attempt 8→10pts, attempt 9+→10pts (floor kicks in).
Too High, even attempt: +5; odd attempt: −5
Too Low: −5
Unknown outcome: score unchanged

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
Ran test case file. Rechecked on streamlit byt trying multiple cases myself.

- Describe at least one test you ran (manual or using pytest)  
Manual - tested by trying numbers lower and higher around hint answer. It showed that code was buggy in the sense that it should have said go higher but said go lower instead.

  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
No?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.


