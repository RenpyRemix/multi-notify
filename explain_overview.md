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
The principle part is the for loop and conditional, which cycles through the global `notify_messages` and, if their time value indicates they are currently shown, shows each in its own subscreen.

#### Using `index` in the for loop

Note how that for loop has the index clause in it?
```py
            for msg_info index msg_info[1] in notify_messages:
```
The keyword `index` tells Ren'Py to identify the ATL and state within each iteration of the loop by that value. The value of each index should be unique and hashable, so a long float works nicely and explains why we went to the trouble of making sure they were unique earlier.
When Ren'Py redraws a screen it will reuse old displayables in order to save time creating new surfaces. ATL and state relating to those displayables will also be reused rather than refreshed. This means that if "Notification #1" has long since faded away and Ren'Py decides to reuse that displayable for "Notification #21" it will be using #1's state. So, it would show the new notification at the end of its ATL cycle, faded away and shrunk to nothing, which we certainly do not want.
Using `index` here, with a new unique value that does not match the value of old displayables ensures that each new notification starts its own ATL rather than using an expired/finished one. It makes it so it uses everything fresh.

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
This subscreen shows each individual notification and can also be altered to reflect the style you want in your game.  
I used a style prefix to allow named styles with that prefix to apply to both the `frame:` and the `text`.
One point worth noting is the `use_atl=True` parameter and the `if use_atl:` conditional. Those are so the history screen (which uses these same subscreens) does not fade the notifications away using ATL.  
You could use different subscreens for the history or tweak things any way you like.

## The ATL

Did you note the `at notify_appear` for the `frame:` in the subscreen?  
Did you read the explanation of `index` in the for loop?

If so, you should be able to surmise that when each new notification is shown it starts running an ATL transform.
```py
transform notify_appear():

    yzoom 0.0 alpha 0.5

    linear 1.0 yzoom 1.0 alpha 1.0

    pause 2.0

    linear 1.0 yzoom 0.0 alpha 0.0

    function finish_notify
```
The transform there just makes them grow vertically, fade in from transparent, pause for two seconds while the player reads the info then fade and shrink away.  
You can change that ATL to whatever suits your game best.

The most important part is ending the ATL with the `function finish_notify` which tells it to run the python function after it has finished doing everything else.
```py
    def finish_notify(trans, st, at):

        max_start = time.time() - notify_duration

        if not [k for k in notify_messages if k[1] > max_start]:

            # If the notification list is now empty, hide the screen
            renpy.hide_screen("notify_container")
            renpy.restart_interaction()

        return None
```
Housekeeping; When each notification finishes its ATL we call this function which just checks to see if any notifications are still showing and hides the screen if none are. 


### Navigation:

Back to the main page [Home](README.md)
