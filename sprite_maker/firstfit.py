#!/usr/bin/python

import sys
import os
import glob
import json
import math
import time
from PIL import Image
from sprite_maker import common


def overlaps (x, y, img1, img2):
	_overlaps = False
	
	_w1 = x + img1.width
	_h1 = y + img1.height
	x2 = img2.x
	y2 = img2.y
	_w2 = x2 + img2.width
	_h2 = y2 + img2.height
	
	return (x < _w2 and _w1 > x2 and y < _h2 and _h1 > y2)
	
	
def isFeasible (_x, _y, _sprite, _placed, _size):
	if (_x + _sprite.width > _size):
		return False
	if (_y + _sprite.height > _size):
		return False
	
	for _img in _placed:
		if (overlaps (_x, _y, _sprite, _img)):
			return False
	
	return True


def new_column (x, y, _sprite, _placed, _size, _index = 0):
	if (x + _sprite.width > _size):
		return _size
	if (_index >= len(_placed)):
		return x

	if (overlaps (x, y, _sprite, _placed[_index])):
		return new_column(_placed[_index].x + _placed[_index].width - 1, y,
				_sprite, _placed, _size, _index + 1)
	return new_column(x, y, _sprite, _placed, _size, _index + 1)


def get_first_position (_sprite, _placed, _size):
	_offset = int(common.ImgData.PADDING / 2)
	
	_count = 0
	_lastPlaced = len(_placed) - 1
	i = 0
	while (i < _size):
		if (i + _sprite.height > _size):
			return (-1, -1)
			
		j = 0
		while (j < _size):
			_count += 1
			if (j + _sprite.width > _size):
				j = 0
				break
				
			if (isFeasible (j, i, _sprite, _placed, _size)):
				return (j, i)
				
			#shift j in right direction
			j = new_column(j, i, _sprite, _placed, _size)
				
			j += 1
		# since this row is not feasible shift row
		_shift = i + 1
		for img in _placed:
			if(i >= img.y and i < img.y + img.height):
				if(_shift == i + 1):
					_shift = img.y + img.height
					continue
				if (_shift > img.y + img.height):
					_shift = img.y + img.height
		i = _shift
		
	return (-1, -1)


def firstfit (_sprites, _size):
	_placed = []
	
	for _sprite in _sprites:
		#print ("trying to fit: {}".format(_sprite.src))
		_pos = get_first_position(_sprite, _placed, _size)
		
		if (_pos[0] == -1):
			#print ("Couldn't fit {}".format(_sprite.src))
			return False
			
		_sprite.x, _sprite.y = _pos
		_placed.append(_sprite)
	return True


def spriteit (_root, _op, _size, _padding, _inc):
	common.ImgData.PADDING = _padding
	
	_sprites = common.load_image_data(_root)
	
	_sprites.sort(key = lambda _sprite : _sprite.width * _sprite.height,
		reverse = True)
	
	_start = time.time()
	success = False
	while (not success):
		print("trying with size:", _size)
		success = firstfit(_sprites, _size)
		if not success:
			_size += _inc
	_elapsed = time.time() - _start

	#generate appropriate filename
	_op = os.path.join(_op, '{}_ff_{}.png'.format(_root.replace('/', '_'), _size))
	print (_op)
	print ("Output image will be of {}x{} resolution\n".format(_size, _size))
	print ("\nplaced all {} sprites in {} seconds".format(
		len(_sprites), _elapsed))
	
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
