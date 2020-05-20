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
This is the function that we told Ren'Py to use instead of the standard `renpy.display_notify` and it behaves slightly differently.

First we use `global` to let Python know we are using the global notify_messages list when we come to change its value.  
Then we determine the time (in float hundredths of a second since Epoch, e.g. 1589982411.26) which we want to be unique for each notification. If that value matches the previous existing one, we add 0.01 to the existing one and use that. This is important and is to make sure each is unique, which comes into play later when we are using ATL.

We add our new notification text and the unique time value to the global notify_messages list and then truncate that list to a maximum length to reflect the `notify_history_length` value.

Like the normal Ren'Py function for notifications, we now show a screen (our container screen in this method) and restart the interaction so it is shown.

We will cover the `finish_notify` ATL function later, after detailing;

## The Screens

```py
screen notify_container():

    fixed:

        pos (0.5, 50)

        vbox:

            spacing 5

            # We index on the time the notification was added as that
            # is unique. Using index helps manage the ATL nicely
            for msg_info index msg_info[1] in notify_messages:

                if msg_info[1] > time.time() - notify_duration:

                    use notify_item(msg_info[0])
```
Just a pretty standard screen that you can alter so it shows things how you want.  
The principle part is the for loop and conditional, which cycles through the global `notify_messages` and, if their time value indicates they are currently shown, shows each in its own subscreen
```py
screen notify_item(msg, use_atl=True):

    style_prefix "notify_item"

    frame:

        if use_atl: # ATL not used for history

            at notify_appear

        else:
            xpos 0.5

        text msg
```



### Navigation:

Back to the main page [Home](README.md)
