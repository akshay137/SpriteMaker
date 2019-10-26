#!/usr/bin/python3

import sys
import os
import glob
import json
import math
import time
from PIL import Image
from sprite_maker import common


def fits (_img, _space):
	return (_img.width <= _space.w and _img.height <= _space.h)


def partitionFit (sprites, size):
	#create first partition as whole spritesheet
	_partitions = [common.Rect()]
	_partitions[0].w = size
	_partitions[0].h = size
	
	for _sprite in sprites:
		#print ("trying to fit", _sprite.src)
		success = False
		_fits = []
		#_partitions.sort(key = lambda _sp : _sp.w * _sp.h)
		#_partitions.reverse()
		for _space in _partitions:
			#print ("space", _space.x, _space.y, _space.w, _space.h)
			if (fits (_sprite, _space)):
				_fits.append(_space)
				success = True
		
		if (not success):
			return False

		_fits.sort(key = lambda _sp : _sp.w * _sp.h, reverse = False)
		# place image in smallest fit
		_space = _fits[0]
		_sprite.x = _space.x
		_sprite.y = _space.y
		#print ("placed at", _sprite.x, _sprite.y, _sprite.width, _sprite.height)
		# create new spaces
		_partitions.remove(_space)
		
		#create 2 new partitions (bottom and right)
		_br = common.Rect()
		_rr = common.Rect()
		
		if(_space.w - _sprite.width < _space.h - _sprite.height):
			#vertical split
			_br.x = _space.x
			_br.y = _space.y + _sprite.height
			_br.w = _space.w
			_br.h = _space.h - _sprite.height
	
			_rr.x = _space.x + _sprite.width
			_rr.y = _space.y
			_rr.w = _space.w - _sprite.width
			_rr.h = _sprite.height
		else:
			#horizontal split
			_br.x = _space.x + _sprite.width
			_br.y = _space.y
			_br.w = _space.w - _sprite.width
			_br.h = _space.h
		
			_rr.x = _space.x
			_rr.y = _space.y + _sprite.height
			_rr.w = _sprite.width
			_rr.h = _space.h - _sprite.height
		
		
		
		if(_br.x < _br.x + _br.w and _br.y < _br.y + _br.h):
			_partitions.append(_br)
		if(_rr.x < _rr.x + _rr.w and _rr.y < _rr.y + _rr.h):
			_partitions.append(_rr)
				
	return True


def sortImage (s1):
	return s1.width * s1.height


def spriteit (_root, _op, _size, _padding, _inc):
	common.ImgData.PADDING = _padding
	
	_sprites = common.load_image_data(_root)
	
	_sprites.sort(key = sortImage, reverse = True)
	
	_start = time.time()
	success = False
	while (not success):
		print ("trying with size:", _size)
		success = partitionFit(_sprites, _size)
		if(not success):
			_size += _inc
	_elapsed = time.time() - _start
	print ("\nPlaced in {} seconds".format(_elapsed))
	
	
	print ("Output image will be of {}x{} resolution\n".format(_size, _size))
	#generate appropriate filename
	_op = os.path.join(_op, '{}_ff_{}.png'.format(_root.replace('/', '_'), _size))
	print (_op)
	
	#placeholder
	_area = 0
	_lb = _sprites[0].y + _sprites[0].height
	for img in _sprites:
		_area += img.width * img.height
		_b = img.y + img.height
		if (_b > _lb):
			_lb = _b
			
	_unused = (_size * _size) - _area
	print ("wasted", _unused, "pixels")
	print (_unused / (_size * _size) * 100, "%")
	
	print ("\n\nNow writing sprites to:", _op)
	_spritesheet = Image.new("RGBA", (_size, _size))
	for _sprite in _sprites:
		#print ("Pasting {}".format(_sprite.src))
		_sp = Image.open(_sprite.src)
		_spritesheet.paste(_sp, (_sprite.x, _sprite.y))
		_sp.close()
	
	_elapsed = time.time() - _start
	print ("\nDone in {} seconds".format(_elapsed))
	
	
	print ("Writing to disk...")
	_spritesheet.save(_op)
	_spritesheet.close()
	
	#output a json file for image positions
	_json = json.dumps(_sprites, indent = 4, sort_keys = True,
		default = lambda x : x.__dict__)
	_jf = open("{}.json".format(_op), 'w+')
	_jf.write(_json)
	_jf.close()
	
	_elapsed = time.time() - _start
	print ("\nDone in {} seconds".format(_elapsed))
