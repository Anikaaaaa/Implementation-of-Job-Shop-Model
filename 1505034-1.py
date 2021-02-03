import heapq
import random
from builtins import print
import matplotlib.pyplot as plt
import numpy as np


MAX_TIME = 8
class Params:
    def __init__(self):

        self.No_of_stations = 0  # Number of stations
        self.Num_of_machines_each_station = []
        self.inter_arrival_time_for_jobs = 0.0
        self.num_job_type = 0
        self.job_probablities = []
        self.num_of_stations = []
        self.job_station_routing = []
        self.mean_service_time = []
        self.a = []



def taking_input(params):
    f = open('input.txt')
    lines = f.readlines()
    total_lines = len(lines)
    params.No_of_stations = int(lines[0])
    #print(params.No_of_stations)

    i = 0
    for word in lines[1].split():
        params.Num_of_machines_each_station.append(int(word))
        #print(params.Num_of_machines_each_station[i])
        i += 1

    params.inter_arrival_time_for_jobs = float(lines[2])
    #print(params.inter_arrival_time_for_jobs)

    params.num_job_type = int(lines[3])
    #print((params.num_job_type))

    i = 0
    for word in lines[4].split():
        params.job_probablities.append(float(word))
        #print(params.job_probablities[i])
        i += 1

    i = 0
    for word in lines[5].split():
        params.num_of_stations.append(int(word))
        #print(params.num_of_stations[i])
        i += 1

    j = 0
    while j < params.num_job_type:
        params.job_station_routing.append([])
        params.mean_service_time.append([])
        j += 1

    j = 0
    while j < params.num_job_type:
        i = 0
        for word in lines[6 + (j * 2)].split():
            params.job_station_routing[j].append(int(word))
            #print(params.job_station_routing[j][i])
            i += 1
        i = 0
        for word in lines[7 + (j * 2)].split():
            params.mean_service_time[j].append(float(word))
            #print(params.mean_service_time[j][i])
            i += 1

        j += 1

    f.close()
    i=1
    while i<= params.num_job_type:
        params.a.append(i)
        i+=1


