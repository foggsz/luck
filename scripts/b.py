graph = {}
graph['start'] ={}
graph['start']['a'] = 6
graph['start']['b'] = 2

graph['a'] = {}
graph['a']['c'] = 1

graph['b']  = {}
graph['b']['a'] = 1
graph['b']['d']   = 4

 
graph['c'] = {}
graph['c']['d'] = 1
graph['c']['fin'] = 8 



graph['d'] = {}
graph['d']['fin'] = 5

graph['fin'] = {}

inf = float("inf")
costs = {}
costs['a'] = 6
costs['b'] = 2
costs['c'] = inf
costs['d'] = inf
costs['fin']  = inf


parents = {}
parents['a'] = 'start'
parents['b'] = 'start'
parents['c'] = 'a'
parents['d'] = 'b'
parents['fin'] = None

processed = []


def find_lower_node(costs):
    lower_cost = float('inf')
    lower_cost_node = None
    for node in costs:
        cost = costs[node]
        if cost < lower_cost  and node not in processed:
            lower_cost = cost
            lower_cost_node = node    
    return lower_cost_node

def find():
    node = find_lower_node(costs)
    while node is not None:
        cost = costs[node]
        neighbors = graph[node]
        for n in neighbors.keys():
            new_cost = cost + neighbors[n]
            if costs[n] > new_cost:
                costs[n]  = new_cost
                # print(new_cost)
                # print(costs[n])
                # print(neighbors)
                parents[n] = node
        processed.append(node)
        node = find_lower_node(costs)

find()

values = [   i for i in parents.values() if i!="start"  ]
values = ['start']  +  values  + ["end"]
print(values)
