from pyswmm import Simulation, Nodes, Links, Subcatchments, Output


sim = Simulation(r"./example.inp")

# get single subcatchments
# subcatchments = Subcatchments(sim)
# s1 = subcatchments['S1']
slope = 0.005
for i in range(100):
    # print(s1.slope)
    sim.execute()
    sim.report()
    # print(sim)
    subcatchments = Subcatchments(sim)
    print(subcatchments.next)
    # s1 = subcatchments['S1']
    # print(s1.rainfall)
    # s1.slope = slope
    # slope += 0.005

    # get max rainfall
    # max_rainfall = max([s1.rainfall for step in sim])
    # print(max_rainfall)

# execute simulation
# for step in sim:
# print(step.swmm_report)
# if s1.rainfall > 0:
# print(s1.rainfall)

# get max rainfall
# max_rainfall = max([s1.rainfall for step in sim])
# print(max_rainfall)