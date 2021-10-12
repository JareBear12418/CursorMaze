import math

points_of_collision = [(160.0, 292.5),
 (0.0, 200.00213475328354),
 (0.0, 200.00000000000003),
 (0.0, 199.99786522203328),
 (0.0, 100.00391596851114),
 (5.684341886080802e-14, 100.0),
 (0.0032548430767178615, 99.99999999999997),
 (35.13240018313621, 100.0),
 (35.1351351351351, 100.00000000000003),
 (100.00131418066482, 200.0),
 (109.40050761816128, 200.00000000000003),
 (109.40170940170941, 199.99999999999997),
 (109.40291117210987, 200.0),
 (131.16781630228456, 200.00000000000006),
 (131.16883116883116, 200.0),
 (131.16984602905137, 199.99999999999994),
 (141.02467710190172, 200.0),
 (141.02564102564102, 200.00000000000003),
 (141.0266049454258, 200.0),
 (172.64863035230033, 200.00000000000006),
 (172.64957264957266, 199.99999999999994),
 (172.6505149494222, 199.99999999999994),
 (179.21981428350276, 199.99999999999997),
 (179.2207792207792, 200.00000000000006),
 (179.22174416206582, 200.00000000000003),
 (199.99890203177497, 200.0),
 (200.0, 200.0),
 (200.0, 200.00253900378567),
 (200.0, 208.92642533781498),
 (200.0, 208.92857142857144),
 (200.0, 208.93071742965378),
 (200.0, 237.4988437341013),
 (200.0, 237.50000000000003),
 (200.0, 237.5011562341018),
 (200.0, 243.74900584725873),
 (200.0, 243.75),
 (200.0, 243.7509941285091),
 (200.0, 258.08753924574205),
 (200.0, 258.0882352941176),
 (200.0, 258.08893133051725),
 (200.0, 260.4160093263248),
 (200.0, 260.4166666666667),
 (200.0, 260.4173239964638),
 (200.0, 266.070853950285),
 (200.0, 266.07142857142856),
 (200.0, 266.072003184979),
 (200.0, 269.85241295116157),
 (200.0, 269.8529411764706),
 (200.0, 269.8534693957983),
 (200.0, 277.08287391315986),
 (200.0, 277.08333333333337),
 (200.0, 277.0837927499655),
 (200.0, 281.61721745125334),
 (200.0, 281.61764705882354),
 (200.0, 281.61807666405616),
 (200.0, 293.38195274662803),
 (200.0, 293.38235294117646),
 (200.0, 293.38275313590145),
 (200.0, 293.7495996095001),
 (200.0, 293.75),
 (200.0, 293.75040039075014),
 (200.0, 294.64245599511287),
 (200.0, 294.6428571428571),
 (200.0, 294.64325829103126),
 (200.0, 299.99958593827637),
 (200.0, 300.0),
 (300.0, 318.75144922146734),
 (300.0, 336.7631659326371),
 (300.0, 336.76470588235287),
 (300.0, 336.7662458418067),
 (300.0, 355.20665245978586),
 (300.0, 355.20833333333337),
 (300.0, 355.21001422193876),
 (300.0, 377.93925503984053),
 (300.0, 377.94117647058823),
 (300.0, 377.94309792478884),
 (300.0, 399.9977745706595),
 (299.99999999999994, 400.0),
 (299.9971017819302, 400.0),
 (284.3398625453982, 400.0),
 (284.3373493975903, 400.0),
 (284.33483630791727, 400.0),
 (232.53168485233158, 400.0),
 (232.53012048192772, 400.0),
 (232.5285561326333, 400.0),
 (200.0012238417632, 400.0),
 (199.99999999999997, 400.0),
 (199.99877616734443, 399.99999999999994),
 (180.72400651615717, 400.0),
 (180.72289156626505, 399.9999999999999),
 (180.72177662067156, 400.0000000000001),
 (128.91682752965536, 400.0),
 (128.91566265060237, 400.0000000000001),
 (128.91449776481278, 399.99999999999994),
 (100.00140987585189, 400.0),
 (100.0, 400.0),
 (100.0, 399.9974740035907),
 (100.0, 370.3141091517281),
 (100.0, 370.3125),
 (100.0, 370.31089089000875),
 (100.0, 332.81337085546045),
 (100.0, 332.8125),
 (100.0, 332.81162915624157),
 (100.0, 300.00060937576177),
 (0.0, 312.49999999999994),
 (0.0, 312.49837500203114),
 (0.0, 300.00160351637663),
 (0.0, 299.99999999999994),
 (0.0, 299.9983964851266)]
print(len(points_of_collision))

# remove coordinates if there are more then 3 close togther

new_points_of_collision = []

for index in range(len(points_of_collision)):
    index+1
    
    x1 = points_of_collision[index-1][0]
    y1 = points_of_collision[index-1][1]
    
    x2 = points_of_collision[index][0]
    y2 = points_of_collision[index][1]
    
    distance = math.hypot(x1 - x2, y1 - y2)
    if distance < 4:
        print(distance)
        # print(distance)
    # else:
        new_points_of_collision.append((x2,y2))
        # new_points_of_collision.append((x2,y2))
        # new_points_of_collision.append(x1)
        # new_points_of_collision.append(y1)
        # new_points_of_collision.append(x2)
        # new_points_of_collision.append(y2)
    # distance_2 = math.hypot(x3 - pt1, y3 - pt2)
    
    # 
    
    # print(coord)
print(len(new_points_of_collision))
# print(new_points_of_collision)