class States:
    def __init__(self):
        # States
        self.work_station_queue = []
        self.work_station_queue_jobType = []
        self.work_station_queue_currentStation = []
        self.work_station_machine = []
        self.no_of_occurances_this_type_job =[]
        self.occupied_machine = []
        self.station_delays = []
        self.job_type_delays = []
        self.customer_served_by_station = []
        self.area_num_in_queues = []
        self.current_amount_jobs = 0
        self.area_num_jobs = 0.0
        self.delay_each_job_type = []
        self.avg_q_delays = []
        self.avg_q_lengths =[]
        self.avg_job_delay = []
        self.job_served_each_type = []
        self.station_served = []
        self.overall_job_delay = 0.0
        self.No_of_jobs_this_type = []
        self.each_type_job = []
        self.avg_num_jobs = 0.0

        self.queue = []


        # Declare other states variables that might be needed
        self.server_status = 0
        self.delay = 0.0
        self.length = 0
        self.time_since_last_event = 0.0
        self.time_of_last_event = 0.0
        self.total_time_served = 0.0
        self.service_time=0.0
        self.no_of_cust_delayed = 0
        self.num_in_queue = 0
        self.area_num_in_queue = 0.0
        self.num_waited = 0
        self.servers_status = []
        #self.service_time = 0
        self.wait_time = 0
        #self.busy=1
        # Statistics
        self.util = 0.0
        self.avgQdelay = 0.0
        self.avgQlength = 0.0
        self.served = 0
        self.QueueLimit = 1000
        self.num_in_q=0
        self.no_of_q_avilable = 0




    def update(self, sim, event):
        # Complete this function
        self.time_since_last_event =  event.eventTime - self.time_of_last_event
        self.time_of_last_event = event.eventTime
        self.total_time_served += ( self.server_status * self.time_since_last_event )
        #self.total_time_served =
        #self.area_num_in_queue += ( self.num_in_q * self.time_since_last_event)
        i=0
        while i< sim.params.No_of_stations:
            self.area_num_in_queues.append(0.0)
            self.avg_q_delays.append(0.0)
            self.avg_q_lengths.append(0.0)
            i+=1

        i = 0
        while i < sim.params.No_of_stations:
            self.area_num_in_queues[i] += self.time_since_last_event * len(self.work_station_queue[i]) ########## += naki =
            i += 1

        i = 0
        while i < sim.params.No_of_stations:
            self.area_num_in_queue += float(self.area_num_in_queues[i])
            i += 1

        if sim.simclock > 0:
            i = 0
            while i < sim.params.No_of_stations:
                self.avg_q_lengths[i] = self.area_num_in_queues[i]/sim.simclock
                i += 1

        self.area_num_jobs += self.time_since_last_event * self.current_amount_jobs



        i = 0
        while i < sim.params.num_job_type:
            self.delay_each_job_type.append(0.0)
            i += 1

        i = 0
        while i < sim.params.num_job_type:
            #self.delay_each_job_type[i] = self.job_type_delays[i]/sim.params.num_job_type ########## AVG
            #if self.job_served_each_type[i] > 0:
             #   self.delay_each_job_type[i] = self.job_type_delays[i] / self.job_served_each_type[i]

            ########## im changing this
            #if self.No_of_jobs_this_type[i] > 0 :
             #   self.delay_each_job_type[i] = self.job_type_delays[i] / self.No_of_jobs_this_type[i]
            if self.each_type_job[i] > 0:
                self.delay_each_job_type[i] = self.job_type_delays[i] / self.each_type_job[i]

            i += 1

        ##-------------------overall delay korte hbe
        i = 0
        while i < sim.params.num_job_type:
            if self.job_served_each_type[i] > 0:
                self.avg_job_delay[i]=self.job_type_delays[i]/self.job_served_each_type[i]

            i+=1
        i = 0
        while i < sim.params.num_job_type:
            #print("job prb....  %lf" %sim.params.job_probablities[i])
            self.overall_job_delay += (sim.params.job_probablities[i] * self.delay_each_job_type[i])
            i += 1


        i = 0
        while i < sim.params.No_of_stations :
            if self.customer_served_by_station[i] > 0:
                ################## ekhane thik korbo queue length thik nah ashle
                self.avg_q_delays[i] = self.station_delays[i]/self.customer_served_by_station[i]
                ############## im redoing prev one and commenting this
            #if self.station_served[i] > 0 :
                #self.avg_q_delays[i] = self.station_delays[i] / self.station_served[i]
            i+=1

        i = 0
        while i < sim.params.No_of_stations:
            self.served += self.customer_served_by_station[i]
            i += 1

        i = 0
        while i < sim.params.No_of_stations:
            self.delay += self.station_delays[i]
            i += 1

    def finish(self, sim):
        self.avg_num_jobs = self.area_num_jobs/sim.simclock
        self.avgQdelay = self.delay / self.served
        self.avgQlength = self.area_num_in_queue / sim.simclock

        #self.util = self.total_time_served / sim.simclock


    def printResults(self,sim):
        i = 0
        while i < sim.params.num_job_type:
            print('served job type %d = %d'%((i+1),self.job_served_each_type[i]))
            i += 1
        print('MMk Total customer served: %d' % (self.served))
        print('MMk Average queue length: %lf' % (self.avgQlength))
        print('MMk Average customer delay in queue: %lf' % (self.avgQdelay))
        print('Overall avg Job delay %lf' %(self.overall_job_delay))
        print("Avg total delay for each jobs ")
        i=0
        while i < sim.params.num_job_type:
            print(i+1 , self.delay_each_job_type[i])
            i+=1

        i = 0
        while i < sim.params.No_of_stations:
            print(i+1 , self.avg_q_lengths[i] , self.avg_q_delays[i])
            i += 1

    def printResults1(self, sim):
        # DO NOT CHANGE THESE LINES
        print('MMk Results: lambda = %lf, mu = %lf, k = %d' % (sim.params.lambd, sim.params.mu, sim.params.k))
        print('MMk Total customer served: %d' % (self.served))
        print('MMk Average queue length: %lf' % (self.avgQlength))
        print('MMk Average customer delay in queue: %lf' % (self.avgQdelay))
        print('MMk Time-average server utility: %lf' % (self.util))

    def getResults(self, sim):
        return (self.avgQlength, self.avgQdelay, self.util)

    def AnalyticalResults(self, sim):
        print('MMk AnalyticalResults  : lambda = %lf, mu = %lf, k = %d' % (sim.params.lambd, sim.params.mu, sim.params.k))
        #print('MMk Total customer served: %d' % (self.served))
        aql=0
        adq=0
        if sim.params.mu != sim.params.lambd :
            aql = float((sim.params.lambd ** 2) / (sim.params.mu * (sim.params.mu - sim.params.lambd)))
            adq = float(sim.params.lambd / (sim.params.mu * (sim.params.mu - sim.params.lambd)))
        uf = float(sim.params.lambd / sim.params.mu)
        print('MMk Average queue length: %lf' % (aql))
        print('MMk Average customer delay in queue: %lf' % (adq))
        print('MMk Time-average server utility: %lf' % (uf))

    # Write more functions if required


