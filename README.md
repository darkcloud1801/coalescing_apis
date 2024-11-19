# Coalescing APIs

## Commands
Run Server
> fastapi dev app/main.py

Run Tests
> pytest

## Considerations
While there are only given APIs to retrieve information from, I still wanted to reduce my endpoints response time
by making the calls parallel in case there may be more or some take longer to send a response, etc.

With respect to the coalesce endpoint, it really depends on the target of my endpoint. If this 
world a real world problem, I would want to know who that audience was, if one of the endpoints were
more accurate, why there was different data to begin with, etc. That being said, I made 2 configs.

The first one favors the consumer so it takes the minimum for the copay and oop_max, while maximizing
the remaining_oop_max. The other config took a more mathematical approach - Use the average of the
values returned, if the mode did not exist. I do have a couple of other approaches, that I didnt code
like returning a weighted average, or something that combines the first 2 - return the minimum if the mode does not exist.

That being said, I elected to make this dynamic so I could tweak it some more. So it is possible to customize
the config using built-in math functions. If we wanted something more robust, I would need more time.
