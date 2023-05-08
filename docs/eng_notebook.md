# Engineering Notebook

## Initial Thoughts
- Apache Hadoop has an implementation of it
- We shouldn't use their package, instead implement our own
- mapreduce implementations usually have a central node and worker nodes
- treat the central node like a server and the workers as replicas or clients?
- seems to be common to use mapreduce for word counting

We decided to use word counting as our primary task

Implementation:
- in Python using gRPC for the server
- treat the workers as clients for now, change this later if we need the server to be able to send requests to workers
- borrow from psets 1 and 3 for server design

## Initial Implementation
- Protos: Task and Empty
    - task has id, task type (map, reduce, idle, or shutdown), data, and a parameter for buckets
    - for now, data = just a filename: we make sure it works locally by splitting up files into tasks first
- Server/Coordinator
    - keep track of number of tasks
    - let client request tasks
    - how to know when client is finished? have them submit a finish task request
- Worker
    - worker has mapper and reducer
    - mapper will read data from assigned files and output intermediate results to a directory
    - mapper just catalogues the words 
    - the words are then outputted into num_reduce_tasks buckets so that they are prepared for the right number of reduce tasks
    - reducer then counts up word frequency and dumps into output files

Presentation Feedback:
- need to implement fault tolerance
- need to run experiments across multiple different numbers of map and reduce tasks
- need to time our program
- need to try chunking data

## Final Implementation
- Data Chunking
    - The original which takes the total number of files, assumes all the files are the same length and thus divides the number of files by the number of tasks
        - shortcomings of this are that some files are likely much longer than others which means we’re not load balancing that well
    - Chunking each file into little pieces: doing a line by line approach and truly doing parallel and equal processing
        - This is technically the best for load balancing and ensuring that each worker is super equally split
        - however, this had a super high overhead (like massive) and communication costs were really high, I anticipate this would be better if the file were actually massive or the actual computation took a long time but given what we’re doing its probably too granular?
    - Chunking each file into larger pieces: the approach that ended up working for us

- Fault Tolerance
    - Have the workers send a "goodbye" request when they go down to the server, so that the server is aware the worker is gone-- we used a similar approach in another pset
    - Have the server keep track of which task ids are assigned to who
    - When a worker down request is received, take the task ids assigned to that worker and put them in a backlog
    - Have each of the task requests draw from the backlog before proceeding with assigning new tasks
    - this works!!

After chunking is implemented, the following things change:
- mapper and reducer now don't write to intermediate files (because these wouldn't be accessible by a server on another machine)
- they just transmit results through protos back to the server
- the server writes its output files

Implemented cross-machine version
- just have the workers indicate the ip address of the server, server runs on 0.0.0.0

Experiments 
- run experiments for a bunch of different values of number of workers, map tasks, and reduce tasks
- run experiments when we use a couple different machines and see the impact
- there may not be a pattern because our data is pretty small