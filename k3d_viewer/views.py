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

DATA_PATH='/home/junwon/smt-data/Train_All/'

DP_ROOT='/home/junwon/smt-project/SMT/detect_part/'
MODEL=DP_ROOT + 'cd_20170714.model'

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
        print 'k3dfile:',k3dfile.keys()

        cv2.imwrite('./k3d_viewer/static/k3d_viewer/img_bgr.png',k3dfile['img_bgr'])

        cv2.imwrite('./k3d_viewer/static/k3d_viewer/img_gray.png',k3dfile['img_gray'])


        #DC.get_components_from_pickle(MODEL,callback=progressbar_callback)
        #print 'k3dfile observed_w:',k3dfile['observed_w']

    return render(request, 'k3d_viewer/info_view.html',{'q':q,'fileNm':fileNm,'k3dfile':k3dfile})

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