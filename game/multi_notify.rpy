## To view example in your game add
##
##  call multi_notify_example
##
## somewhere in your running label script



            ###########################################
            #                                         #
            #           To use in your game           #
            #                                         #
            #    Uncomment the following line and     #
            #    maybe delete the example label at    #
            #    the end of this file                 #
            #                                         #
            ###########################################

# define config.notify = add_notify_message


# Global list of notifications
default notify_messages = []

# Duration the full ATL takes
default notify_duration = 4.0

# Max number we store for reviewing in the history screen
default notify_history_length = 20

init python:

    import time

    def add_notify_message(msg=None):

        if not msg:
            return

        global notify_messages

        add_time = time.time()

        # Just in case multiple notifications are added really really 
        # fast, this gives them minorly different time values so they 
        # do not steal displayables meant for other notifications
        if notify_messages and notify_messages[-1][1] >= add_time:

            add_time = notify_messages[-1][1] + 0.01

        notify_messages.append((msg, add_time))

        # just keep notify_history_length number of messages
        notify_messages = notify_messages[-notify_history_length:]

        renpy.show_screen("notify_container")
        renpy.restart_interaction()


    def finish_notify(trans, st, at):

        max_start = time.time() - notify_duration

        if not [k for k in notify_messages if k[1] > max_start]:

            # If the notification list is now empty, hide the screen
            renpy.hide_screen("notify_container")
            renpy.restart_interaction()

        return None


style notify_item_frame:

    background Frame("images/notify_frame_background.png", 10, 10)

    padding (16, 2, 16, 2)
    minimum (20,20)
    # xanchor 0.5


style notify_item_text:

    xsize None 
    align (0.5,0.5) 

    # just standard font specific stuff
    color "#FFF"
    outlines [(abs(2), "#000", abs(0), abs(0))]
    # font ""
    size 20


transform notify_appear():

    yzoom 0.0 alpha 0.5

    linear 1.0 yzoom 1.0 alpha 1.0

    pause 2.0

    linear 1.0 yzoom 0.0 alpha 0.0

    function finish_notify


screen notify_item(msg, use_atl=True):

    style_prefix "notify_item"

    frame:

        if use_atl: # ATL not used for history

            at notify_appear

        # else:
        #     xpos 0.5

        text msg


screen notify_container():

    fixed:

        pos (5, 50)

        vbox:

            xmaximum 250
            spacing 5

            # We index on the time the notification was added as that
            # is unique. Using index helps manage the ATL nicely
            for msg_info index msg_info[1] in notify_messages:

                if msg_info[1] > time.time() - notify_duration:

                    use notify_item(msg_info[0])


screen notify_history():

    viewport:
        area (5, 50, 320, 380)
        # scrollbars "vertical"
        draggable True
        mousewheel True
        yinitial 1.0

        vbox:
            xfill True
            spacing 5

            for msg_info in notify_messages:

                use notify_item(msg_info[0], False)





            ###########################################
            #                                         #
            #    Once you have seen the example you   #
            #    can delete everything below here     #
            #                                         #
            ###########################################



label multi_notify_example:

    scene expression "#AAA"

    $ config.notify = add_notify_message

    $ renpy.notify("First test notification")
    pause
    $ renpy.run(Notify("Second test, using the Notify action"))
    pause
    $ renpy.notify("Third test")

    "Now for a loop of random notifications... (too fast to read fully)"
    extend "\nBetter if you do not click while running."

    $ random_notifications_idx = 0

    while random_notifications_idx < len(random_notifications):

        $ renpy.notify(" ".join(
            random_notifications[random_notifications_idx].split()))

        $ random_notifications_idx += 1

        pause 0.35

    "One more before showing the notify history screen"

    $ renpy.notify(
        ("This is a rather longer notification "
         "to check that longer lines work."))

    pause

    show screen notify_history

    pause

    hide screen notify_history
    
    $ config.notify = renpy.display_notify

    return


default random_notifications = """
    You took 38hp damage.
    Elf needs food badly.
    Building complete!
    You found some evidence.
    You were too late to save the kittens.
    Poison damage 3hp plus fatigue.
    The straps on your chainmail top are almost perished.
    You found a silver key.
    You gained one treasure map.
    The vagabond cleric has healed you fully.
    You see a shiny coin just peeking from the sand.
    """.split('\n')