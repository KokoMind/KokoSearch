from reppy.robots import Robots
from urllib import robotparser
import time

start = time.time()
link = "https://www.facebook.com/pages/Mentor-Graphics/194224383963572?pnref=lhc"
robot_url = Robots.robots_url(link)
parse = robotparser.RobotFileParser()
parse.set_url(robot_url)
parse.read()
print(parse.can_fetch('Googlebot', link))
end = time.time()
print(end - start)
