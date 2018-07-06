from __future__ import division
import math, random

from phenomena.particles.kinematics.parameters import boostParams

import nbody


# Sergi was here


class C12M3BodyCalc(nbody.C12MCalc):
    # Calculations for energies and momenta in the CM for particles 1 and 2 only (CM 1-2)
    def _Dalitz1(masses):
        m12 = random.uniform(masses[1]+masses[2],masses[3])
        return m12

    @staticmethod
    def E(masses,m12):
        E2 = (m12**2-masses[1]**2+masses[2]**2)/(2*m12)
        E1 = (E2**2+masses[1]**2-masses[2]**2)**(1/2)
        E3 = (masses[0]**2-m12**2-masses[3]**2)/(2*m12)
        return [E1,E2,E3]

    # We divide the Dalitz calculation so we can calculate and save the energies needed for m23
    def _Dalitz2(masses, E):
        m23 = random.uniform((E[1]+E[2])**2-((E[1]**2-masses[2]**2)**(1/2)+(E[2]**2-masses[3]**2)**(1/2))**2,(E[1]+E[2])**2-((E[1]**2-masses[2]**2)**(1/2)-(E[2]**2-masses[3]**2)**(1/2))**2)
        return m23

    @staticmethod
    def p(masses,m12):
        num1 = m12**2-(masses[1]+masses[2])**2
        num2 = m12**2-(masses[1]-masses[2])**2
        p = (num1*num2)**(1/2)/(2*m12)
        return [p,p]

    @staticmethod
    def pxy(masses,m12,angles):
        p = C12M3BodyCalc.p(masses,m12)
        return [{   'x':p[0]*math.cos(angles[1]),
                    'y':p[0]*math.sin(angles[1])
                },{
                    'x':p[1]*math.cos(angles[2]),
                    'y':p[1]*math.sin(angles[2])
                }]

class CM3BodyCalc(nbody.CMCalc):

    def _p3(masses,dalitz):
        p3 = ((dalitz[0]**2-(masses[1]+masses[2])**2)*(dalitz[0]**2-(masses[1]-masses[2])**2))**(1/2)
        return p3

    @staticmethod
    def pExy(self,masses,angles):
        dalitz = []
        dalitz[0] = C12M3BodyCalc.dalitz1(masses)
        C12ME = C12M3BodyCalc.E(masses,dalitz[0])
        dalitz[1] = C12M3BodyCalc.dalitz2(masses,C12ME)
        p3 = CM3BodyCalc.p3(masses,dalitz)
        gamma = (1+p3**2/dalitz[0]**2)**(1/2)
        beta = boostParams.beta_from_gamma()
        C12Mpxy = C12M3BodyCalc.pxy(masses,dalitz[0],angles)

        return [
            {
            'x':gamma*(C12Mpxy[0]['x'] - beta*C12ME[0]),
            'y':C12Mpxy[0]['y'],
            'z':0,
            'E':gamma*(-beta*C12Mpxy[0]['x'] + C12ME[0])
            },
            {
            'x':gamma*(C12Mpxy[1]['x'] - beta*C12ME[1]),
            'y':C12Mpxy[1]['y'],
            'z':0,
            'E':gamma*( -beta*C12Mpxy[1]['x'] + C12ME[1])
            },
            {
            'x':p3,
            'y':0,
            'z':0,
            'E':(masses[3]**2+p3**2)**(1/2)
            }
        ]

class LAB3BodyCalc(nbody.LabCalc):

    def __init__(self,decay,masses,theta,gamma):
        self._decay = decay
        self._gamma = gamma
        self._masses = masses
        self._anglesCM12 = self._set_AnglesCM12(theta)
        self._pExyz = self._set_pExyz(self._masses, self._anglesCM12, self._gamma, self._dalitzvar, self._energies)
        self._p = self._set_p()
        self._theta = self._set_boostedAngles() # Boost angles from CM RF to LAB RF

        self._values = self._set_values()

    # It's convenient to set the angles in the simplest reference frame (CM 1-2 in this case)
    def _set_AnglesCM12(self, theta):
        anglesCM = []  # list 0:parent particle angle, 1:first decay particle angle in CM, etc
        anglesCM.append(theta)
        angle = 2*math.pi * random.random()
        angles = [angle,angle+math.pi]
        for angle in angles:
            anglesCM.append(angle)
        return anglesCM

    def _set_pExyz(self,masses,angles,gamma):
        beta = boostParams.beta_from_gamma(gamma)
        CMpExy = CM3BodyCalc.pExyz(masses,angles)

        # Change the angles from the CM 1-2 to the new frame CM
        # Also add a random angle between the plane of the decay in CM and the speed of P
        theta0 = CMpExy[0]['y']/CMpExy[0]['x']
        theta1 = CMpExy[1]['y']/CMpExy[1]['x']
        alpha = 2*math.pi * random.random()
        angles[1:4] = [math.atan(theta0)+alpha,math.atan(theta1)+alpha,alpha]

        # Update the momenta with the new angles
        p = self._set_p()
        for i in range(1,4):
            CMpExy[i]['x'] = p[i]['x']*math.cos(angles[i])
            CMpExy[i]['y'] = p[i]['y']*math.sin(angles[i])


        return [
            {
            'x':gamma*(CMpExy[0]['x']+ beta*CMpExy[0]['E']),
            'y':CMpExy[0]['y'],
            'z':0,
            'E':gamma*(beta*CMpExy[0]['x']+ CMpExy[0]['E'])
            },
            {
            'x':gamma*(CMpExy[1]['x']+ beta*CMpExy[1]['E']),
            'y':CMpExy[1]['y'],
            'z':0,
            'E':gamma*(beta*CMpExy[1]['x']+ CMpExy[1]['E'])
            },
            {
            'x':gamma*(CMpExy[2]['x']+ beta*CMpExy[2]['E']),
            'y':CMpExy[1]['y'],
            'z':0,
            'E':gamma*(beta*CMpExy[2]['x']+ CMpExy[2]['E'])
            }
        ]

    def _set_p(self):
        return [math.sqrt(self._pxy[0]['x']**2+self._pxy[0]['y']**2),math.sqrt(self._pxy[1]['x']**2+self._pxy[1]['y']**2),math.sqrt(self._pxy[2]['x']**2+self._pxy[2]['y']**2)]

    def _set_boostedAngles(self):
        if self._gamma != 1:
            theta0 = self._pxy[0]['y']/self._pxy[0]['x']
            theta1 = self._pxy[1]['y']/self._pxy[1]['x']
            theta2 = self._pxy[2]['y']/self._pxy[2]['x']
            theta = [math.atan(theta0),math.atan(theta1),math.atan(theta2)]
        else:
            theta = self._anglesCM[1:]

        return [theta[0]+self._anglesCM[0],theta[1]+self._anglesCM[0]]


    def _set_values(self):
        return  [{
                    'name': self._decay[0],
                    'p': self._p[0],
                    'theta':self._theta[0],
                    'E':self._pExyz[0]['E']      },{
                    'name': self._decay[1],
                    'p': self._p[1],
                    'theta':self._theta[1],
                    'E':self._pExyz[1]['E']      },{
                    'name': self._decay[2],
                    'p': self._p[2],
                    'theta':self._theta[2],
                    'E':self._pExyz[2]['E']
                }]

    @property
    def values(self):
        return self._values
