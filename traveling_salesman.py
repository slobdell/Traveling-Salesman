import random
import sys
import copy
import math
import datetime


class Location(object):
    def __init__(self, name, lat, lon):
        self.x = lon
        self.y = lat
        self.name = name

    def __repr__(self):
        return self.name
        # return "(%s, %s)" % (self.x, self.y)


def parse_cities():
    city_dict = {}
    with open('./cities.txt', 'rb') as in_file:
        for line in in_file:
            items = line.split(' ')
            cleaned_items = [item for item in items if len(item) > 0]

            lat = float(cleaned_items[1])
            lon = float(cleaned_items[2])
            city_name = line.replace(cleaned_items[0], "").replace(cleaned_items[1], "").replace(cleaned_items[2], "").strip()
            city_dict[city_name] = (lat, lon)
    in_file.close()
    return city_dict


def _get_distance(loc1, loc2):
    delta_x = loc1.x - loc2.x
    delta_y = loc1.y - loc2.y
    return math.sqrt(delta_x * delta_x + delta_y * delta_y)


def create_locations(locations_to_create):
    all_locations = []
    all_cities = []
    city_dict = parse_cities()
    for j in xrange(locations_to_create):
        city_name = random.choice(city_dict.keys())
        while city_name in all_cities:
            city = random.choice(city_dict.keys())
        all_cities.append(city_name)

    for city in all_cities:
        all_locations.append(Location(city, city_dict[city][0], city_dict[city][1]))
    return all_locations


def determine_possible_paths(all_locations):
    all_paths = []

    def create_path(visited_locations, unvisited_locations):
        if len(unvisited_locations) == 0:
            all_paths.append(visited_locations)
        for unvisited_loc in unvisited_locations:
            vis_copy = copy.copy(visited_locations)
            unvis_copy = copy.copy(unvisited_locations)
            unvis_copy.remove(unvisited_loc)
            vis_copy.append(unvisited_loc)
            create_path(vis_copy, unvis_copy)

    create_path([], all_locations)
    return all_paths


def find_shortest_path(possible_paths):
    min_distance = sys.maxint
    min_path = None
    for path in possible_paths:
        total_distance = 0.0
        for index in xrange(len(path) - 1):
            if index == len(path) - 1:
                total_distance += _get_distance(path[index], path[0])
            else:
                total_distance += _get_distance(path[index], path[index + 1])
        if total_distance < min_distance:
            min_distance = total_distance
            min_path = path
    return min_distance, min_path


def _timedelta_to_seconds(timedelta):
    microseconds = timedelta.microseconds
    seconds = float(microseconds) / 1000000
    seconds += timedelta.seconds
    return seconds


def run_simulation(locations_to_create, for_time=False):
    start_time = datetime.datetime.now()
    all_locations = create_locations(locations_to_create)
    possible_paths = determine_possible_paths(all_locations)
    total_distance, best_route = find_shortest_path(possible_paths)
    end_time = datetime.datetime.now()
    seconds = _timedelta_to_seconds((end_time - start_time))

    if not for_time:
        print "Executed in %s seconds" % seconds
        print "Given the %s locations created, the best path is %s units" % (locations_to_create, total_distance)
        print "The Route is as follows:\n"
        print best_route
        print "\n"
    else:
        print "%s Locations: %s seconds" % (locations_to_create, seconds)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Pass in the number of locations to create!  OR...pass in 'time' as the second argument"
    elif sys.argv[1].lower() == 'time':
        locations_to_create = 1
        while True:
            run_simulation(locations_to_create, True)
            locations_to_create += 1
    else:
        locations_to_create = int(sys.argv[1])
        run_simulation(locations_to_create)
