# Bash Keyboard Shortcuts

Bash is an incredibly powerful shell, and being proficient with it can make a massive difference in your productivity. Small tips and tricks can sometimes make a big difference in how you work. The shortcuts I've listed below deal mostly with what is actually readline functionality and so they may work in many other command line situations and programs. This is not a complete list but just some of my favorites.

## Commands for Moving

These are the basics. The real stand outs here are moving around the line by word - it can save you plenty of time compared to navigating only with the arrow keys.

- **beginning-of-line (Ctrl-a)** - Move to the start of the current line.
- **end-of-line (Ctrl-e)** - Move to the end of the line.
- **forward-char (Ctrl-f)** - Move forward a character.
- **backward-char (Ctrl-b)** - Move back a character.
- **forward-word (Meta-f)** - Move forward to the end of the next word. Words are composed of alphanumeric characters (letters and digits).
- **backward-word (Meta-b)** - Move back to the start of the current or previous word. Words are composed of alphanumeric characters (letters and digits).
- **clear-screen (Ctrl-l)** - Clear the screen leaving the current line at the top of the screen. With an argument, refresh the current line without clearing the screen.

## Commands for Manipulating the History

These can be lifesavers. Especially if you're running the same or similar commands over and over. For example Ctrl-o is so much faster than pressing 'up' a bunch of times, then pressing 'up' the same number of times to get to the next command in the sequence - use Ctrl-o, or maybe even a keyboard macro.

- **accept-line (Newline, Return)** - Accept the line regardless of where the cursor is. If this line is non-empty, add it to the history list according to the state of the HISTCONTROL variable. If the line is a modified history line, then restore the history line to its original state.
- **previous-history (Ctrl-p)** - Fetch the previous command from the history list, moving back in the list.
- **next-history (Ctrl-n)** - Fetch the next command from the history list, moving forward in the list.
- **beginning-of-history (Meta-<)** - Move to the first line in the history.
- **end-of-history (Meta->)** - Move to the end of the input history, i.e., the line currently being entered.
- **reverse-search-history (Ctrl-r)** - Search backward starting at the current line and moving 'up' through the history as necessary. This is an incremental search.
- **forward-search-history (Ctrl-s)** - Search forward starting at the current line and moving 'down' through the history as necessary. This is an incremental search.
- **yank-nth-arg (Meta-Ctrl-y)** - Insert the first argument to the previous command (usually the second word on the previous line) at point. With an argument n, insert the nth word from the previous command (the words in the previous command begin with word 0). A negative argument inserts the nth word from the end of the previous command.
- **yank-last-arg (Meta-., Meta-_)** - Insert the last argument to the previous command (the last word of the previous history entry). With an argument, behave exactly like yank-nth-arg. Successive calls to yank-last-arg move back through the history list, inserting the last argument of each line in turn.
- **shell-expand-line (Meta-Ctrl-e)** - Expand the line as the shell does. This performs alias and history expansion as well as all of the shell word expansions.
- **history-expand-line (Meta-^)** - Perform history expansion on the current line.
- **insert-last-argument (Meta-., Meta-_)** - A synonym for yank-last-arg.
- **operate-and-get-next (Ctrl-o)** - Accept the current line for execution and fetch the next line relative to the current line from the history for editing. Any argument is ignored.
- **edit-and-execute-command (Ctrl-x Ctrl-e)** - Invoke an editor on the current command line, and execute the result as shell commands. Bash attempts to invoke $VISUAL, $EDITOR, and emacs as the editor, in that order.

## Commands for Changing Text

- **delete-char (Ctrl-d)** - Delete the character at point. If point is at the beginning of the line, there are no characters in the line, and the last character typed was not bound to delete-char, then return EOF.
- **quoted-insert (Ctrl-q, Ctrl-v)** - Add the next character typed to the line verbatim. This is how to insert characters like Ctrl-q, for example.
- **tab-insert (Ctrl-v TAB)** - Insert a tab character.
- **transpose-chars (Ctrl-t)** - Drag the character before point forward over the character at point, moving point forward as well. If point is at the end of the line, then this transposes the two characters before point. Negative arguments have no effect.
- **transpose-words (Meta-t)** - Drag the word before point past the word after point, moving point over that word as well. If point is at the end of the line, this transposes the last two words on the line.
- **upcase-word (Meta-u)** - Uppercase the current (or following) word. With a negative argument, uppercase the previous word, but do not move point.
- **downcase-word (Meta-l)** - Lowercase the current (or following) word. With a negative argument, lowercase the previous word, but do not move point.
- **capitalize-word (Meta-c)** - Capitalize the current (or following) word. With a negative argument, capitalize the previous word, but do not move point.

## Killing and Yanking

Killing and yanking can be a tremendous time saver over copy/paste with the mouse.