class Event:
    def __init__(self, sim):
        self.eventType = None
        self.sim = sim
        self.eventTime = None
        self.job_type = None
        self.current_station = None


    def process(self, sim):
        raise Exception('Unimplemented process method for the event!')

    def __repr__(self):
        return self.eventType



class StartEvent(Event):
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'START'
        self.sim = sim
        #self.job_type=job_type


    def process(self, sim):

        Time = sim.simclock + random.expovariate(1/sim.params.inter_arrival_time_for_jobs)
        #job_type = int(np.random.choice(sim.params.a,1,sim.params.job_probablities))
        job_type = int(np.random.choice(sim.params.a, 1, p=[0.3,0.5,0.2]))

        #print('job type %d' %job_type)
        sim.states.No_of_jobs_this_type[job_type-1] += 1
        station = sim.params.job_station_routing[job_type-1][0]
        #print('Scheduling Arrival event at start event at %f' %self.eventTime)
        sim.scheduleEvent(ArrivalEvent ( Time,sim ,job_type,station))
        sim.scheduleEvent(ExitEvent(MAX_TIME, sim))

class ExitEvent(Event):
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'EXIT'
        self.sim = sim

    def process(self, sim):
        # Complete this function
        None


class ArrivalEvent(Event):
    def __init__(self, eventTime, sim,job_type,current_station):
        self.eventTime = eventTime
        self.eventType = 'ARRIVAL'
        self.sim = sim
        self.job_type = job_type
        self.current_station = current_station


    def process(self, sim):
        #arrrval_time = sim.simclock + random.expovariate(sim.params.lambd)
        #sim.scheduleEvent(ArrivalEvent(arrrval_time , sim))
        if self.current_station == sim.params.job_station_routing[self.job_type - 1][0]:
            sim.states.current_amount_jobs += 1
            sim.states.no_of_occurances_this_type_job[self.job_type - 1] +=  1
            Time = sim.simclock + random.expovariate(1/sim.params.inter_arrival_time_for_jobs)
            #type_job = int(np.random.choice(sim.params.a, 1, sim.params.job_probablities))
            type_job = int(np.random.choice(sim.params.a, 1, p=[0.3, 0.5, 0.2]))

            sim.states.No_of_jobs_this_type[type_job - 1] +=1
            print('job type %d' % type_job)
            station = sim.params.job_station_routing[type_job - 1][0]
            # print('Scheduling Arrival event at start event at %f' %self.eventTime)
            sim.scheduleEvent(ArrivalEvent(Time, sim, type_job, station))

        no_machines_in_station = sim.params.Num_of_machines_each_station[self.current_station - 1]
        #print('No of machines %d' %no_machines_in_station)
        i = 0
        pos_of_free_machine = 100
        while i < no_machines_in_station:
            if sim.states.work_station_machine[self.current_station - 1][i] == 0:
                #print(self.current_station,i)
                pos_of_free_machine = i
                break
            else:
                i += 1

        if pos_of_free_machine != 100:

            total_station_routing_this_job = len(sim.params.job_station_routing[self.job_type - 1])
            index_station = 0
            i = 0
            while i < total_station_routing_this_job:
                if sim.params.job_station_routing[self.job_type - 1][i] == self.current_station:
                    index_station = i
                    break
                else:
                    i += 1

            sim.states.work_station_machine[self.current_station - 1][pos_of_free_machine] = 1
            departure_time = sim.simclock + random.expovariate((sim.params.mean_service_time[self.job_type - 1][index_station])/2)+random.expovariate((sim.params.mean_service_time[self.job_type - 1][index_station])/2)
            sim.states.occupied_machine[self.current_station - 1][pos_of_free_machine] = float(departure_time)
            sim.states.station_delays[self.current_station - 1] +=  0.0
            sim.states.customer_served_by_station[self.current_station - 1] += 1
            sim.scheduleEvent(DepartureEvent(departure_time, sim , self.job_type,self.current_station))
        else:
            sim.states.work_station_queue[self.current_station - 1].append(sim.simclock)
            sim.states.work_station_queue_jobType[self.current_station - 1].append(self.job_type)
            sim.states.work_station_queue_currentStation[self.current_station - 1].append(self.current_station)


