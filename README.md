# Fotosort

Fotosort is a program for quickly copying or moving pictures from different events into different folders. This sounds quite abstract, so let's look at a few scenarios to spice things up:

## Scenario 1: Random stuff

Assume you have a family, a dog and a kitten. Since they're living with you and they're all doing cute things over and over, you occasionally take out your phone and take a picture. So eventually your phone piles up with pictures of totally unrelated events. Three pictures of your mom climbing a tree. Two pictures of kitty hanging upside down on a chair and looking adorable. A picture of your father laughting. Two pictures of your dog trying to open a can. Random stuff over and over. You know exactly what I'm talking about.

Your *goal* is to sort these pictures into three folders: "family random", "doggy" and "kitty" such that when your niece wants to see how the kitten is doing, you hand her the "kitty" folder and there is no risk of her catching a glimpse of your parents doing weird things.

Your *problem* is that it is extremely painful to move all the pictures by hand into different subfolders. Your file manager only shows tiny previews, forcing you to constantly open and close your picture viewer, and your hand hurts from clasping the mouse after having aimed for target directories for 500 pictures.

Your *solution* is Fotosort. Sounds like a brag, I know. But this is exactly what I made this software for. After spending a minute setting it up, Fotosort knows your three folders (family, doggy and kitty) and you'll spend only a second per picture sending it the right directory at the press of a button. Of course, Fotosort has a trash functionality, allowing you to kick out the bad ones right away. And when you get tired after hundreds of pictures and move or delete a picture accidentally, don't worry: Fotosort's undo functionality is just a Ctrl+Z away.

## Scenario 2: One-timers

Unlike your directories from scenario 1 "family random", "doggy" and "kitty" (which you keep using over months or years), there are events that only take place once. You probably wanna keep them in folders ordered by date, such as "2019_06_18 Hike to the Mount Everest". So for every one of these events, you'll likely create a folder, put the good pictures into it, delete the other pictures and then never add anything to that folder again. It would be pointless to have to create every folder manually, add it to Fotosort, move the pictures into it and remove the folder again. However, Fotosort is equipped for this situation as well:

Your *goal* is to quickly create a folder with the date when the picture was taken (for alphanumerical chronological sorting in any file manager) as well as a short description (for searching in your archive). You want to move some pictures into that folder and will never add anything to the folder again.

Your *problem* is that you need to create the folder manually. The event was a few months back and you don't remember the date, so you go digging in the EXIF data, check the date as recorded by the camera, create the folder and then move the pictures into that folder, sort out the bad ones and navigate back to your main pictures folder for creating the folder for the next event. Pain, pain, pain.

Your *solution* is... yap, you guessed it. At the press of a single keyboard shortcut, Fotosort proposes a suitable name for a target directory based on the capture date it found in the picture. You type in the short description, hit Enter (less than a second elapsed so far!) and have not only the folder created and ready for you, but Fotosort also registeres the new folder as a possible target and you can move pictures into it at the stroke of a single key. Since you won't be using the folder later, Fotosort registers this destination folder as *temporary* and forgets about it when it is closed, sparing you the need of cleaning up the configured target folders too often.

## Scenario 3: Mix

If you have a mix of random and event-style pictures on your phone or camera, don't worry. Thanks to *permanent* target folders (family, dog, kitty) and *temporary* ones (your trip to the Everest), your list of proposed target directories is always down to the relevant ones. Just type a part of a word that occurs in path of your desired directory (e.g. "fam" for family) and the current picture will be moved there as soon as you press return.

# Installing Fotosort

Fotosort is available on PyPi. Type `sudo pip install fotosort` in order to install Fotosort system-wide (or `pip install --user fotosort` to install it inside your user directory). In case your main python version is python2, type `pip3` instead of `pip`.

After creating the configuration file (see below), you can launch Fotosort by typing `fotosort` in the terminal. Make sure the path pip installs to is in your PATH variable.

## Configuration file

Copy the the file `fotosort.yaml.example` to `/home/youruser/.config/fotosort.yaml` and adjust it as follows:

 - If you want to keep the pictures on your camera / phone, set `copy_pictures` to `true`, or set it to `false` if you want to move the files instead.
 - The `extensions` should already work for you. If your camera produces a different file format, add the extension here.
 - Change the list of permanent output directories `perm_output_dirs` such that it contains the directories you often move pictures to, as described in scenario 1. Do not suffix paths with `/`.
 - Put the path to your pictures folder (including the suffix `/`) next to `temp_output_prefix`. This is where temporary output paths will be created, as described in scenario 2.

 You may now launch fotosort.

# Using Fotosort

When Fotosort starts up, it shows `[No Image]`. Hit the menu Fotosort -> Open Folder or press Ctrl+O. Navigate to your camera or phone, where the unsorted pictures are.

You can browse through the photos with Tab and Shift+Tab. The pictures are automatically rotated according to their EXIF data.

In the bottom left corner, you find a combobox listing the configured target paths. You can either select a path from the list by clicking the triangle, or type directly in the text field. The box has an auto-complete feature and the completions are shown to the right of the box. For instance, if you type "rand" with the example configuration, the autocompletion will bring up `/home/user/Pictures/Family Random`. Suggestions are generated on a most-recently-used basis and case-matching results are preferred.

In order to move a picture to the shown target directory, make sure the cursor is placed inside the combobox and hit Enter or Return. In order to move a picture to trash, press Ctrl+D. The picture is not actually deleted, but moved to a folder on the camera or phone, called `FOTOSORT-TRASH`. In order to undo an action, press Ctrl+Z.

## Configuring target directories

Press Ctrl+Shift+T (or use the "Fotosort" menu) to configure target directories. Make sure that every path is on a single line. The paths listed under "Permanent target locations" are saved to the config file when the application is closed and will re-appear on the next launch. The paths under "Temporary target locations" are forgotten as soon as you close Fotosort. In order to make a temporary path permanent or vice versa, simply select the path to change, press Ctrl+X and insert it on a fresh line in the other field using Ctrl+V.

## Quickly creating a temporary target directory

In order to quickly create a temporary target directory as described in scenario 2, press Ctrl+T. The suggested target directory name is generated from the prefix you specified in the config file as well as the capture date found in the current picture. However, this is just a suggestion and you may enter an arbitrary path. Once done, hit Enter and the folder is created (unless it exists already), added to the temporary target directories, and activated in the combobox. When you hit Enter again, the current picture is moved to that folder.

# Contributing

I wrote this program for my own convenience, but there isn't really a reason why you shouldn't be able to adjust it for you own needs. After all, this is FOSS! :-) I'm happy to accept your pull requests.