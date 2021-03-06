//
//  Parameters.cpp
//  Flame_Fractal
//
//  Created by Jiali Mei on 2/20/13.
//  Copyright (c) 2013 Bunny. All rights reserved.
//

#include "Parameters.h"


// NEED to check parameters' validity, some robustness test !! 


Parameters::Parameters(){
    _nonLinTrans[0] = sinus;
    _nonLinTrans[1] = spheric;
    _nonLinTrans[2] = swirl;
    _nonLinTrans[3] = horseshoe;
    _nonLinTrans[4] = polar;
    _nonLinTrans[5] = hankerchief;
    _nonLinTrans[6] = heart;
    _nonLinTrans[7] = disc;
    _nonLinTrans[8] = spiral;
    _nonLinTrans[9] = hyperbolic;
    _nonLinTrans[10] = diamond;
    _nonLinTrans[11] = ex;
    
    _postTrans.assign(6, 0);
    _postTrans.at(0) = _postTrans.at(4) = 1;
    for (int k = 0; k<100; k++) {
        _preTrans[k].assign(6, 0);
        _preTrans[k].at(0) = _preTrans[k].at(4) = 0.5;
        _preTrans[k].at(5) = 0.5*(k%4==0);
        _preTrans[k].at(2) = 0.5*(k%4==1);
        if (k%4 == 3) _preTrans[k] = _postTrans;
    }
    _probNonLin.assign(12, 0);
    _probNonLin.at(0) = 1;
    _probLin.assign(100, 1.0/100.0);
    _k = 1;
    
}

Parameters::~Parameters(){}

int Parameters::getCount() const {
    return _k;
}

std::vector<numty> Parameters::getProbaNonLin() const{
    return _probNonLin;
}

std::vector<numty> Parameters::getProbaLin() const{
    return _probLin;
}

std::vector<numty> Parameters::getPreTrans(int which) const {
    return _preTrans[which];
}

std::vector<numty> Parameters::getPostTrans() const{
    return _postTrans;
}

// updata parameters through specifying which non linear trans to be used, and how many non linear to be used.
void Parameters::update(std::vector<bool> whichNonLin, int numLin) {
    // the length of the bool vector has to be 12
    numty normConst = 0;
    for (int i = 0; i <12; i++) normConst += numty(whichNonLin[i]);
    for (int i = 0; i<12; i++){
        _probNonLin.at(i) = numty(whichNonLin[i])/normConst;
    }

    _probLin.assign(numLin, 0);
    for (int i = 0; i<numLin; i++)
        _probLin.at(i) = 1/float(numLin);
    
    // generate linear parameters in a random way
    std::vector<numty> tmp;
    tmp.assign(5*numLin, 0);
    for (int i = 0; i<5*numLin; i++) tmp.at(i) = numty(rand()%RANGE)/RANGE;
    for (int i = 0; i<numLin; i++){
        _preTrans[i].at(0) = (1.5*tmp.at(5*i))*cosf(tmp.at(5*i+2)*2*M_PI);
        _preTrans[i].at(1) = -(1.5*tmp.at(5*i+1))*sinf(tmp.at(5*i+2)*2*M_PI);
        _preTrans[i].at(2) = tmp.at(5*i+3);
        _preTrans[i].at(3) = (1.5*tmp.at(5*i))*sinf(tmp.at(5*i+1)*2*M_PI);
        _preTrans[i].at(4) = (1.5*tmp.at(5*i+1))*cosf(tmp.at(5*i+2)*2*M_PI);
        _preTrans[i].at(5) = tmp.at(5*i+4);
    }

}

// still need to define function isContract