class DepartureEvent(Event):
    def __init__(self, eventTime, sim,job_type,current_station):
        self.eventTime = eventTime
        self.eventType = 'DEPARTURE'
        self.sim = sim
        self.job_type = job_type
        self.current_station = current_station

    def process(self, sim):
        #sim.states.customer_served_by_station[self.current_station-1] += 1
        sim.states.each_type_job[self.job_type-1] += 1
        sim.states.station_served[self.current_station - 1] +=1
        total_station_routing_this_job = len(sim.params.job_station_routing[self.job_type-1])
        index_station = 0
        i=0
        while i < total_station_routing_this_job :
            if sim.params.job_station_routing[self.job_type-1][i] == self.current_station:
                index_station=i
                break
            else:
                i += 1

        pos_of_occupied_machine = 100
        i = 0
        while i < sim.params.Num_of_machines_each_station[self.current_station-1]:
            if self.eventTime == sim.states.occupied_machine[self.current_station-1][i]:
                pos_of_occupied_machine = i
                #print("pos")
                #print(pos_of_occupied_machine)
                break
            else:
                i += 1
        print("pos")
        print(pos_of_occupied_machine)

        if index_station == (total_station_routing_this_job - 1) :
            sim.states.current_amount_jobs -= 1
            sim.states.job_served_each_type[self.job_type-1] += 1
            print("This is the final station")

        else:
        #elif pos_of_occupied_machine != 100:
            #Time = sim.simclock + random.expovariate(sim.params.)
            #################### time ta thik korte hbe
            #Time = sim.simclock
            Time = self.eventTime
            station = sim.params.job_station_routing[self.job_type - 1][index_station + 1]
            # print('Scheduling Arrival event at start event at %f' %self.eventTime)
            sim.scheduleEvent(ArrivalEvent(Time, sim, self.job_type, station))
        if pos_of_occupied_machine != 100:
            queue_len = len(sim.states.work_station_queue[self.current_station-1])
            if queue_len > 0:
                #time = sim.states.work_station_queue[self.current_station-1].pop(0)
                #sim.states.station_delays[self.current_station-1] = sim.states.station_delays[self.current_station-1] + (sim.simclock - time)
                #sim.states.job_type_delays[self.job_type-1] = sim.states.job_type_delays[se]
                sim.states.customer_served_by_station[self.current_station - 1] += 1
                type_job = sim.states.work_station_queue_jobType[self.current_station-1].pop(0)
                this_station = sim.states.work_station_queue_currentStation[self.current_station-1].pop(0)
                sim.states.work_station_machine[self.current_station - 1][pos_of_occupied_machine] = 1
                time = sim.states.work_station_queue[self.current_station - 1].pop(0)
                sim.states.station_delays[self.current_station - 1] += (sim.simclock - time)
                sim.states.job_type_delays[type_job - 1] += (sim.simclock - time)
                idx = 0
                i = 0
                total_station_routing_this_job_1 = len(sim.params.job_station_routing[type_job - 1])
                while i < total_station_routing_this_job_1:
                    if sim.params.job_station_routing[type_job - 1][i] == this_station:
                        idx = i
                        break
                    else:
                        i += 1

                time_departure = sim.simclock + random.expovariate((sim.params.mean_service_time[type_job - 1][idx]) / 2) + random.expovariate((sim.params.mean_service_time[type_job - 1][idx]) / 2)
                sim.states.occupied_machine[self.current_station - 1][pos_of_occupied_machine] = float(time_departure)
                sim.scheduleEvent(DepartureEvent(time_departure, sim, type_job, self.current_station))

            else:
                sim.states.work_station_machine[self.current_station - 1][pos_of_occupied_machine] = 0


