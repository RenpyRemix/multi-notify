# Multiple Notify

#### Note: All you really need are the two files in [The game folder](game). Just one image and a small script file. They can be dropped into a new or existing project and a label called to show an example. (A config setting will need defining to use. Details in the multi_notify.rpy script)
#### Alternatively, just clone the lot as a zip from [The Repository Main Page](https://github.com/RenpyRemix/multi-notify)

Want your players to know when important events happen in your game?
Want to use the `renpy.notify` system with its associated screen Action?

Want it to do more though? Want multiple notifications on screen at once, want them animating in with ATL and animating out after a set time? Want a stored history of previous notifications?

![Image of Multiple Notify](explain_images/multi_notify.gif?raw=true "Sample")

Very basic example image (as gif is not great for displaying this type of animation)

# Multiple Notify in Ren'Py

Not much is required to do this:
  - Tell Ren'Py to use a different function when notifications occur.
  - Use that function to add the new notification to a global list (and prune that list if needed).
  - Show a container screen that displays all the current notifications.
  - Tweak styles and ATL so everything looks great.

The main part of this is adjusting the styles and ATL. The sample here is very basic and could be changed to suit almost any requirements.

### Important Reading:

The overview of the system is more fully explained in [Multi Notify Overview](explain_overview.md)

[![Support me on Patreon](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://www.patreon.com/bePatron?u=19978585)

### Please note:

The way this approach works might not be suitable for complete beginners. It is a basic platform on which to build a system that might grow. As such it will likely require a little knowledge of Ren'Py in order to extend it to your particular needs. 

Though I have tried to explain it as simply as possible, I will not be available to help extend it unless under a paid contract.
Basically, if you want it to do more, you are expected to know enough Ren'Py to handle that yourself (or consider paying someone)
