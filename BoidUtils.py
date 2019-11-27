'''
# Boid Utils
- Code By Michael Sherif Naguib
- license: MIT
- Date: 6/27/19
- @University of Tulsa
## Description:
- This file holds a lot of usefull Boid Specific STATIC methods for calculations....
'''

#imports
from Vector import Vector
import numpy as np
import math
import random
class BoidUtils:
    def __init__(self):
        pass
    @staticmethod
    def absoluteValsFromRelative(relValues,maxValue):
        '''
        :description:        Compute absolute values given a relative set of values and a maximim:
                             i.e rescale the weights according to size up to the max

                             normalizedVect(relValues)*maxValue
        :param relWeights:   the values to convert to absolute weights [1,1,1] & max=5 ==> [5,5,5]
        :param maxWeight:    the value to scale by
        :return: the absolute values
        '''
        # Each value becomes its fraction of the average
        s = sum(relValues)
        assert(s!=0)
        absoluteValues = [relValue*maxValue*(1/s) for relValue in relValues]
        return absoluteValues
    @staticmethod
    def limitVect(vect,mag):
        vmag = np.linalg.norm(vect)
        if vmag>mag:
            return (mag/vmag)*vect
        else:
            return vect
    @staticmethod
    def cohereForce(boid,boids,neighbors,distances,distance,weight,dim=3):
        '''
        :description:       Calculates the coherence force update for the boids sim for a particular boid
        :param boids:       a list of all the boids
        :param neighbors:   a list of indicies of the neighbors of the boid (implicit) we are computing for
        :param distances:   the distances coresponding to that boid to the other nearest boids...
        :param distance:    the max distance for which this rule is valid
        :param weight:      the relative strength of this force...
        :param dim:         the dimension for the vectors...
        :return:            vector representing the force update
        '''
        pos_sum = np.zeros(dim)
        mass_sum=0
        count = 0
        # For every Neighbor:
        for indx in range(len(neighbors)):
            # Check to make sure it meets the distance requirements
            if distances[indx]> distance:
                continue# Goto the next
            # otherwise
            mass = boids[neighbors[indx]].mass
            mass_sum+=mass
            pos_sum = np.add(pos_sum,boids[neighbors[indx]].pos*(1/mass))
            count+=1
        # If there were no force updates return 0 vect
        if count==0:
            return pos_sum
        # otherwise
        target = pos_sum*(1/mass_sum)
        steer = np.subtract(np.subtract(target,boid.pos),boid.vel)
        return steer*weight
    @staticmethod
    def seperateForce(boid,boids,neighbors,distances,distance,weight,dim=3):
        '''
        :description:       Calculates the seperation force update for the boids sim for a particular boid
        :param boids:       a list of all the boids
        :param neighbors:   a list of indicies of the neighbors of the boid (implicit) we are computing for
        :param distances:   the distances coresponding to that boid to the other nearest boids...
        :param distance:    the max distance for which this rule is valid
        :param weight:      the relative strength of this force...
        :param dim:         the dimension for the vectors...
        :return:            vector representing the force update
        '''
        pos_sum = np.zeros(dim)
        count = 0
        mass_sum=0
        # For every Neighbor:
        for indx in range(len(neighbors)):
            # Check to make sure it meets the distance requirements
            if distances[indx]> distance:
                continue# Goto the next
            # otherwise
            # calculate current separation distance direction and weight by edge distance
            edge_dist = distances[indx]
            sep_norm = np.subtract(boid.pos,boids[neighbors[indx]].pos)* (1/(edge_dist if edge_dist!=0 else random.random()))# Catch divide by zero errors by inroducing a small random value
            # since the two boids overlap exactly ... introduce some small uncertianty in the distance ... interesting ... this makes sense from a practical programatic perspective...
            # uncertainty in the location of an item at small scales makes sense ... Heisenburg uncertianty?
            mass = boids[neighbors[indx]].mass
            pos_sum = np.add(pos_sum,sep_norm*mass)
            count+=1
            mass_sum+=mass
        # If there were no force updates return 0 vect
        if count==0:
            return pos_sum
        # otherwise

        target = pos_sum*(1/mass_sum)
        steer = np.subtract(target,boid.vel)
        return steer*weight
    @staticmethod
    def alignForce(boid,boids,neighbors,distances,distance,weight,dim=3):
        '''
        :description:       Calculates the alignment force update for the boids sim for a particular boid
        :param boids:       a list of all the boids
        :param neighbors:   a list of indicies of the neighbors of the boid (implicit) we are computing for
        :param distances:   the distances coresponding to that boid to the other nearest boids...
        :param distance:    the max distance for which this rule is valid
        :param weight:      the relative strength of this force...
        :param dim:         the dimension for the vectors...
        :return:            vector representing the force update
        '''
        vel_sum = np.zeros(dim)
        mass_sum=0
        count = 0
        # For every Neighbor:
        for indx in range(len(neighbors)):
            # Check to make sure it meets the distance requirements
            if distances[indx]> distance:
                continue# Goto the next
            # otherwise
            mass = boids[neighbors[indx]].mass
            mass_sum+=mass
            vel_sum = np.add(vel_sum,boids[indx].vel*mass)
            count+=1
        # If there were no force updates return 0 vect
        if count==0:
            return vel_sum
        # otherwise
        target = vel_sum*(1/(mass_sum))
        steer = np.subtract(target,boid.vel)
        return steer*weight