class Simulator:
    def __init__(self, seed):
        self.eventQ = []
        self.simclock = 0
        self.seed = seed
        self.states = None
        self.params = None

    def initialize(self):
        self.simclock = 0
        self.scheduleEvent(StartEvent(0, self))


    def configure(self, params , states):
        self.params = params
        self.states = states

    def now(self):
        return self.simclock

    def scheduleEvent(self, event):
        heapq.heappush(self.eventQ, (event.eventTime, event))

    def run(self):
        random.seed(self.seed)
        self.initialize()
        i=0
        while i < self.params.No_of_stations:
            self.states.work_station_queue.append([])
            self.states.work_station_queue_currentStation.append([])
            self.states.work_station_queue_jobType.append([])
            self.states.work_station_machine.append([])
            self.states.occupied_machine.append([])
            self.states.station_delays.append(0.0)
            self.states.customer_served_by_station.append(0)
            self.states.station_served.append(0)
            i+=1

        i=0
        while i < self.params.No_of_stations:
            j=0
            while j<self.params.Num_of_machines_each_station[i]:
                self.states.work_station_machine[i].append(0)
                self.states.occupied_machine[i].append(0)
                j += 1
            i+=1

        i=0
        while i<self.params.num_job_type:
            self.states.no_of_occurances_this_type_job.append(0)
            self.states.job_type_delays.append(0.0)
            self.states.avg_job_delay.append(0.0)
            self.states.job_served_each_type.append(0)
            self.states.No_of_jobs_this_type.append(0)
            self.states.each_type_job.append(0)
            i+=1

        while len(self.eventQ) > 0:


            time, event = heapq.heappop(self.eventQ)
            if event.eventType == 'EXIT':
                break

            if self.states != None:
                self.states.update(self, event)

            print(event.eventTime, 'Event', event)
            self.simclock = event.eventTime
            event.process(self)
        self.states.finish(self)


    def printResults(self):
        self.states.printResults(self)
        #self.states.AnalyticalResults(self)

    def getResults(self):
        return self.states.getResults(self)


def task11():
    params = Params()
    taking_input(params)
    seed = 101
    sim = Simulator(seed)
    sim.configure(params, States())

    sim.run()
    sim.printResults()



