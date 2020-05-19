# Multi Notify Overview

So, the first thing we want to do is tell Ren'Py to use our own function whenever notifications appear.
This is done through a config setting which can either be set in an `init python:` block or by using the `define` keyword.

#### Note: In the sample script this is set (and unset) during the label. In practice that is not a good approach and it is only used here so as not to break existing scripts.
```py
# Use the add_notify_message for notifications
define config.notify = add_notify_message
```
At the top of the script are a few default variables which should be understandable with their comments. Then comes an `init python:` block for our functions which starts off by importing the time module.

Next come our functions:
```py
    def add_notify_message(msg=None):

        if not msg:
            return

        global notify_messages

        add_time = time.time()

        # Just in case multiple notifications are added really really 
        # fast, this gives them minorly different time values so do 
        # not steal displayables meant for other notifications
        if notify_messages and notify_messages[-1][1] >= add_time:

            add_time = notify_messages[-1][1] + 0.01

        notify_messages.append((msg, add_time))

        # just keep notify_history_length number of messages
        notify_messages = notify_messages[-notify_history_length:]

        renpy.show_screen("notify_container")
        renpy.restart_interaction()
```
This is the function that we told Ren'Py to use instead of the standard `renpy.display_notify` and it behaves in a similar way.


### Navigation:

Back to the main page [Home](README.md)
