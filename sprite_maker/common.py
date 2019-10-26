#!/usr/bin/python3

import sys
import os
import glob
import json
import math
import time
from PIL import Image

class ImgData:
	PADDING = 0
	MAX_WIDTH = 0
	_WIDTH = 0;
	_HEIGHT = 0
	src = ""
	#pos = (0, 0)
	x = 0
	y = 0
	width = 0
	height = 0
	rotate = False

class Rect:
	x = 0
	y = 0
	w = 0
	h = 0

_types = ["*.jpg", "*.jpeg", "*.png"]

def load_image_data (_root):
	_img_list = []
	for _type in _types:
		_img_list.extend(glob.glob("{}/{}".format(_root, _type)))
	
	_img_data = []
	
	for img in _img_list:
		_idata = ImgData()
		_idata.src = img
		im = Image.open(img)
		_idata.width, _idata.height = im.size
		_idata.width += ImgData.PADDING
		_idata.height += ImgData.PADDING
		ImgData.MAX_WIDTH += _idata.width
		if(ImgData._HEIGHT < _idata.height):
			ImgData._HEIGHT = _idata.height
		im.close()
		_img_data.append(_idata)
	
	ImgData._WIDTH = ImgData.MAX_WIDTH
	return _img_data


def overlaps (sprite1, sprite2):
	return ((sprite1.x < sprite2.x + sprite2.width)
		and (sprite1.x + sprite1.width > sprite2.x)
		and (sprite1.y < sprite2.y + sprite2.height)
		and (sprite1.y + sprite1.height > sprite2.y))


def overlapRect (r1, r2):
	return ((r1.x < r2.x + r2.w) and (r1.x + r1.w > r2.x)
		and (r1.y < r2.y + r2.h) and (r1.y + r1.h > r2.y))


def getWidth (sprites):
	_w = 0
	for _sprite in sprites:
		if(_w < _sprite.x + _sprite.width):
			_w = _Sprite.x + _sprite.width
	return _w


def getHeight (sprites):
	_h = 0
	for _sprite in sprites:
		if(_h < _sprite.y + _sprite.height):
			_h = _sprite.y + _sprite.height
	return _h
	return _img_data
