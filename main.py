import math

class Solution:
    def __init__(self, file_path):
        self.file_path = file_path
        self.segments = self.read_segments()

    def read_segments(self):
        segments = []
        with open(self.file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) != 5:
                    print(f"Skipping invalid line: {line.strip()}")
                    continue
                try:
                    x1, y1, x2, y2 = map(float, parts[:4])
                    segment_number = int(parts[4])
                    segments.append(((x1, y1), (x2, y2), segment_number))
                except ValueError as e:
                    print(f"Error processing line: {line.strip()}. {e}")
        return segments

    def area_ratio(self, segment):
        (x1, y1), (x2, y2), segment_number = segment
        if not (0 <= x1 <= 1 and 0 <= y1 <= 1 and 0 <= x2 <= 1 and 0 <= y2 <= 1):
            raise ValueError("Coordinates must lay on the sides of the unit square.")

        if (x1 == 0 and y2 == 1) or (y1 == 0 and x2 == 1) or (y1 == 0 and x2 == 1) or (x1 == 0 and y2 == 1):
            # Bottom-Right or Left-Top connection
            area = 0.5 * (x2 - x1) * (y2 - y1)
            left_area_ratio = min(area, 1 - area)
            right_area_ratio = max(area, 1 - area)

        elif ((x1 == 0 and y2 == 0) or (y1 == 0 and x2 == 0)) or ((y1 == 1 and x2 == 1) or (x1 == 1 and y2 == 1)):
            # Bottom-Left or Right-Top connection
            area =abs(0.5 * (x2 - x1) * (y2 - y1))
            left_area_ratio = min(area, 1 - area)
            right_area_ratio = max(area, 1 - area)

        elif x1 == 0 and x2 == 1:
            # Left-Right connection
            area = 0.5 * (y2+y1)
            left_area_ratio = area
            right_area_ratio = 1 - area
        elif y1 == 0 and y2 == 1:
            # Bottom-Top connection
            area = 0.5 * (x1+x2)
            left_area_ratio = area
            right_area_ratio = 1 - area
        else:
            raise ValueError("Segment does not connect two sides of the square.")

        return f"Segment {segment_number}: Left Area Ratio = {left_area_ratio:.4f}, Right Area Ratio = {right_area_ratio:.4f}"

    def find_intersections(self):
        intersections = []
        for i, segment1 in enumerate(self.segments):
            for j, segment2 in enumerate(self.segments):
                if i < j:
                    intersection = self.segment_intersection(segment1, segment2)
                    if intersection:
                        intersections.append(intersection)
        return intersections

    def segment_intersection(self, segment1, segment2):
        (x1, y1), (x2, y2) = segment1[:2]
        (x3, y3), (x4, y4) = segment2[:2]

        def line(p1, p2):
            A = (p1[1] - p2[1])
            B = (p2[0] - p1[0])
            C = (p1[0]*p2[1] - p2[0]*p1[1])
            return A, B, -C

        L1 = line((x1, y1), (x2, y2))
        L2 = line((x3, y3), (x4, y4))

        D = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]

        if D != 0:
            x = Dx / D
            y = Dy / D
            if 0 <= x <= 1 and 0 <= y <= 1:
                return (x, y)
        return None

    def find_triple_intersections(self):
        intersections = self.find_intersections()
        intersection_count = {}
        for point in intersections:
            if point in intersection_count:
                intersection_count[point] += 1
            else:
                intersection_count[point] = 1

        triple_intersections = [point for point, count in intersection_count.items() if count >= 3]
        if triple_intersections:
            return triple_intersections
        else:
            print("No points where at least three segments intersect were found.")
            return []

    def run_analysis(self):
        print("Segment Area Ratios:")
        for segment in self.segments:
            try:
                ratio_message = self.area_ratio(segment)
                print(ratio_message)
            except ValueError as e:
                print(f"Segment {segment[2]} error: {e}")

        print("\nIntersections:")
        intersections = self.find_intersections()
        if intersections:
            for point in intersections:
                print(f"Intersection point: {point}")
        else:
            print("No intersection points were found.")

        print("\nTriple Intersections:")
        triple_intersections = self.find_triple_intersections()
        if triple_intersections:
            for point in triple_intersections:
                print(f"Intersection point: {point}")
        else:
            print("No points where at least three segments intersect were found.")

class Main:
    def __init__(self, file_path):
        self.file_path = file_path

    def run(self):
        solution = Solution(self.file_path)
        solution.run_analysis()

if __name__ == "__main__":
    # Replace 'segments.txt' with the path to your file
    main = Main('segments.txt')
    main.run()
