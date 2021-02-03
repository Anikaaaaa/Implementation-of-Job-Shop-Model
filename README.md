# Implementation-of-Job-Shop-Model
In this task, I will implement a job-shop model. The model is a manufacturing
system consisting of n workstations, and at present stations 1, 2, · · · , n consist of ni
, i ∈ {1, · · · , n}
identical machine(s), respectively, as shown in Figure 1. In effect, the system is a network of n
multiserver queues. Assume that jobs arrive at the system with interarrival times that are IID
exponential random variables with mean t hours. There are k types of jobs, and arriving jobs are
of type 1, 2, · · · , k with respective probabilities p1, p2, · · · , pk. A job of type i requires si tasks to
be done, and each task must be done at a specified station and in a prescribed order. For example,
the Figure 1, the sequence for job 1 is 3 → 1 → 2 → 5.If a job arrives at a particular station and finds all machines in that station already busy, the
job joins a single FIFO queue at that station. The time to perform a task at a particular machine is an independent 2-Erlang random variable whose mean r depends on the job type and the stationto which the machine belongs. Use the sum of two exponential random variables each with mean 1/2r to sample from 2-Erlang.

1. Expected average total delay in queue (exclusive of service times) for each job type and the
expected overall average job total delay.
2. Expected average number in each queue and average number of jobs in the whole system
3. Expected average delay in queue for each station

Decision choice: Suppose that all machines cost approximately the same and that the system
has the opportunity to purchase one new machine with an eye toward efficiency improvement. You
have to determine where you will fit the new machine. (You may use the results from the previous
simulation, or run new simulations with the added machine. The latter will incur some penalty.)



<p><img src="https://drive.google.com/drive/folders/1NdAACbmFtoWY115x9XhqZIk6uh_799ZN" alt="Figure 1" width=60% height=50%></p>   | <p><img src="https://drive.google.com/drive/folders/1NdAACbmFtoWY115x9XhqZIk6uh_799ZN" alt="Input" width=60% height=50%></p>
