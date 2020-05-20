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

    background Frame("images/notify_frame_background.png", 20, 20)

    padding (16, 2, 16, 2)
    minimum (40, 40)
    xanchor 0.5


style notify_item_text:

    xsize None 
    align (0.5,0.5) 

    # just standard font specific stuff
    color "#444"
    outlines [(abs(2), "#DDD", abs(0), abs(0))]
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

        else:
            xpos 0.5

        text msg


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


screen notify_history():

    viewport:
        xysize (600,380)
        xalign 0.5
        ypos 50
        # scrollbars "vertical"
        draggable True
        mousewheel True
        yinitial 1.0

        vbox:
            xfill True
            spacing 5

            for msg_info in notify_messages:

                use notify_item(msg_info[0], False)


init python:

    # Just for this sample... so it runs

    config.label_overrides['start'] = "multi_notify_example"


label multi_notify_example:

    scene expression "#AAA"

    $ config.notify = add_notify_message

    $ renpy.notify("First test notification")
    pause
    $ renpy.run(Notify("Second test, using the Notify action"))
    pause
    $ renpy.notify("Third test")

    "Now for a loop of Lorem Ipsum... (too fast to read fully)"
    # lorem_ipsum list defaulted at end of script

    $ lorem_idx = 0

    while lorem_idx < len(lorem_ipsum):

        $ renpy.notify(" ".join(lorem_ipsum[lorem_idx].split()))

        $ lorem_idx += 1

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

    if "start" in config.label_overrides:

        $ del config.label_overrides['start']

    return


default lorem_ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing 
    elit. Fusce hendrerit nunc et tellus accumsan eleifend. Nunc maximus 
    ipsum a dictum varius. In bibendum purus vel elit sagittis, ac tincidunt 
    quam posuere. Nullam ornare venenatis lorem sit amet efficitur. 
    Vestibulum commodo in arcu ac pellentesque. Vivamus condimentum lacus nec 
    volutpat bibendum. Sed faucibus vestibulum leo, eu faucibus diam facilisis 
    sit amet. In metus elit, scelerisque at augue id, tincidunt tempor odio. 
    Curabitur rutrum tortor in nulla luctus, vel iaculis eros dictum.
    Vestibulum auctor ex risus, sed vestibulum nisl consectetur mattis. Etiam 
    lacus magna, sodales vitae faucibus sit amet, laoreet nec elit. Etiam non 
    cursus justo. Curabitur nisl eros, imperdiet ac semper nec, lacinia et 
    nibh. Mauris vestibulum eros non ipsum bibendum fringilla. Morbi ut rutrum 
    libero. Phasellus a tempor nisl. Nulla convallis gravida lorem, sagittis 
    volutpat nulla rutrum eu. Vivamus ac nulla volutpat, rutrum tellus eu, 
    finibus eros. Phasellus finibus iaculis libero, eu auctor metus suscipit 
    vel. Etiam tempor lorem ut facilisis porta. Fusce interdum venenatis 
    metus, vel laoreet purus. Curabitur semper consequat fermentum. Maecenas 
    sed eleifend nisl, ac malesuada odio.""".split('.')