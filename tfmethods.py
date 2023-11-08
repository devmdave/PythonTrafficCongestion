

class TrafficMethods:
    def __init__(self) :
        pass


    def tf_density(vehicles,stretch_of_road):
        '''
        this function is made to calculate traffic density using the some of paramaters taken above.
        author: Madhav Dave.
        '''
        if vehicles == 0 or stretch_of_road == 0:
            density = 0
        elif vehicles == 0 and stretch_of_road == 0:
            density = 0
        else:
            density = vehicles/stretch_of_road
    
        return density
    

    def tf_flow(vehicles,time_interval):
        '''
        this function is made to calculate traffic flow using the neccesary parameters taken above.
        author: Madhav Dave.
    
        '''
        if time_interval == 0 or vehicles == 0:
            flow=0
        elif time_interval ==0 and vehicles == 0:
            flow=0
        else:
            flow = vehicles/time_interval
        return flow
    

    def tf_headway(stretch_of_road,vehicles):
        '''
        this function is made to calculate traffic headway using the neccesary parameters taken above.
        author:Madhav Dave.
        '''
        if stretch_of_road ==0 or vehicles == 0:
            headway = 0
        elif stretch_of_road ==0 and vehicles ==0:
            headway = 0
        else:
            headway = stretch_of_road/vehicles
        return headway


    def tf_speed(flow,density):
        '''
        this function is made to calculate the average speed of traffic movement using the neccesary parameters taken above.
        author: Madhav Dave.
        '''
        if flow == 0 or density ==0:
            speed = 0
        elif flow == 0 and density == 0:
            speed = 0
        else:
            speed = flow/density

        return speed

    def estimated_tf_at_xtime(self):
        '''
        this function is made to calculate the estimated traffic at particular x time.
        author: Madhav Dave.

        '''
        pass

    def peak_tf_time(self):
        '''
        this function is made to calculate the estimated peak traffic time
        author: Madhav Dave.
        '''
        pass
    
    def mean_tf_flow(self):
        '''this function is made to calculate mean traffic flow 
        author: Madhav Dave.
        '''
        pass

    def mean_tf_speed(self):
        '''
        this function is made to calculate mean traffic speed
        author: Madhav Dave.
        '''
        pass
    


    