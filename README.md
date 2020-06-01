## To run
dependencies: you should have Docker installed(I use Docker version 19.03.8)
- `docker-compose up` in the project directory
- http://localhost:15672/#/queues/%2F/test - RabbitMQ management tool(guest:guest)
- http://localhost:8000/matches - api list view
- http://localhost:8000/matches/1 - api list view
- if the queue grows feel free to scale number of workes with `docker-compose scale worker=4`(NB: the actual performance depends on the machine)

## Design desicions
- I made some desicions to make this project interesting for me. In real life everything is discussable.
- The solution tries to follow 'shared nothing' approach
- There are 3 "application" services: backend, worker(consumer) and producer. And two "backing" services: postgres and rabbitmq.
- Configuration between services is shared through environment variables(check .env file)
- Backend doesn't listen(handle) to amqp messages. It gives me a way to scale backend and workers separately.
- Worker is based on a Django management command which gives me a way to reuse the models.
- [Producer](https://github.com/kharandziuk/hypothetical-rank-service/blob/master/backend/matches/management/commands/run-worker.py) generates constant amount of messages every second
- I run a separate command to [setup AMQP topology](https://github.com/kharandziuk/hypothetical-rank-service/blob/master/backend/matches/management/commands/build-amqp-topology.py)
- Worker intentionally doens't handle the possible errors. The idea was to build a service which follow twelve-factor application approach
- In a case of exception it should be printed to [stdout](https://12factor.net/logs), the worker will fail and superviser(in this particular case it's docker-compose with `restart` clause) will restart it. you can observe this behaviour when the worker starts before the actuall exchange created.
- I use django-filter to create filters

## Notes about "Merging events"
In real life I will ask questions beforehand instead of making assumptions or guessing. But for a study project I belive it's ok to make assumptions. So, my assumptions are bellow

- I treat a source as some form of "namespace". My original assumption was: they are used to separate platforms(Nintendo vs Switch)
- If the match/team/tournament have the same id I treat change of the name as rename
- I cast all the ids to string(external_id).
- I update date_start_text for a message with the same match.id. Probably it's wrong, but I didn't figure out something better.
- feel free to check the tests https://github.com/kharandziuk/hypothetical-rank-service/blob/master/backend/tests.py#L11

## Technical depth
- hardcoded names for the queue and the exchange
- some fields are nullable
- only one filter is covered with test
- test suit isn't exchaustive
- separate serializer for list and detail view
- split from_msg for smaller parts
