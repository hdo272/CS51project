 def process():
    progress = 0
    for x in range(0, width):
        progress += 1
        for y in range(0, height):
            value = mags.item((x,y))
            if value >= upper:
                edges.itemset((x,y), 255)
				hystConnect(x, y)
#	for x in range(0, width):
#        for y in range(0, height):
#            if mags.item((x,y)) = 255:
#                edges.itemset((x,y), 255)
#            else: 
#                edges.itemset((x,y), 0)
