# -*- coding: utf-8 -*-
__author__ = 'SeekerLiu'

def study_laravel():
    study = input("想学 PHP Laravel 和 Vue.js 么？(yes/no)\n>")
    if study == 'no':
        print('滚犊子！')
        study_laravel()
    elif study == 'yes':
        print('到 laravist.com 成为现代的 Web 开发工程师吧！')
        study_laravel()
    else:
        pass

study_laravel()