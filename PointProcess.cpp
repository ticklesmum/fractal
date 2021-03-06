//
//  PointProcess.cpp
//  Flame_Fractal
//
//  Created by Jiali Mei on 2/20/13.
//  Copyright (c) 2013 Bunny. All rights reserved.
//

#include "PointProcess.h"

#define MAXWALK 30
#define NONPLOT 20

PointProcess::PointProcess(){}
PointProcess::~PointProcess(){}

std::vector<numty> PointProcess::getXcord(){
    if (_xtraj.empty()){
        std::cout<<"empty process !\n"<<std::endl;
    }
    return _xtraj;
}

std::vector<numty> PointProcess::getYcord(){
    if (_ytraj.empty()) {
        std::cout<<"empty process !\n"<<std::endl;
    }
    return _ytraj;
}

void PointProcess::postTrans(Parameters & pparam){
    // final transformation to give it a certain symetry...
    std::vector<numty> tmp = pparam.getPostTrans();
    for (int i = 0; i < _xtraj.size(); i++) {
    _xtraj[i] = tmp[0]* _xtraj[i] + tmp[1]* _ytraj[i] + tmp[2];
    _ytraj[i] = tmp[3]* _xtraj[i] + tmp[4]* _ytraj[i] + tmp[5];
    }
    
}

void PointProcess::start(int iter, Parameters & pparam){
    _xtraj.clear();
    _ytraj.clear();
    numty tmpx = 0;
    numty tmpy = 0;
//    srand(time(NULL));

    Transformation transformer(pparam);
    
    for (int it = 0; it < iter; it ++){
// debug use
//        std::cout<<"\n *** new point --- x:"<<_xtraj.back()<<", y-"<<_ytraj.back();
//        std::cout<<"\nstart point:\n ";
                
        tmpx = 4*float(rand()%RANGE)/RANGE-2;
        tmpy = 4*float(rand()%RANGE)/RANGE-2;
        for (int i = 0; i < MAXWALK; i++){
            transformer.push(tmpx,tmpy);
            /*transformer.preTrans();
            transformer.nonLinTrans(eng);
            transformer.postTrans();*/
            
            /* or use multiTrans instead to save some time */
            transformer.multiTrans();
            tmpx = transformer.getOutPut()[0];
            tmpy = transformer.getOutPut()[1];
            if (!isValidPoint(tmpx, tmpy))
                break;
// debug use
//            std::cout<<"\n x-"<<tmpx<<", y-"<<tmpy;
            
            if (i >= NONPLOT) {
                _xtraj.push_back(tmpx);
                _ytraj.push_back(tmpy);
                
            }
        }
        
    }
}