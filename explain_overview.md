# Multi Notify Overview

So, the first thing we want to do is tell Ren'Py to use our own function whenever notifications appear.
This is done through a config setting which can either be set in an `init python:` block or by using the `define` keyword.

#### Note: In the sample script this is set (and unset) during the label. In practice that is not a good approach and it is only used here so as not to break existing scripts.
```py
# Use the add_notify_message for notifications
define config.notify = add_notify_message
```


### Navigation:

Back to the main page [Home](README.md)
