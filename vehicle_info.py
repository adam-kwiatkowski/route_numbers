import os

class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def to_tuple(self):
        return self.x, self.y

    def to_array(self):
        return [self.x, self.y]

    @staticmethod
    def from_dict(data):
        return Point(int(data['x']), int(data['y']))


class RegionOfInterest:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __repr__(self):
        return f'RegionOfInterest({self.start}, {self.end})'

    def __iter__(self):
        yield self.start
        yield self.end

    def to_tuple(self):
        return self.start.to_tuple(), self.end.to_tuple()

    def to_sequence(self):
        return self.start.to_array() + self.end.to_array()


class VehicleInfo:
    def __init__(self, vehicle_type: str, route_number: str, vehicle_roi: RegionOfInterest,
                 route_number_roi: RegionOfInterest, image_filename: str, image_download_url: str):
        self.vehicle_type = vehicle_type
        self.route_number = route_number
        self.vehicle_roi = vehicle_roi
        self.route_number_roi = route_number_roi
        self.image_filename = image_filename
        self.image_download_url = image_download_url

    def __repr__(self):
        return f'VehicleInfo({self.vehicle_type}, {self.route_number}, {self.vehicle_roi}, {self.route_number_roi}, {self.image_filename}, {self.image_download_url})'

    @staticmethod
    def from_dict(data):
        return VehicleInfo(data['vehicleType'], data['routeNumber'],
                           RegionOfInterest(Point.from_dict(data['vehicleROI']['start']),
                                            Point.from_dict(data['vehicleROI']['end'])),
                           RegionOfInterest(Point.from_dict(data['routeNumberROI']['start']),
                                            Point.from_dict(data['routeNumberROI']['end'])),
                           data['path'].split('/')[-1], data['downloadUrl'])

    @staticmethod
    def column_names():
        return ['vehicleType', 'routeNumber', 'vehicleROI_start_x', 'vehicleROI_start_y', 'vehicleROI_end_x',
                'vehicleROI_end_y', 'routeNumberROI_start_x', 'routeNumberROI_start_y', 'routeNumberROI_end_x',
                'routeNumberROI_end_y', 'image_filename', 'image_download_url']

    def to_columns(self):
        return [self.vehicle_type,
                self.route_number] + self.vehicle_roi.to_sequence() + self.route_number_roi.to_sequence() + [
            self.image_filename, self.image_download_url]
    
    @staticmethod
    def from_columns(columns):
        return VehicleInfo(columns[0], columns[1],
                           RegionOfInterest(Point(columns[2], columns[3]), Point(columns[4], columns[5])),
                           RegionOfInterest(Point(columns[6], columns[7]), Point(columns[8], columns[9])),
                           columns[10], columns[11])

    @staticmethod
    def vehicle_types():
        return ['VehicleType.bus', 'VehicleType.tram']
