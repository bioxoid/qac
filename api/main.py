from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from io import BytesIO
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from select_stars_by_qa import select_stars_by_qa
from type_definitions import Star, QAArgs
import sys
try:
    from dwave.system import DWaveSampler, EmbeddingComposite
    import dimod
except ImportError as e:
    print(e)
    sys.exit(1)


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
		"https://qac.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Star(BaseModel):
	# name: str #星座名
	# description: str #神話
	image: str
	angle: List[int]
	max_mag: float
	blur_radius: float = 15
	pixel_rate: int = 32768

@app.post("/")
def post_root(star: Star):
	with open('stars.json', 'r') as file:
		star_list = json.load(file)
	
	image = Image.open(BytesIO(base64.b64decode(star.image.replace("data:image/png;base64,", ""))))
	chosen_star_list, connection_list = make_zodiac_sign(image, star.angle, star_list, star.max_mag, star.blur_radius, star.pixel_rate)
	return chosen_star_list, connection_list

def make_zodiac_sign(image:Image, placement_angle, star_list, maximum_mag, blur_radius = 30, rate_of_using = 32768):
	placement_angle#位置指定形式合わせ
	def reverse_by_angle(coordinate):
		return coordinate#形式に合わせた変換
	
	blured_image = image.filter(ImageFilter.GaussianBlur(blur_radius))

	horizontal_offset = int(round(image.size[0] / 2))#天体と絵のスケール
	vertical_offset = int(round(image.size[1] / 2))#同上
	def trans_from_surface_to_image(m, n):
		new_m = m + horizontal_offset
		new_n = n + vertical_offset
		if 0 > new_m or 0 > new_n:
			return None
		if image.size[0] <= new_m or image.size[1] <= new_n:
			return None
		return new_m, new_n

	candidate_list = []
	array_of_blured = np.array(blured_image)
	for star in star_list:
		if maximum_mag < star['mag']:
			continue
		x, y, z = reverse_by_angle((star['x'], star['y'], star['z']))
		if 0. > z:#視線方向に合わせて除外
			continue
		place_in_image = trans_from_surface_to_image(int(round(y)), int(round(x)))#視線方向に合わせて変更
		if None is place_in_image:
			continue
		candidate_list.append((star, array_of_blured[place_in_image[0], place_in_image[1], 3]))
	chosen_star_list = choice_star_of_zodiac_dummy(candidate_list, int(round(np.count_nonzero(np.array(image)[:, :, 3]) / rate_of_using)))#qa 方式に差し替え
	# chosen_star_list = select_stars_by_qa(
	# 	candidate_list,
	# 	n_opaque=510,
	# 	n_pixel=100,
	# 	qa_args=QAArgs( lagrange_multiplier=10, token="T6nD-003e8847b163bdf7bb0adf388dc62fb50e697cb0", num_reads=1000,)
	# ) #qa 方式に差し替え

	def trans_to_image(star):
		x, y, _ = reverse_by_angle((star['x'], star['y'], star['z']))
		return trans_from_surface_to_image(int(round(y)), int(round(x)))
	connection_list = connect_star_dummy(chosen_star_list, array_of_blured, trans_to_image)#qa 方式に差し替え
	return chosen_star_list, connection_list

def choice_star_of_zodiac_dummy(candidate_list, number_of_using):
	ranking_list = sorted([(star['mag'] * (2. - alpha / 128.), star) for star, alpha in candidate_list], key=lambda x:x[0])
	chosen_list = []
	squared_restriction_radius = 10000.
	def check_chosen(candidate):
		for chosen in chosen_list:
			if squared_restriction_radius > sum([(candidate[key] - chosen[key]) ** 2 for key in ['x', 'y', 'z']]):
				return False
		return True
	for _ in range(number_of_using):
		for _, star in ranking_list:
			if check_chosen(star):
				chosen_list.append(star)
				break
	return chosen_list

def connect_star_dummy(star_list, array_of_image, trans_function):
	data_list = [(star['id'], trans_function(star)) for star in star_list]
	distance_list = sorted([((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2, (id1, id2), (coord1, coord2)) for id1, coord1 in data_list for id2, coord2 in data_list if id1 != id2], key=lambda x:x[0])
	def check_usable(coord1, coord2):
		target_matrix = array_of_image[coord1[0]:coord2[0], coord1[1]:coord2[1], 3]
		return len(target_matrix) == np.count_nonzero(target_matrix)
	group_list = [[id] for id, _ in data_list]
	def find_group(id):
		for index in range(len(group_list)):
			if id in group_list[index]:
				return index
	connection_list = []
	for _, (id1, id2), (coord1, coord2) in distance_list:
		index1 = find_group(id1)
		index2 = find_group(id2)
		if index1 == index2:
			continue
		if not check_usable(coord1, coord2):
			continue
		connection_list.append((id1, id2))
		group_list[index1] += group_list[index2]
		group_list.pop(index2)
		if 1 == len(group_list):
			break
	return connection_list
