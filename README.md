# SpriteMaker
Make spritesheet from given images
placement of images is reasonably fast for most usecases.
Memory usage is reasonable
Not for realtime usecases

e.g.

spriteit -algo firstfit -size 512 -inc 128 -path . -o . -padding 0

-algo: [firstfit, spacepart]