def task1():
    params = Params()
    taking_input(params)
    total_run = 30
    avg_total_delay_in_queue = []
    avg_number_in_queue = []
    avg_delay_in_queue = []
    a = []
    overall_job_delay = 0.0
    avg_num_jobs1 = 0.0
    i = 0
    #print("before")
    #print(params.num_job_type)
    while i < params.num_job_type:
        avg_total_delay_in_queue.append(0.0)
        a.append(0.0)
        i += 1

    i = 0
    while i < params.No_of_stations:
        avg_number_in_queue.append(0.0)
        avg_delay_in_queue.append(0.0)
        i += 1

    i = 0
    while i < total_run :

        seed = 101
        sim = Simulator(seed)
        sim.configure(params, States())

        sim.run()
        j = 0
        #print("ddcdcdcsdcjnjc")
        #print(sim.params.num_job_type)
        while j < sim.params.num_job_type:
            avg_total_delay_in_queue[j] += sim.states.delay_each_job_type[j]
            a[j] += sim.states.avg_job_delay[j]
            j += 1

        overall_job_delay += sim.states.overall_job_delay
        avg_num_jobs1 += sim.states.avg_num_jobs
        k = 0
        while k < sim.params.No_of_stations:
            avg_number_in_queue[k] += sim.states.avg_q_lengths[k]
            avg_delay_in_queue[k] += sim.states.avg_q_delays[k]

            k+=1
        p = 0
        while p < sim.params.num_job_type:
            #print("No of job served %d type is %d" % ((p + 1), sim.states.job_served_each_type[p]))
            p += 1

        i += 1

    j = 0
    print()
    while j < sim.params.num_job_type:
        avg_total_delay_in_queue[j] = avg_total_delay_in_queue[j] / total_run
        print(" average total delay in the queue for %d job %lf " %((j+1),avg_total_delay_in_queue[j]))
        #print("ppp %lf" %(sim.states.avg_job_delay[j]))
        j += 1
    overall_job_delay = overall_job_delay / total_run
    avg_num_jobs1 = avg_num_jobs1 / total_run
    print()
    print("Overall Job Delay %lf" %(overall_job_delay))
    print("Avg num jobs %lf" %(avg_num_jobs1))
    ################# Average Number of jobs kivabe kore????
    print()


    j = 0
    while j < sim.params.No_of_stations:
        avg_number_in_queue[j] = avg_number_in_queue[j] / total_run
        avg_delay_in_queue[j] = avg_delay_in_queue[j] / total_run
        #print(" average Number in the queue %d is %lf " % ((j+1),avg_number_in_queue[j]))
        #print(" average delay in the queue %d is %lf " % ((j+1), avg_delay_in_queue[j]))
        j += 1

    j = 0
    while j < sim.params.No_of_stations:
        print(" average Number in the queue %d is %lf " % ((j + 1), avg_number_in_queue[j]))
        #print(" average delay in the queue %d is %lf " % ((j + 1), avg_delay_in_queue[j]))
        j += 1

    print()

    j = 0
    while j < sim.params.No_of_stations:
        #print(" average Number in the queue %d is %lf " % ((j + 1), avg_number_in_queue[j]))
        print(" average delay in the queue %d is %lf " % ((j + 1), avg_delay_in_queue[j]))
        j += 1
    max_delay = 0
    idxx = 0

    j = 0
    while j < sim.params.No_of_stations:
        # print(" average Number in the queue %d is %lf " % ((j + 1), avg_number_in_queue[j]))
        #print(" average delay in the queue %d is %lf " % ((j + 1), avg_delay_in_queue[j]))
        if avg_delay_in_queue[j] > max_delay :
            max_delay = avg_delay_in_queue[j]
            idxx = j
        j += 1
    print("Max delay at station %d" %(idxx+1))
    print("Bottleneck %d" %(idxx+1))
   # sim.printResults()


def main():

    task1()


main()
