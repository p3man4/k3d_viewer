# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

import sys
import os


import smt_process.process as process
import smt_process.detect_class as detect_class
import smt_process.read_component_db as read_component_db

import cv2
import numpy as np

# change below to your DATA_PATH and DP_ROOT
DATA_PATH='/home/junwon/smt-data/Train_0818/'
DP_ROOT='/home/junwon/smt-project/SMT-newtest/detect_part/'


menu={}
def index(request):
    return render(request, 'k3d_viewer/index.html',{})

def main(request):
    return render(request, 'k3d_viewer/main.html',locals())

def selector(request):
    global menu
    for x in os.walk(DATA_PATH):
        menu[x[0].split('/')[-1]]= x[2]
    

    return render(request, 'k3d_viewer/selector.html',{'menu':menu})

def info_view(request):
    
    fileNm= None
    q = None
    k3dfile=None
    img_buf=None
    img_bgr_size=None
    img_gray_size=None
    img_3d_size=None
    compid=None
    print "<<info_view>>"
    if 'fileNm' in request.GET:
        fileNm = request.GET['fileNm']


    if 'q' in request.GET:
        q = request.GET['q']


    if fileNm is not None and q is not None:
        f_path= DATA_PATH + str(q) + "/" + fileNm
        f = open(f_path,'r')
    
        DC =  detect_class.ComponentDetector()
        k3dfile = DC.parse_k3d(f.read())
        f.close()

        cv2.imwrite('./k3d_viewer/static/k3d_viewer/img_bgr.png',k3dfile['img_bgr'])

        img_bgr_size = k3dfile['img_bgr'].shape

        cv2.imwrite('./k3d_viewer/static/k3d_viewer/img_gray.png',k3dfile['img_gray'])

        img_gray_size =k3dfile['img_gray'].shape

        img3d = k3dfile['img_3d'].astype(int)
        cv2.imwrite('./k3d_viewer/static/k3d_viewer/img_3d.png',img3d)

        img_3d_size= img3d.shape

        compid= k3dfile['component_id']

    return render(request, 'k3d_viewer/info_view.html',{'q':q,'fileNm':fileNm,'k3dfile':k3dfile,'img_bgr_size':img_bgr_size,'img_gray_size':img_gray_size,'img_3d_size':img_3d_size,'compid':compid})

def search_list(request):
    q=None
    file_list=[]
    all_list=[]
    print "<< search list section>>"
    if 'q' in request.GET:
        q= request.GET['q']
        print 'q:', q
        all_list= menu[q]
        
        for file in all_list:
            if not file.endswith('txt'):
                file_list.append(file)

    return render(request, 'k3d_viewer/search_list.html',{'q':q,'menu':menu,'file_list':file_list})
