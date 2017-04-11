# Latinissimus
A game designed to help the learning of Latin vocabulary words

Winner of the Viacom Sponsor Prize at HackNYU 2017

[See DevPost Page here](https://devpost.com/software/latinissimus)

## Inspiration
Inspiration
We were two young children in a far, far away high school where we had the opportunity to take Latin. We found learning the language, translating ancient Roman literature, and discovering the Roman culture very interesting. However, we were surprised by the amount of people who thought Latin was a dead and useless language.

So we're bringing Latin alive and out of its grave with Latinissimus, a game revolving around mythology that is designed to help learn Latin vocabulary. We decided to focus on the journey of Odysseus (also known as Ulysses in Latin) from The Odyssey, in which he had to face Polyphemus the Cyclops inside a cave. We hope that Latinissimus will spark interests in Latin and ancient Rome.

## What it does
Latinissimus gives the player a list of Latin vocabularies along with their English translations prior to the start of the game. Then the player is given control of Ulysses, who has the ability to jump to dodge the incoming Cyclopes, or use his sharp wooden dagger to attack the Cyclopes. Each Cyclops has a Latin vocabulary above its head, and the player must avoid the incorrect Cyclopes by jumping, but attack the correct Cyclops. Touching Cyclopes or attacking the wrong Cyclopes will take away lives. When all lives are used up, the game is over.

## How we built it
We used the Pygame module in Python 3 to build Latinissimus. The sprites and art are custom made using a Clip Studio Paint.

## Challenges we ran into
The first challenge we ran into was learning how to use Pygame. The tutorials and documentations seemed really overwhelming, and we felt discouraged already so early on in the process. We were not sure if Latinissimus was an idea we should go forward with, but we decided to stick with it and do our best.

One of the other challenges we ran into was getting the different sprites to detect each other. Even though Pygame simplifies the collision detection between sprites, we wanted to detect collision between specific areas of the sprites from a group, which made the process more difficult.

Another challenge we ran into was randomizing the cyclopes so that each one had its own Latin word attached to it and would enter into the display screen in a systematic manner.

## Accomplishments that we're proud of
We have something that works. There are multiple characters in the game and we can detect the interactions between the characters. We also managed to solve the problems the we mentioned previously while making the game. I’m also happy we have our own art ^3^

## What we learned
The two of us don’t have much experience in making games and we were both interested in learning. We learned how to use Pygame to create games, which was challenging at first because we were not familiar with it, but after watching tutorials and looking through the documentation, we were able to figure a lot of stuff out along the way. It was interesting to learn about the background work that goes into making games that we normally don’t think about.

## What's next for Latinissimus
We want to implement more levels in the future, perhaps with a greater range of horizontal movement for Ulysses and with the ability of Cyclopes to appear from both directions. Also, we want to add more words, not just nouns. We also would like to give the user more myths to choose from instead of just one.
