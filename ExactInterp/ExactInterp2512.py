#!/usr/bin/env python3
# coding=utf-8

# ExactInterp2512
# License: GPL3
# Copyright (c) Jan Knuts EM-Teknik
# https://github.com/EM-Teknik/ExactInterp
#
import inkex
from inkex import bezier
from inkex import command, styles
from inkex.elements import PathElement
import copy



class ExactInterp (inkex.EffectExtension):
    
    def add_arguments (self, pars):
        pars.add_argument ("--use_t" , type=inkex.Boolean, help="t")
        pars.add_argument ("--t", type=float, default=0.5, help="t-valu1(0-1)")
        pars.add_argument ("--intervals", type=int, default=5, help="intervals")
 
    def effect(self):
        #t=0.5 
        use_t = self.options.use_t
        t = self.options.t

        if use_t:
            intervals=2  
        else:
            intervals = self.options.intervals
        
        svgs=self.svg.selection.filter(inkex.PathElement).values()

        if len(svgs) != 2:
            self.msg("Select 2 paths !")
            return

        current_layer = self.svg.get_current_layer()  

        path1,path2=svgs
 
        if len(path1.path) != len(path2.path):
            self.msg("Warning, paths has not equal numbers of nodes\n")
            self.msg("Number of nodes in path1= %s, in path2= %s\n" % (len(path1.path) ,len(path2.path)))
            return

        csp1=path1.path.to_superpath()
        csp2=path2.path.to_superpath()

        for n in range(1,intervals):
            if use_t:
                pass
            else:
                t=n/intervals

            path0=copy.deepcopy(path1)
            current_layer.append(path0)     
            csp0=path0.path.to_superpath()
            csp00=csp0+csp1+csp2
            sp0,sp1,sp2=csp00
           
            for m in range(0,len(sp0)):
                sp0[m][0][0]=sp1[m][0][0]*(1-t)+sp2[m][0][0]*t
                sp0[m][0][1]=sp1[m][0][1]*(1-t)+sp2[m][0][1]*t
                sp0[m][1][0]=sp1[m][1][0]*(1-t)+sp2[m][1][0]*t
                sp0[m][1][1]=sp1[m][1][1]*(1-t)+sp2[m][1][1]*t
                sp0[m][2][0]=sp1[m][2][0]*(1-t)+sp2[m][2][0]*t
                sp0[m][2][1]=sp1[m][2][1]*(1-t)+sp2[m][2][1]*t

            path0.path=csp0

if __name__ == '__main__':
    ExactInterp().run()
