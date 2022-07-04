#pragma once

#include <cstdint>
#include <vector>

struct rect_t
{
	int32_t x, y, width, height;

	rect_t(int32_t x=0, int32_t y=0, int32_t width=0, int32_t height=0)
	{
		this->x = x;
		this->y = y;
		this->width = width;
		this->height = height;
	}

	int32_t area() const
	{
		return width * height;
	}

	// checks if given rectangle fits within this rectangle or not
	bool canContain(const rect_t& other) const
	{
		return (this->width >= other.width)
			&& (this->height >= other.height);
	}

	void split(const rect_t& rect, rect_t& big, rect_t& small)
	{
		auto dw = this->width - rect.width;
		auto dh = this->height - rect.height;

		if (dh > dw)
		{
			big.x = this->x + rect.width;
			big.y = this->y;
			big.width = this->width - rect.width;
			big.height = this->height;

			small.x = this->x;
			small.y = this->y + rect.height;
			small.width = rect.width;
			small.height = this->height - rect.height;
		}
		else
		{
			big.x = this->x;
			big.y = this->y + rect.height;
			big.width = this->width;
			big.height = this->height - rect.height;

			small.x = this->x + rect.width;
			small.y = this->y;
			small.width = this->width - rect.width;
			small.height = rect.height;
		}

		// if (big.area() < small.area())
		// {
		// 	auto temp = big;
		// 	big = small;
		// 	small = temp;
		// }
	}
};

struct packer_t
{
	int32_t width, height;
	std::vector<rect_t> partitions;

	packer_t(int32_t w, int32_t h)
	{
		width = w;
		height = h;
		partitions.push_back(rect_t(0, 0, w, h));
	}

	bool pack(const rect_t& rect, int32_t& x, int32_t& y)
	{
		for (auto& part : partitions)
		{
			if (part.canContain(rect))
			{
				x = part.x;
				y = part.y;

				rect_t big;
				rect_t small;
				part.split(rect, big, small);
				part = small;
				partitions.push_back(big);
				return true;
			}
		}

		// no suitable partition was found
		return false;
	}

	void mergePartitions()
	{
		int max_height = 0;

		for (const auto& part : partitions)
		{
			if (part.y > max_height)
				max_height = part.y;
		}

		partitions.clear();
		partitions.push_back(rect_t(0, max_height, width, height - max_height));
	}
};