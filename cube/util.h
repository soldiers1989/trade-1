#pragma once
#include "cube/type.h"
BEGIN_CUBE_NAMESPACE
cube::byte* fast_search(const cube::byte* content, int content_length, const cube::byte* target, int target_length);
cube::byte* slow_search(const cube::byte* content, int content_length, const cube::byte* target, int target_length);
END_CUBE_NAMESPACE