- **kill-line (Ctrl-k)** - Kill the text from point to the end of the line.
- **backward-kill-line (Ctrl-x Backspace)** - Kill backward to the beginning of the line.
- **unix-line-discard (Ctrl-u)** - Kill backward from point to the beginning of the line. The killed text is saved on the kill-ring.
- **kill-word (Meta-d)** - Kill from point to the end of the current word, or if between words, to the end of the next word. Word boundaries are the same as those used by forward-word.
- **backward-kill-word (Meta-Backspace)** - Kill the word behind point. Word boundaries are the same as those used by backward-word.
- **shell-kill-word (Meta-d)** - Kill from point to the end of the current word, or if between words, to the end of the next word. Word boundaries are the same as those used by shell-forward-word.
- **shell-backward-kill-word (Meta-Backspace)** - Kill the word behind point. Word boundaries are the same as those used by shell-backward-word.
- **unix-word-Backspace (Ctrl-w)** - Kill the word behind point, using white space as a word boundary. The killed text is saved on the kill-ring.
- **delete-horizontal-space (Meta-\)** - Delete all spaces and tabs around point.

## Completing

There are some powerful completing shortcuts.

- **complete (TAB)** - Attempt to perform completion on the text before point. Bash attempts completion treating the text as a variable (if the text begins with $), username (if the text begins with ~), hostname (if the text begins with @), or command (including aliases and functions) in turn. If none of these produces a match, filename completion is attempted.
- **possible-completions (Meta-?)** - List the possible completions of the text before point.
- **insert-completions (Meta-*)** - Insert all completions of the text before point that would have been generated by possible-completions.
- **complete-filename (Meta-/)** - Attempt filename completion on the text before point.
- **possible-filename-completions (Ctrl-x /)** - List the possible completions of the text before point, treating it as a filename.
- **complete-username (Meta-~)** - Attempt completion on the text before point, treating it as a username.
- **possible-username-completions (Ctrl-x ~)** - List the possible completions of the text before point, treating it as a username.
- **complete-variable (Meta-$)** - Attempt completion on the text before point, treating it as a shell variable.
- **possible-variable-completions (Ctrl-x $)** - List the possible completions of the text before point, treating it as a shell variable.
- **complete-hostname (Meta-@)** - Attempt completion on the text before point, treating it as a hostname.
- **possible-hostname-completions (Ctrl-x @)** - List the possible completions of the text before point, treating it as a hostname.
- **complete-command (Meta-!)** - Attempt completion on the text before point, treating it as a command name. Command completion attempts to match the text against aliases, reserved words, shell functions, shell builtins, and finally executable filenames, in that order.
- **possible-command-completions (Ctrl-x !)** - List the possible completions of the text before point, treating it as a command name.
- **dynamic-complete-history (Meta-TAB)** - Attempt completion on the text before point, comparing the text against lines from the history list for possible completion matches.
- **complete-into-braces (Meta-{)** - Perform filename completion and insert the list of possible completions enclosed within braces so the list is available to the shell (see Brace Expansion above).

## Keyboard Macros

These can be useful if you're running the same few commands over and over. For example, when I'm working in my IDE and then want to run some tests, I can quickly create a macro the first time I run my couple of commands to clean, build, and run the tests. When I want to run that sequence again it's very quick, and doesn't require hunting/searching through the history.

- **start-kbd-macro (Ctrl-x ()** - Begin saving the characters typed into the current keyboard macro.
- **end-kbd-macro (Ctrl-x ))** - Stop saving the characters typed into the current keyboard macro and store the definition.
- **call-last-kbd-macro (Ctrl-x e)** - Re-execute the last keyboard macro defined, by making the characters in the macro appear as if typed at the keyboard.

## Miscellaneous

- **prefix-meta (ESC)** - Metafy the next character typed. ESC f is equivalent to Meta-f.
- **undo (Ctrl-_, Ctrl-x Ctrl-u)** - Incremental undo, separately remembered for each line.
- **tilde-expand (Meta-&)** - Perform tilde expansion on the current word.
- **set-mark (Ctrl-@, Meta-)** - Set the mark to the point. If a numeric argument is supplied, the mark is set to that position.
- **exchange-point-and-mark (Ctrl-x Ctrl-x)** - Swap the point with the mark. The current cursor position is set to the saved position, and the old cursor position is saved as the mark.
- **character-search (Ctrl-])** - A character is read and point is moved to the next occurrence of that character. A negative count searches for previous occurrences.
- **character-search-backward (Meta-Ctrl-])** - A character is read and point is moved to the previous occurrence of that character. A negative count searches for subsequent occurrences.
- **insert-comment (Meta-#)** - Without a numeric argument, the value of the readline comment-begin variable is inserted at the beginning of the current line. If a numeric argument is supplied, this command acts as a toggle: if the characters at the beginning of the line do not match the value of comment-begin, the value is inserted, otherwise the characters in comment-begin are deleted from the beginning of the line. In either case, the line is accepted as if a newline had been typed. The default value of comment-begin causes this command to make the current line a shell comment. If a numeric argument causes the comment character to be removed, the line will be executed by the shell.
- **display-shell-version (Ctrl-x Ctrl-v)** - Display version information about the current instance of bash.
